#!/bin/bash
sleep 240s && ps -e | grep recon-all | awk '{print $1}' >> $1
