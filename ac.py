import sys
import re
import argparse
from netaddr import *

parser = argparse.ArgumentParser()

parser.add_argument("host",type=str,help="Hostname")
parser.add_argument("ip",type=str,help="IP address of previously network")
parser.add_argument("desc",type=str,help="Description")
parser.add_argument("-v", action="store_true", help="add vpn string")
parser.add_argument("-z", action="store_true", help="If current network is zero you should set it in ip field and flag 'z' up")

args = parser.parse_args()


host = args.host


desc = args.desc
d = re.split('\(',desc)


ip = IPNetwork(args.ip+'/27')
if(args.z):
 next_net = ip
else:
 next_net = ip.next()
l29 = list(next_net.subnet(29))

#Network
out = host + "\t" + str(next_net.network) + "\t# /" + str(next_net.prefixlen) + " " + desc + "\n"

#VPN
if(args.v):
 vnet = l29[0]
 vhosts = list(vnet.iter_hosts())
 out = out + host + "-vpn\t" + str(vnet.network) + "\t# /" + str(vnet.prefixlen) + " " + d[0] + "VPN (." + str(vhosts[0].words[3]) + "-cisco, ." + str(vhosts[1].words[3]) + "-asa)\n"

#MMEDIA
mmnet = l29[1]
mmhosts = list(mmnet.iter_hosts())
out = out + host + "-mmedia\t" + str(mmnet.network) + "\t# /" + str(mmnet.prefixlen) + " " + d[0] + "MMEDIA (." + str(mmhosts[0].words[3]) + "-cisco, ." + str(mmhosts[5].words[3])+ "-IPOffice)\n"

#MGMT
mgnet = l29[2]
mghosts = list(mgnet.iter_hosts())
out = out + host + "-mgmt\t" + str(mgnet.network) + "\t# /" + str(mgnet.prefixlen) + " " + d[0] + "MGMT (." + str(mghosts[0].words[3]) + "-cisco, ." + str(mghosts[1].words[3]) + "-." + str(mghosts[5].words[3]) + "-sw*)\n"

sys.stdout.write(out)