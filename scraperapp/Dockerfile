FROM ubuntu:latest
ENV LANG en_US.utf8
#Update Ubuntu
RUN apt update && apt install \
    openssh-server -y \
    openssh-client -y \
    sudo -y \
    supervisor -y \
    rsync -y \
    nano
#Adds administrator user and the dedicated user directory
RUN useradd -rm -d /home/administrator -s /bin/bash -g root -G sudo -u 1000 administrator 
#Configures the following password for the user
RUN  echo 'administrator:password' | chpasswd
#Start the SSH service and expose port 22
RUN service ssh start
EXPOSE 22
RUN DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get -y install tzdata
#Install python and the python dependencies
RUN apt install python3-pip -y
RUN mkdir /opt/app
RUN chown administrator:root /opt/app
COPY app/requirements.txt /opt/app/requirements.txt
RUN pip install -r /opt/app/requirements.txt
#Copy supervisoryd.conf configuration that defines the startup services
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
#start startup services when the server starts
CMD ["/usr/bin/supervisord"]