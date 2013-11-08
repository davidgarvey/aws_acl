#!/usr/bin/python
import boto.ec2
import os
key = os.environ['AWS_SECRET_ACCESS_KEY']
id = os.environ['AWS_ACCESS_KEY_ID']
ec2Region = 'us-east-1'
filename = 'last.ip'

ip = [line.strip() for line in open(filename)]
print ip[0]
cidr_ip = "%s/32" %ip[0]
print cidr_ip


conn = boto.ec2.connect_to_region(ec2Region,aws_access_key_id=id, aws_secret_access_key=key)
rs = conn.get_all_security_groups()
#print rs
sg = rs[0]
#print sg.name
if sg.name == 'dev':
    print sg.rules
    for rule in sg.rules:
        for ip in rule.grants:
            if rule.ip_protocol == "tcp" and rule.from_port == '3306':
               print ip
    #sg.authorize(ip_protocol="tcp", from_port=3306, to_port=3306, cidr_ip=cidr)
    sg.revoke(ip_protocol="tcp", from_port=3306, to_port=3306, cidr_ip=cidr_ip)



try:
    os.remove(filename)
except OSError:
    pass
