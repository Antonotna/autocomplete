import sys
import re
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("host",type=str,help="Hostname")
parser.add_argument("ip",type=str,help="IP address of previously network")
parser.add_argument("desc",type=str,help="Description")
parser.add_argument("-v", action="store_true", help="add vpn string")
parser.add_argument("-z", action="store_true", help="If network is zero you should set current network in ip field and this option")

args = parser.parse_args()


host = args.host


desc = args.desc
d = re.split('\(',desc)


ip = args.ip

lip=ip.split('.')
three = '.'.join(lip[0:3])
if(args.z):
 nlip = int(lip[3])
else:
 nlip = int(lip[3]) + 32
vpn = nlip
mmedia = nlip + 8
sw = nlip + 16


#Network
out = host + "\t" + three + "." + str(nlip) + "\t# /27 " + desc + "\n"

#VPN
if(args.v):
 out = out + host + "-vpn\t" + three + "." + str(nlip) + "\t# /29 " + d[0] + "VPN (." + str(vpn+1) + "-cisco, ." + str(vpn+2) + "-asa)\n"

#MMEDIA
out = out + host + "-mmedia\t" + three + "." +str(mmedia) + "\t# /29 " + d[0] + "MMEDIA (." + str(mmedia+1) + "-cisco, ." + str(mmedia+6)+ "-IPOffice)\n"

#MGMT
out = out + host + "-mgmt\t" + three + "." + str(sw) + "\t# /29 " + d[0] + "MGMT (." + str(sw+1) + "-cisco, ." + str(sw+2) + "-." + str(sw+6) + "-sw*)\n"

sys.stdout.write(out)
