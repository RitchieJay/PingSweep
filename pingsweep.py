import sys
import argparse
import datetime
import ipaddress
from ping3 import ping

subnet = ''
output_file = ''
verbose = True


def ping_sweep(subnet):
    network = ipaddress.ip_network(subnet, strict=False)
    scan_ip(network)


def scan_ip(network):
    for ip in network.hosts():
        message = ""
        message = compose(message, ip)
        if verbose:
            print(message)

        try:
            with open(output_file, 'a') as f:
                f.write(message + '\n')
        except:
            pass


def compose(msg, ip):
    ip_str = str(ip)
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    try:
        response_time = ping(ip_str, timeout=1)
        if response_time is not None:
            msg = f"{timestamp} - {ip_str} is reachable"
        else:
            msg = f"{timestamp} - {ip_str} is unreachable"
    except Exception:
        msg = f"{timestamp} - Error pinging {ip_str}"

    return msg


parser = argparse.ArgumentParser(
    description="Network Ping Sweeper", formatter_class=argparse.ArgumentDefaultsHelpFormatter)


parser.add_argument("-s", "--subnet", help="Subnet for sweeping")
parser.add_argument("-o", "--output", help="output file name")


args = parser.parse_args()

if len(sys.argv) > 1:
    subnet = args.subnet
    output_file = args.output
    ping_sweep(subnet)
