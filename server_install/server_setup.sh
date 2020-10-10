./ansible.sh
cp ansible_hosts /etc/ansible/hosts
ansible-playbook -C playbooks/ftp.yml