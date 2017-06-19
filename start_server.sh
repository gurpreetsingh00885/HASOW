sudo ifconfig enp2s0 192.168.12.1 netmask 255.255.255.0
echo
echo
echo "----------   Welcome to HASoW   ----------"
printf "\n\nThis project was implemented by\n-Gurpreet Singh\n-Haripal Baluja\n-Harmanjeet Singh\n-Mani Kumar\n\n------------------------------------------\nStarting Hotspot and server now...\n\n\n"
./utility.sh "sudo create_ap wlp4s0 lo HASoW-Server 1234567890" "python2 manage.py runserver 0:8000"
