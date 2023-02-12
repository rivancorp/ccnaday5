import json
import telnetlib

with open("router_config.json") as f:
    config = json.load(f)

hostname = config["hostname"]
password = config["password"]
ip_address = config["ip_address"]

tn = telnetlib.Telnet(ip_address)

tn.read_until(b"Username: ")
tn.write(hostname.encode('ascii') + b"\n")

tn.read_until(b"Password: ")
tn.write(password.encode('ascii') + b"\n")

tn.write(b"enable\n")
tn.write(password.encode('ascii') + b"\n")

tn.write(b"configure terminal\n")

for iface, info in config["interface"].items():
    tn.write(f"interface {iface}\n".encode('ascii'))
    tn.write(f"description {info['description']}\n".encode('ascii'))
    tn.write(f"ip address {info['ip_address']} {info['subnet_mask']}\n".encode('ascii'))
    tn.write(b"no shutdown\n")

tn.write(b"end\n")
tn.write(b"exit\n")

print(tn.read_all().decode('ascii'))