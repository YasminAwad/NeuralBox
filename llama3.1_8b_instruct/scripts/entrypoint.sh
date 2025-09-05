#!/bin/bash

# Start the SSH service in the background
/usr/sbin/sshd

# Start Jupyter Lab
jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root --NotebookApp.token='' --NotebookApp.password=''