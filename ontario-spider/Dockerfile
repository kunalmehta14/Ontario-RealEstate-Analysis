FROM ubuntu:latest
ENV LANG en_US.utf8
#Update Ubuntu
RUN apt update && apt full-upgrade -y
RUN apt install \
    sudo -y \
    supervisor -y \
    nano

RUN DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get -y install tzdata
# Install python and the python dependencies
RUN apt install python3-pip -y
# Create App Directory
RUN mkdir /opt/app
# RUN chown administrator:root /opt/app
COPY ./app/requirements.txt /opt/app/requirements.txt
WORKDIR /opt/app
RUN pip install -r requirements.txt
#Copy supervisoryd.conf configuration that defines the startup services
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
#Copy the logging script and make it executable
USER root
RUN ln -sf /proc/1/fd/1 /var/log/scrapy.log
RUN ln -sf /proc/1/fd/1 /var/log/amenties-calculator.log
RUN ln -sf /proc/1/fd/1 /var/log/avgprice-calculator.log
#start startup services when the server starts
CMD ["/usr/bin/supervisord"]