FROM     ubuntu:20.04

RUN apt-get update ; apt-get install -y vsftpd
COPY vsftpd.conf /etc/vsftpd.conf
CMD service vsftpd start && tail -F /var/log/vsftpd.log

EXPOSE 21