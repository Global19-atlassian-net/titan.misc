#!/bin/sh -xe
#obsolete

#env
#cd TTCNv3/usrguide
#chmod a+x pdfgen.sh
#./pdfgen.sh
#cd ..
#mkdir -p ${WORKSPACE}/RELEASE


for HOST in tcclab1 tcclab2 tcclab3 gen_vm
do
	echo "idx     state   ip            host    name
1       idle    172.31.21.229 tcclab2 openSUSE 10.0 64bit
2       idle    172.31.21.224 tcclab2 openSUSE 11.1
3       idle    172.31.21.239 tcclab2 openSUSE 11.2 64bit
4       running 172.31.21.199 tcclab3 openSUSE 11.3 64bit
5       idle    172.31.21.203 gen_vm openSUSE 12.1 64bit
6       running 172.31.21.227 tcclab3 SLED 10 32 bit
7       idle    172.31.21.230 tcclab3 SLED 10.1 32 bit
8       idle    172.31.21.234 tcclab2 SLED 10.1 64 bit
9       idle    172.31.21.231 tcclab3 SLED 10.2 32 bit
10      idle    172.31.21.232 tcclab3 SLED 10.2 64 bit
11      idle    172.31.21.248 tcclab3 SLED 10.3 32 bit
12      idle    172.31.21.249 tcclab3 SLED 10.3 64 bit
13      idle    172.31.21.242 gen_vm SLED 11.0 32 bit
14      idle    172.31.21.244 gen_vm SLED 11.0 64 bit
15      running 172.31.21.241 tcclab1 SLED 11.1 64 bit
16      idle    172.31.21.208 tcclab1 SLED 11.1 32 bit
17      idle    172.31.21.219 tcclab1 SUSE Linux 10.1 32-bit
18      running 172.31.21.221 tcclab1 SUSE Linux 10.0 32 bit
19      running 172.31.21.218 tcclab1 SUSE Linux Enterprise Server 10 32-bit
20      idle    172.31.21.236 tcclab1 SUSE Linux Enterprise Server 10.1 32 bit
21      idle    172.31.21.247 tcclab2 SUSE Linux Enterprise Server 10.1 64 bit
22      idle    172.31.21.214 tcclab1 SUSE Linux Enterprise Server 10.2 64-bit
23      idle    172.31.21.212 tcclab1 SUSE Linux Enterprise Server 10.2 32 bit
24      idle    172.31.21.252 tcclab2 SUSE Linux Enterprise Server 10.3 64-bit
25      running 172.31.21.240 tcclab1 SUSE Linux Enterprise Server 11.1 64 bit
26      idle    172.31.21.225 tcclab1 SUSE Linux Enterprise Server 9 32 bit
27      idle    172.31.21.216 tcclab1 Red Hat Enterprise Linux 4 32 bit
28      idle    172.31.21.215 tcclab3 Red Hat Enterprise Linux 4 64 bit
29      idle    172.31.21.233 tcclab3 Red Hat Enterprise Linux 5 32 bit
30      idle    172.31.21.217 tcclab3 Red Hat Enterprise Linux 5 64 bit
31      running 172.31.21.251 tcclab1 Red Hat Enterprise Linux 6 64 bit
32      idle    172.31.21.211 gen_vm Ubuntu 8.10 64-bit
33      idle    172.31.21.213 gen_vm Ubuntu 8.10 32 bit
34      idle    172.31.21.228 tcclab2 Ubuntu 9.04 64bit
35      idle    172.31.21.235 tcclab2 Ubuntu 9.10 64bit
36      running 172.31.21.200 gen_vm Ubuntu 9.10 32bit
37      idle    172.31.21.237 tcclab3 Ubuntu 10.04 64bit desktop
38      idle    172.31.21.238 tcclab2 Ubuntu 10.04 64bit server
39      idle    172.31.21.246 gen_vm Ubuntu 10.10 64bit desktop
40      idle    172.31.21.250 tcclab2 Ubuntu 11.04 64bit desktop
41      idle    172.31.21.207 gen_vm Ubuntu 11.10 64bit desktop
42      running 172.31.21.206 gen_vm Ubuntu 12.04 64bit desktop
43      running 172.31.21.205 gen_vm Ubuntu 12.04 32bit desktop
44      idle    172.31.21.202 tcclab3 Debian 6 32 bit" | grep -E "(idle|running).*$HOST" | awk '{ print $1 }' | xargs -I image bash -c 'echo image $HOST; sleep 1' &
done
wait

# vm_images.sh #instead of the hardcoded string

# make_titan_package.sh -d ${WORKSPACE}/RELEASE -r v3-1-pl0 -p /home/titanrt/jenkins/usrguide_pdf -v image
# cd ${WORKSPACE}/RELEASE
# rsync -auv . esekilxxen1843.rnd.ericsson.se:/proj/TTCN/www/ttcn/root/download 
