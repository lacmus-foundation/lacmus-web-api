For initial server setup run
```
git clone git@github.com:lacmus-foundation/lacmus-web-api.git
```

define your password in ~/.bashrc
	MINIO_ACCESS_KEY
 	MINIO_SECRET_KEY
 	POSTGRES_PASSWORD

define your hosts in lacmus-web-api/server_install/ansible_hosts (for single-server config you can keep default 127.0.0.1) 
define your external host name in lacmus-web-api/server_install/playbooks/DockerFiles/ftp/vsftpd.conf in setting pasv_address 

Whole settings are not tested for the case of multiserver installation, but supposedly you'll have to publish relevant ports 
instead of exposing those and define system variable POSTGRES_SERVER FTP_SERVER MINIO_SERVER. As orchestator runs docker 
containers locally - workers yet should be build and available to start on the same host as orchestrator

```
cd lacmus-web-api/server_install
chmod +x ./server_setup.sh
sudo ./server_setup.sh
```

Some useful commands:
	Running psql client (on db server): 
	docker exec -it postgres_instance psql -U postgres