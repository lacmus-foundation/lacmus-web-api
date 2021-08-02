Follow the instruction at https://openvinotoolkit.github.io/cvat/docs/administration/basics/installation/
Before starting the docker 

1. create directory /media/data/cvat (or another one and update docker-compose.override.yml accordingly)
2. export your hostname like (put it to ~/.bashrc)
 export CVAT_HOST=176.99.131.182
3. copy docker-compose.override.yml to cvat folder like 
	scp docker-compose.override.yml app-dev-01:/home/ubuntu/cvat/
4. start with docker-compose -f docker-compose.yml -f docker-compose.override.yml up -d instead of command in manual


