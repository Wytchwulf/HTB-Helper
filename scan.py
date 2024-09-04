import os
import subprocess

def add_host_entry(target_ip, target_host):
    # Command to add entry to /etc/hosts
    command = f'echo "{target_ip} {target_host.lower()}.htb" | sudo tee -a /etc/hosts'
    os.system(command)
    print(f"Added {target_ip} {target_host} to /etc/hosts")

def nmap_scan(target_ip):
    # First nmap command to get open ports
    nmap_command = f"nmap -p- --min-rate 10000 -T4 {target_ip}"
    result = subprocess.run(nmap_command, shell=True, stdout=subprocess.PIPE, text=True)
    
    # Extract open ports
    ports = []
    for line in result.stdout.splitlines():
        if line.startswith(tuple(str(i) for i in range(10))):
            port = line.split('/')[0]
            ports.append(port)
    
    if ports:
        ports_str = ','.join(ports)
        # Second nmap command to scan specific ports
        detailed_scan_command = f"nmap -p {ports_str} -A -oN nmapScan {target_ip}"
        os.system(detailed_scan_command)
        print(f"Scan complete. Results saved to nmapScan.")
    else:
        print("No open ports found.")

if __name__ == "__main__":
    target_ip = input("Enter the target IP address: ")
    target_host = input("Enter the box name: ")

    add_host_entry(target_ip, target_host)
    nmap_scan(target_ip)
