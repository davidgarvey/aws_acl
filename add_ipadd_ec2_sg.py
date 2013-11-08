#!/usr/bin/python
import boto.ec2
import os, sys
import argparse
key = os.environ['AWS_SECRET_ACCESS_KEY']
id = os.environ['AWS_ACCESS_KEY_ID']
ec2Region = 'us-east-1'
filename = 'last.ip'
parser = argparse.ArgumentParser(description='Add ip address to ec2')
parser.add_argument('--ip', help='Need ip address for mysql port')
args = parser.parse_args()
ip = str(args.ip) 
cidr = "%s/32" %ip

if not os.path.exists(filename):
    file = open(filename, 'wb')
    file.write(ip + "\n")
    file.close()
    conn = boto.ec2.connect_to_region(ec2Region,aws_access_key_id=id, aws_secret_access_key=key)
    rs = conn.get_all_security_groups()
    sg = rs[0]
    if sg.name == 'dev':
        sg.authorize(ip_protocol="tcp", from_port=3306, to_port=3306, cidr_ip=cidr)

else:
    sys.exit(1)
