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
        # Calculate IP header length and transport layer start position
        ip_header_length = ihl * 4
        transport_start = 14 + ip_header_length  # Ethernet(14) + IP header length

        print(f"IP Packet:")
        print(f"Version: {version}, Header Length: {ip_header_length} bytes")
        print(f"TTL: {ttl}, Protocol: {protocol}")
        print(f"Source: {s_addr}, Destination: {d_addr}")
        print(f"Transport Layer Start: {transport_start}")

        # TCP protocol (6)
        if protocol == 6 and len(raw_packet) >= transport_start + 20:
            tcp_header = raw_packet[transport_start:transport_start+20]
            tcph = struct.unpack('!HHLLBBHHH', tcp_header)

            source_port = tcph[0]
            dest_port = tcph[1]
            flags = tcph[5]

            print(f"TCP Segment:")
            print(f"TCP Ports: {source_port}->{dest_port} Flags: {flags:08b}")

        elif protocol == 17 and len(raw_packet) >= transport_start + 8:
            udp_header = raw_packet[transport_start:transport_start+8]
            udph = struct.unpack('!HHHH', udp_header)
        
            source_port = udph[0]
            dest_port = udph[1]
            length = udph[2]
            checksum = udph[3]

            print(f"UDP Datagram:")
            print(f"UDP Ports: {udph[0]}->{udph[1]} Length: {length} bytes")
            print(f"Checksum: {checksum}")

def format_mac(bytes_addr):
    return ':'.join(f'{b:02x}' for b in bytes_addr)

if __name__ == "__main__":
    packet_sniffer()
