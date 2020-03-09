#!/usr/bin/env python3

import os
import ssl
import socket
import argparse
import sys

def parse_args():
    # parse the arguments
    parser = argparse.ArgumentParser(epilog='\tExample: \r\npython ' + sys.argv[0] + " -d jd.com")
    parser.add_argument('-d', '--domain', help="input domain",default=None)
    return parser.parse_args()


def cert(hostname):

	ctx = ssl.create_default_context()
	s = ctx.wrap_socket(socket.socket(), server_hostname=hostname)
	try:
		try:
			s.connect((hostname, 443))
			info = s.getpeercert()
		except:
			ctx = ssl._create_unverified_context()
			s = ctx.wrap_socket(socket.socket(), server_hostname=hostname)
			s.connect((hostname, 443))
			info = s.getpeercert(True)
			info = ssl.get_server_certificate((hostname, 443))
			f = open('{}.pem'.format(hostname), 'w')
			f.write(info)
			f.close()
			cert_dict = ssl._ssl._test_decode_cert('{}.pem'.format(hostname))
			info = cert_dict
			os.remove('{}.pem'.format(hostname))
		try:
			for _,domain in info['subjectAltName']:
				print(domain)
		except KeyError:
			pass

	except:
		print (' SSL is not Present on Target URL...Skipping...')

if __name__=='__main__':
	args = parse_args()
	domain = args.domain
	cert(domain)