chmod +x ./ansible.sh
./ansible.sh
cp ansible_hosts /etc/ansible/hosts
ansible-playbook playbooks/ftp_docker.yml
ansible-playbook playbooks/minio_docker.yml
ansible-playbook playbooks/postgres_docker.yml
ansible-playbook playbooks/identity_api_docker.yml