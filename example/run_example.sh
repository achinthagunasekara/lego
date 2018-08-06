#!/bin/bash

apt-get update
apt-get install -y python2.7 python-apt python-pip vim
pip install setuptools --upgrade
cd /mnt
python setup.py install
cd /mnt/example
lego build server.yaml

echo "################################################"
echo "INFO: Please kill the container when you're done"
echo "################################################"

# Ensure the continer keep running
while true; do sleep 100; done
