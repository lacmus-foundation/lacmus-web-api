import openstack
import logging
import requests
import time
from ml_worker import MLWorker
from commons.config import ORIGINAL_ML_WORKER_VOLUME, ML_WORKER_PORT


# 1/
# openstack volume create ml-worker-cpu-01-volume --source ubuntu-20-04-1-lacmus-api-worker-cpu
# 2. создаем тачку
# openstack server create ml-cpu-worker-01 --flavor cpu.16.32.160 --key-name gosha20777 --network inetcom --volume ml-worker-cpu-01-volume
# 3, ждем статус Active, получаем IP,
# шлем на IP:5000 фотки
# 4. убиваем сервер
# openstack server delete ml-cpu-worker-01
# 5. убиваем волум
# openstack volume delete ml-worker-cpu-01-volume

# All functions implemented as sync intentionally, as they run from a separate processing thread

def create_ml_worker():
    try:
        logging.info("Connecting to openstack")
        conn = openstack.connect()
        logging.info("openstack: Creating volume")
        origin_volume = conn.get_volume(ORIGINAL_ML_WORKER_VOLUME)
        if origin_volume is None:
            raise Exception('Volume %s not found' % ORIGINAL_ML_WORKER_VOLUME)
        volume = conn.create_volume(20, wait=True, name='ml-worker-cpu-volume',
                                    source_volid=origin_volume['id'], bootable=True)

        logging.info("openstack: Volume created. Creating server")
        server = conn.create_server(name='ml-cpu-worker-lacmus',
                                    boot_volume=volume['id'],
                                    boot_from_volume=True,
                                    flavor='cpu.16.32.160',
                                    network='inetcom',
                                    key_name='gosha20777',
                                    security_groups=['lacmus_worker_to_orchestrator'],
                                    wait=True)
        logging.info("openstack: Server created, id=%s. Waiting to come active" % server['id'])
        server = conn.wait_for_server(server)
        logging.info("openstack: Server active. Obtaining IP")
        ip_address = None
        if ('public_v4' in server) and (server.public_v4 is not None):
            ip_address = server.public_v4
        if (ip_address is None) or (ip_address == ''):
            logging.error("openstack: No IP address for server id %s " % (server['id']),
                          exc_info=False)
            raise AttributeError(" server created in openstack, but failed to receive IP")
            # todo - should we try to delete server in such a case, if it created, but don't have IP,
            # how could it happen?

        logging.info("openstack: IP is %s. Waiting worker to boot up" % ip_address)
        conn.close()
        try_attempts = 0
        while True:
            try:
                try_attempts += 1
                response = requests.get('http://%s:%i/api/v2/ping' % (ip_address, ML_WORKER_PORT))
                if not response.ok:
                    raise BaseException("response = %s" % response.reason)
                logging.info("Got ok ping from server %s :)! "%ip_address)
                return MLWorker(server, ip_address, volume)
            except:
                logging.info("Got exception during ping, seems worker is not up yet, wait 2 sec. Try=%i" % try_attempts)
            time.sleep(2)


    except:
        if conn != None:
            conn.close()
        logging.error("openstack: failed create worker ", exc_info=True)
        return None


def try_to_find_exising_workers():
    try:
        logging.info("Trying to found running servers. Connecting to openstack")
        conn = openstack.connect()
        servers = conn.list_servers(detailed=False)
        found = []
        for server in servers:
            if 'ml-cpu-worker-lacmus' == server.name:
                if (server.status == 'ACTIVE') and ('public_v4' in server) \
                        and (server.public_v4 is not None) and (server.public_v4 != ''):
                    found.append(MLWorker(server, server.public_v4))
        return found
    except:
        if conn != None:
            conn.close()
        logging.error("openstack: failed to query workers worker ", exc_info=True)
        return []


def kill_worker(worker: MLWorker):
    try:
        logging.info("Deleting worker %s. Connecting to openstack" % worker.ip)
        conn = openstack.connect()
        if worker.volume is None:
            logging.info("This is preexisting worker, need to query volume")
            server = conn.get_server(worker.server['id'], detailed=True)
            # there is only one volume. Why it's not in 'volumes' but in this weird property  -
            # only openstack devs knows
            volume = server['os-extended-volumes:volumes_attached'][0]
            logging.info('Information obtained. Server.id = %s, volume. id = %s' % (
                server['id'], volume['id']
            ))
        else:
            logging.info("This is worker we created")
            server = worker.server
            volume = worker.volume
        server_delete_result = conn.delete_server(server['id'], wait=True)
        logging.info("Deleted server with result %s" % str(server_delete_result))
        if (server_delete_result):
            vol_delete_result = conn.delete_volume(volume['id'], wait=True)
            logging.info("Deleted volume with result %s" % str(vol_delete_result))
    except:
        if conn != None:
            conn.close()
        logging.error("openstack: failed delete worker ", exc_info=True)
        return
