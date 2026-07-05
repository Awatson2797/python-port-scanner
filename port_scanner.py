import socket
import time

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


def get_port(prompt):
    """Prompt the user until a valid TCP port is entered."""
    while True:
        try:
            port = int(input(prompt))
            if 0 <= port <= 65535:
                return port

            print("Please enter a valid port number between 0 and 65535.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def main():
    # Get target information from the user
    target = input("Enter a host or IP to scan: ")

    # Resolve the hostname before scanning
    ip = get_ip(target)

    if ip is None:
        exit()

    # Get a valid range of ports to scan from the user
    start_port = get_port("Enter the starting port: ")
    end_port = get_port("Enter the ending port: ")

    print(f"Target : {target}")
    print(f"IP     : {ip}")
    print(f"Ports  : {start_port}-{end_port}")

    print(f"\nScanning {target}...\n")

    open_ports = []

    # Start timing the scan
    start_time = time.time()

    # Scan every port in the specified range
    for port in range(start_port, end_port + 1):

        result = scan_port(ip, port)

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

if __name__ == "__main__":
    main()