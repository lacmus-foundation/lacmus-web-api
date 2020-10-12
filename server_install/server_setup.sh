chmod +x ./ansible.sh
./ansible.sh
cp ansible_hosts /etc/ansible/hosts
#ansible-playbook -C playbooks/ftp_docker.yml