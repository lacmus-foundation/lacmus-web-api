import time
import uuid
import docker
import logging
from docker import types
import requests
import commons.config as config


class MLWorker:
    def __init__(self, ip: str, container):
        self.container = container
        self.ip = ip


def create_ml_worker():
    try:
        logging.info("Connecting to docker")
        # https://stackoverflow.com/questions/30535755/can-a-docker-container-manage-other-docker-containers
        # https://docker-py.readthedocs.io/en/stable/
        client = docker.DockerClient(base_url='unix://var/run/docker.sock')
        logging.info("starting worker")
        worker_cont = client.containers.run(config.DOCKER_IMAGE_NAME, None, detach=True,
                                            name="lacmus_ml_worker_%s" % uuid.uuid4(),
                                            network=config.DOCKER_NETWORK,
                                            device_requests=[docker.types.DeviceRequest(
                                                count=-1, capabilities=[['gpu']]
                                            )])
        container = worker_cont
        try_attempts = 0
        while True:
            try:
                try_attempts += 1
                if try_attempts > config.KILL_WORKER_AFTER//2:
                    logging.error("Still failed to get worker ping after %i tries. Try to kill it" % try_attempts)
                    try:
                        container.kill()
                    except:
                        logging.error("failed delete worker, it probably committed suicide ", exc_info=True)
                    return None
                container.reload()
                ip = container.attrs['NetworkSettings']['Networks'][config.DOCKER_NETWORK]['IPAddress']
                if ip is None or len(ip) == 0:
                    logging.info("docker: ip not yet obtained. Try=%i" % try_attempts)
                    time.sleep(2)
                    continue
                logging.info("docker: Worker created. IP:%s" % ip)
                response = requests.get('http://%s:%i/api/v0/ping' % (ip, config.ML_WORKER_PORT))
                if not response.ok:
                    raise BaseException("response = %s" % response.reason)
                logging.info("Got ok ping from server %s :)! " % ip)
                return MLWorker(ip, container)
            except:
                logging.info("Got exception during ping, seems worker is not up yet, wait 2 sec. Try=%i" % try_attempts,
                             exc_info=True)
                time.sleep(2)
    except:
        logging.error("docker: failed create worker ", exc_info=True)
        return None


def try_to_find_existing_workers():
    try:
        logging.info("Trying to found running servers")
        client = docker.DockerClient(base_url='unix://var/run/docker.sock')
        found = []
        containers = client.containers.list(filters={"status": "running", "ancestor": config.DOCKER_IMAGE_NAME})
        for container in containers:
            ip = container.attrs['NetworkSettings']['Networks'][config.DOCKER_NETWORK]['IPAddress']
            logging.info("Found container %s" % ip)
            response = requests.get('http://%s:%i/api/v0/ping' % (ip, config.ML_WORKER_PORT))
            if response.ok:
                found.append(MLWorker(ip, container))
                logging.info("Ping ok, using this worker")
        return found
    except:
        logging.error("docker: failed to query workers worker ", exc_info=True)
        return []


def kill_worker(worker: MLWorker):
    try:
        logging.info("Deleting worker %s." % worker.ip)
        worker.container.kill()
    except:
        logging.error("failed delete worker ", exc_info=True)
        return
