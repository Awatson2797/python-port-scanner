import socket

# Dictionary of common ports
services = {
    20: "FTP",
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    3306: "MySQL",
    3389: "RDP",
}

def get_ip(target):
    try:
        return socket.gethostbyname(target)
    except socket.gaierror:
        print(f"Error: Unable to resolve '{target}'.")
        return None

def scan_port(target, port):

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    
    result = sock.connect_ex((target, port))
    sock.close()

    if result == 0:
        service = services.get(port, "Unknown")
        return (port, service)
    return None

def get_port(prompt):
    while True:
        try:
            port = int(input(prompt))
            if 0 <= port <= 65535:
                return port

            print("Please enter a valid port number between 0 and 65535.")
        except ValueError:
            print("Invalid input. Please enter a number.")

target = input("Enter a host or IP to scan: ")
ip = get_ip(target)

if ip is None:
    exit()

start_port = get_port("Enter the starting port: ")
end_port = get_port("Enter the ending port: ")

print(f"\nScanning {target}...\n")
open_ports = []
for port in range(start_port, end_port + 1):

    result = scan_port(ip, port)

    if result is not None:
        port_number, service = result
        open_ports.append(result)


print("\n======Scan Complete======")
print(f"Open Ports Found: {len(open_ports)}")

for result in open_ports:
    port, service = result
    print(f"{port:<6} {service}")