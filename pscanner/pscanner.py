#Developed by SoloPietro
from socket import gaierror, gethostbyname, socket, AF_INET, SOCK_STREAM
from tabulate import tabulate
from argparse import ArgumentParser
from subprocess import PIPE, TimeoutExpired, run
from threading import Thread
from ipaddress import ip_address
from scapy.all import ARP, Ether, srp
from datetime import datetime

parser = ArgumentParser(description="Host port scanner.")
parser.add_argument('-ip', type=str, help="Set target ip")
parser.add_argument('-url', type=str, help="Set target url")
parser.add_argument('--start_port', type=int, help="Set the port where scanning will begin (Default 1)")
parser.add_argument('--end_port', type=int, help="Set the port where scanning will end (Default 1024)")
args = parser.parse_args()

thread = []
open_port = []

def convert_to_ip(domain_name):
    try:
        ip_address = gethostbyname(domain_name)
        return ip_address
    except gaierror:
        return "Error: Invalid or unreachable domain"

def read_services(filename):
    services = {}
    with open(filename, 'r') as f:
        for line in f:
            if not line.startswith('#') and line.strip():
                parts = line.split()
                if len(parts) >= 2:
                    port = int(parts[1].split('/')[0])
                    service_name = parts[0]
                    services[port] = service_name
    return services

def get_mac_address(ip_address):
    arp_request = ARP(pdst=ip_address)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    
    answered_list = srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    
    if answered_list:
        return answered_list[0][1].hwsrc
    else:
        return None

def ip_check(ip):
    try:
        ip_address(ip)
        try:
            output = run(
                ["ping", "-c", str(1), ip],
                stdout=PIPE,
                stderr=PIPE,
                timeout=3 
            )
            if output.returncode == 0:
                return True 
            else:
                print("\nThe host seems down. If it's really active, he blocks the ping.")
                return False
        except TimeoutExpired:
            print("\nThe host seems down. If it's really active, he blocks the ping.")
            return False
        except Exception as e:
            print("\nThe host seems down. If it's really active, he blocks the ping.")
            return False
    except ValueError:
        return False

def init_scan_port(ip, port):
    s = socket(AF_INET, SOCK_STREAM)
    s.settimeout(1)
    try:
        result = s.connect_ex((ip, port))
        if result == 0:
            open_port.append(port)
    finally:
        s.close()

def run_thread(max_thread=1000):
    global thread
    
    num_groups = (len(thread) + max_thread - 1) // max_thread
    
    for group in range(num_groups):
        start = group * max_thread
        end = min((group + 1) * max_thread, len(thread))
    
        for i in range(start, end):
            thread[i].start()
        
        for i in range(start, end):
            thread[i].join()

def main():
    global thread
    start_port = 1
    end_port = 1024
    
    if args.url is not None:
        args.ip = convert_to_ip(args.url)
            
    if args.ip is not None and ip_check(args.ip):
        ip = args.ip
    else:
        print("Error: Please provide a valid target IP with -ip option (-h for more information)")
        exit()
        
    if args.start_port is not None: start_port = args.start_port
    if args.end_port is not None: end_port = args.end_port

    if start_port < 1: start_port = 1
    if end_port > 65535: end_port = 65535
    if start_port > end_port: 
        temp = start_port
        start_port = end_port
        end_port = temp

    print("Start scanning...")
    print("Started:", datetime.now().strftime("%H:%M:%S"))
    
    for port in range(start_port, end_port + 1):
        thread.append(Thread(target=init_scan_port, args=[ip, port]))
	        
    run_thread()
  
    open_port.sort()
    
    nmap_services_file = './service'
    service_map = read_services(nmap_services_file)
    data = [["PORT", "STATE", "SERVICE"]]
    
    for port in open_port:
        service_name = service_map.get(port, "Unknown")
        data.append([port, "Open" ,service_name])

    print(f"Ports scanned: {end_port-start_port+1}")
    print("\n" + tabulate(data, headers="firstrow", tablefmt="plain"))
    if get_mac_address(ip) is not None:
        print("\nMAC ADDRESS:", get_mac_address(ip).upper())
    
    print("\nFinished:", datetime.now().strftime("%H:%M:%S"))

try:
    main()
except KeyboardInterrupt:
    print("\nScanner stopped by user")