import sys
import argparse
import datetime
import ipaddress
from ping3 import ping

subnet = ''
output_file = ''


def ping_sweep(subnet):
    network = ipaddress.ip_network(subnet, strict=False)

    with open(output_file, 'a') as f:
        for ip in network.hosts():
            ip_str = str(ip)
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            message = ""
            try:
                response_time = ping(ip_str, timeout=1)
                if response_time is not None:
                    message = f"{timestamp} - {ip_str} is reachable"
                else:
                    message = f"{timestamp} - {ip_str} is unreachable"
            except Exception:
                message = f"{timestamp} - Error pinging {ip_str}"
            print(message)
            f.write(message + '\n')


parser = argparse.ArgumentParser(
    description="Network Ping Sweeper", formatter_class=argparse.ArgumentDefaultsHelpFormatter)


parser.add_argument("-s", "--subnet", help="Subnet for sweeping")
parser.add_argument("-o", "--output", help="output file name")


args = parser.parse_args()

if len(sys.argv) > 1:
    subnet = args.subnet
    output_file = args.output
    ping_sweep(subnet)
