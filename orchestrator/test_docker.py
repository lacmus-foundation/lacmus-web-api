import docker
import uuid
client = docker.DockerClient(base_url='unix://var/run/docker.sock')
# client.
worker_cont = client.containers.run("ml_worker_yolo5", None, auto_remove=True, detach=True, name="ml_worker_%s"%uuid.uuid4(),
                      network="lacmus_server")



for n in client.networks.list():
    print(n.name)
