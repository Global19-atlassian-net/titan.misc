#/bin/bash

VMID=($HOSTS)

for ID in "${VMID[@]}"
do
  IP=`vm_images.sh 2>/dev/null | awk -v VM_IDX="$((ID + 1))" 'NR == VM_IDX {print $3;exit}'`
  ping -c 1 $IP > /dev/null 2>&1
  if [[ $? = 0 ]]; then
    echo "$IP is up"
  else
    echo "$IP is down, starting wake-up procedure"
    vm_images.sh -start "$ID"
  fi
    ssh root@$IP "sntp -P no -r 172.31.21.66"
    if [[ $? != 0 ]]; then
      ssh root@$IP "ntpdate -s 172.31.21.66"
    fi
done

