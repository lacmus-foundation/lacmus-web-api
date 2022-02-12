FROM     ubuntu:focal
ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update 
RUN apt-get install -y vsftpd python3 python3-pip postgresql-common libpq-dev
COPY requirements.txt .
RUN pip3 install -r requirements.txt

RUN mkdir /etc/ftp_projects
COPY vsftpd.conf /etc/vsftpd.conf
COPY vsftpd.pam /etc/pam.d/vsftpd

COPY ftp_api/ /root/ftp_api/
WORKDIR /root/ftp_api
CMD service vsftpd start && uvicorn server:app --host 0.0.0.0 --port 5001

EXPOSE 21
EXPOSE 5001