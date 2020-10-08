#!/bin/bash

ping -c 1 $IP_ADDRESS > /dev/null 2>&1

if [[ $? = 0 ]]; then
  echo "$IP_ADDRESS is up"
else
  echo "$IP_ADDRESS is down, starting wake-up procedure"
  vm_images.sh -start "$VM_ID"
fi
