#!/bin/bash
# The application log will be redirected to the main docker container process's stdout, so # that it will show up in the container logs
ln -sf /proc/1/fd/1 /var/log/scrapy.log
ln -sf /proc/1/fd/1 /var/log/amenties-calculator.log