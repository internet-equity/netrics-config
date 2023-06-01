#!/bin/bash
docker run -it --name nm-mgmt-config1 \
       -e BALENA_DEVICE_UUID=051a9184995bdd161e4a031ec8b38fc1 \
       -v $PWD/volume/etc/nm-exp-active-netrics/:/etc/nm-exp-active-netrics/ \
       nm-mgmt-config
