# Python TCP Port Scanner

A command-line TCP port scanner written in Python using the `socket` library. This project scans a user-specified range of TCP ports on a target host or IP address and identifies common network services running on open ports.

---

## Features

- Scan a hostname or IP address
- Resolve hostnames to IP addresses using DNS
- Scan a custom range of TCP ports
- Validate user input
- Detect open TCP ports
- Display common service names for known ports
- Handle invalid hostnames and port numbers gracefully

---

## Technologies

- Python 3
- socket

---

## How It Works

1. Enter a hostname or IP address.
2. The program resolves the hostname to an IP address.
3. Enter the starting and ending port numbers.
4. The scanner attempts a TCP connection to each port.
5. Open ports are displayed along with their associated service names.

---

## Example

```text
Enter a host or IP to scan: scanme.nmap.org
Enter the starting port: 20
Enter the ending port: 100

========== Scan Complete ==========

Open Ports Found: 2

22     SSH
80     HTTP
```

---

## Skills Demonstrated

- Socket Programming
- TCP/IP Networking
- DNS Resolution
- Python Functions
- Exception Handling
- Input Validation
- Dictionaries
- Lists and Tuples
- Command-Line Applications

---

## Future Improvements

- [ ] Export scan results to a text file
- [ ] Display scan duration
- [ ] Multithreaded scanning
- [ ] Banner grabbing
- [ ] Service/version detection
- [ ] Command-line arguments
- [ ] Save results as CSV

---

## Disclaimer

This project is intended for educational purposes and should only be used to scan systems you own or have permission to test.