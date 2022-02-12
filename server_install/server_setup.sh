chmod +x ./ansible.sh
./ansible.sh
cp ansible_hosts /etc/ansible/hosts
docker network create lacmus_server
# you have to install postgres first, as other modules uses DB and will crush with it
ansible-playbook playbooks/network.yml
ansible-playbook playbooks/postgres_docker.yml
ansible-playbook playbooks/minio_docker.yml
ansible-playbook playbooks/ml_worker_yolo5.yml
ansible-playbook playbooks/ftp_docker.yml
ansible-playbook playbooks/identity_api_docker.yml
ansible-playbook playbooks/orchestrator_docker.yml