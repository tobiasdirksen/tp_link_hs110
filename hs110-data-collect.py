import sys
import socket
import json
from struct import pack
from datetime import datetime
from pandas.io.json import json_normalize
import os


def int_to_bytes(x):
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')


def int_from_bytes(xbytes):
    return int.from_bytes(xbytes, 'big')

# Python 3.x version
if sys.version_info[0] > 2:
	def encrypt(string):
		key = 171
		result = pack('>I', len(string))
		for i in string:
			a = key ^ ord(i)
			key = a
			result += bytes([a])
		return result

	def decrypt(string):
		key = 171
		result = ""
		for i in string:
			a = key ^ i
			key = i
			result += chr(a)
		return result

# Python 2.x version
else:
	def encrypt(string):
		key = 171
		result = pack('>I', len(string))
		for i in string:
			a = key ^ ord(i)
			key = a
			result += chr(a)
		return result

	def decrypt(string):
		key = 171
		result = ""
		for i in string:
			a = key ^ ord(i)
			key = ord(i)
			result += chr(a)
		return result


def send_hs_command(address, port, cmd):
    data = b""
    tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        tcp_sock.connect((address, port))
        tcp_sock.send(encrypt(cmd))
        data = tcp_sock.recv(1024)
    except socket.error:
        raise ValueError("Socket closed")
    finally:
        tcp_sock.close()
    return data

def run(address):
"""Input ip address of HS110"""
    try:
        timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        timestamp_utc = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
        
        device_info = send_hs_command(address, 9999, b'{"system":{"get_sysinfo":null}}')
        decrypted_device_info = decrypt(device_info[4:]).decode()
        json_device_info = json.loads(decrypted_device_info)['system']['get_sysinfo']
        
        data = send_hs_command(address, 9999, b'{"emeter":{"get_realtime":{}}}')
        decrypted_data = decrypt(data[4:]).decode()
        json_data = json.loads(decrypted_data)
        
        df = json_normalize(json_data["emeter"]["get_realtime"])
        df['timestamp'] = timestamp
        df['timestamp_utc'] = timestamp_utc
        df['location'] = json_device_info['alias']
        df['rssi'] = json_device_info['rssi']

    except Exception as error:
        print(error)
