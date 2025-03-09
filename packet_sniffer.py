import socket
import struct
import time

def packet_sniffer():
    try:
        # Create raw socket (requires admin privileges)
        sniffer = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
        sniffer.settimeout(2)

        print("Starting packet capture... (Press Ctrl+C to stop)")
        while True:
            try:
                raw_packet = sniffer.recvfrom(65535)[0]
                parse_packet(raw_packet)

            except socket.timeout:
                # Handle timeout gracefully
                continue

    except KeyboardInterrupt:
        print("\nCapture stopped by user")
    finally:
        sniffer.close()

def parse_packet(raw_packet):
    # Parse Ethernet header (first 14 bytes)
    eth_header = raw_packet[:14]
    eth = struct.unpack('!6s6sH', eth_header)
    dest_mac = format_mac(eth[0])
    src_mac = format_mac(eth[1])
    proto = socket.htons(eth[2])

    print(f"\nEthernet Frame:")
    print(f"Destination: {dest_mac}, Source: {src_mac}, Protocol: {proto}")

    # Parse IP packets (Ethertype 0x0800)
    if proto == 8:
        ip_header = raw_packet[14:34]
        iph = struct.unpack('!BBHHHBBH4s4s', ip_header)

        version_ihl = iph[0]
        version = version_ihl >> 4
        ihl = version_ihl & 0xF
        ttl = iph[5]
        protocol = iph[6]
        s_addr = socket.inet_ntoa(iph[8])
        d_addr = socket.inet_ntoa(iph[9])

        print(f"IP Packet:")
        print(f"Version: {version}, Header Length: {ihl*4} bytes")
        print(f"TTL: {ttl}, Protocol: {protocol}")
        print(f"Source: {s_addr}, Destination: {d_addr}")

        # TCP protocol (6)
        if protocol == 6:
            tcp_header = raw_packet[34:54]
            tcph = struct.unpack('!HHLLBBHHH', tcp_header)

            source_port = tcph[0]
            dest_port = tcph[1]
            flags = tcph[5]

            print(f"TCP Segment:")
            print(f"Source Port: {source_port}, Dest Port: {dest_port}")
            print(f"Flags: {flags:08b}")

def format_mac(bytes_addr):
    return ':'.join(f'{b:02x}' for b in bytes_addr)

if __name__ == "__main__":
    packet_sniffer()
