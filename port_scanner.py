import socket
import time
import argparse
from concurrent.futures import ThreadPoolExecutor

# Common network services mapped to their default ports
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
    """Resolve a hostname to an IP address."""
    try:
        return socket.gethostbyname(target)
    except socket.gaierror:
        print(f"Error: Unable to resolve '{target}'.")
        return None

def scan_port(target, port):
    """Attempt a TCP connection to determine if a port is open."""

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    
    result = sock.connect_ex((target, port))
    sock.close()

    if result == 0:
        service = services.get(port, "Unknown")
        return (port, service)
    return None

def save_results(target, ip, open_ports, duration):
    """Write scan results to a text file."""

    with open("scan_results.txt", "w") as file:

        file.write("==== Python TCP Port Scanner ====\n\n")

        file.write(f"Target: {target}\n")
        file.write(f"IP Address: {ip}\n")
        file.write(f"Open Ports Found: {len(open_ports)}\n")
        file.write(f"Scan Time: {duration:.2f} seconds\n\n")

        file.write("Open Ports\n")
        file.write("------------------------\n")

        for port, service in open_ports:
            file.write(f"{port:<6} {service}\n")

def parse_ports(port_range):
    """Convert a port range string into starting and ending ports."""
    
    try:
        ports = port_range.split("-")
        # Validate the port range before starting the scan
        if len(ports) != 2:
            raise ValueError("Invalid port range format. Use 'start-end'.")
        
        start_port = int(ports[0])
        end_port = int(ports[1])

        if not (0 <= start_port <= 65535 and 0 <= end_port <= 65535):
            raise ValueError("Port numbers must be between 0 and 65535.")

        if start_port > end_port:
            raise ValueError("Start port must be less than or equal to end port.")
        
        return start_port, end_port
    
    except ValueError:
        print("Error: Ports must be inn the format start-end, like 20-100.")
        return None

def main():
    # Configure and parse command-line arguments
    parser = argparse.ArgumentParser(
        description="A multithreaded TCP port scanner."
    )
    parser.add_argument(
        "host",
        help="Hostname or IP address to scan."
    )
    parser.add_argument(
        "-p",
        "--ports",
        required=True,
        help="Port range (example: 20-100)"
    )

    args = parser.parse_args()

    target = args.host

    # Resolve the hostname before scanning
    ip = get_ip(target)

    if ip is None:
        exit()

    # Parse and validate the requested port range
    port_range = parse_ports(args.ports)

    if port_range is None:
        return
    
    start_port, end_port = port_range

    # Display scan information
    print(f"Target : {target}")
    print(f"IP     : {ip}")
    print(f"Ports  : {start_port}-{end_port}")

    print(f"\nScanning {target}...\n")

    open_ports = []

    # Start timing the scan
    start_time = time.time()

    # Use a thread pool to scan multiple ports simultaneously for improved performance
    ports = range(start_port, end_port + 1)

    with ThreadPoolExecutor(max_workers=100) as executor:
        results = executor.map(lambda port: scan_port(ip, port), ports)

    for result in results:
        if result is not None:
            open_ports.append(result)

    # Calculate the duration of the scan
    end_time = time.time()
    duration = end_time - start_time

    # Display scan summary
    print("\n====================")
    print("    Scan Complete")
    print("=====================\n")
    print(f"Open Ports Found: {len(open_ports)}")

    if open_ports:
        for port, service in open_ports:
            print(f"{port:<6} {service}")
    else:
        print("No open ports found.")

    print(f"\nScan completed in {duration:.2f} seconds.")


    # Save the results to a file
    save_results(target, ip, open_ports, duration)
    print("\nResults saved to 'scan_results.txt'.")

# Run the scanner only when this file is executed directly
if __name__ == "__main__":
    main()