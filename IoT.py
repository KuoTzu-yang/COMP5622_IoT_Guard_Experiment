import argparse
import datetime
import random
import socket
import time

import numpy as np

from _thread import *


class IoT():

    def __init__(self, args):
        self.args = args
        self.IoT_name = self.args.IoT_name
        print(self.IoT_name)

        self.IoT_socket = None

        self.turn_on()
        
    def turn_on(self):
        PORT = 5622
        HOST = socket.gethostbyname('localhost')
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocket.connect((HOST, PORT))
        self.IoT_socket = clientSocket

    def turn_off(self):
        self.IoT_socket.close()

    def communicate_with_middlebox(self):
        if self.args.is_physical_access_attack:
            self.emit_normal_traffic_under_physical_access_attack_to_middlebox() # TYPE 1
        elif self.args.is_sensitive_information:
            self.emit_normal_traffic_with_sensitive_information_to_middlebox() # TYPE 2
        elif self.args.is_IoT_DDoS:
            self.emit_IoT_DDoS_traffic_to_middlebox() # TYPE 3
        else:
            self.emit_normal_traffic_to_middlebox() # NORMAL

    # NORMAL
    def emit_normal_traffic_to_middlebox(self):
        time_intervals = np.random.normal(self.args.normal_traffic_mu, self.args.normal_traffic_sigma, self.args.num_msgs)
        for i in range(self.args.num_msgs):
            time.sleep(time_intervals[i])
            
            _, self_PORT = self.IoT_socket.getsockname()
            random_val = random.randint(0, 99)
            packet_content = ' {val} | {time} | {port} | {traffic_type} | {IoT_name}'.format(val=str(random_val).rjust(3), time=str(datetime.datetime.now()).rjust(25), port=str(self_PORT).rjust(6), traffic_type='NORMAL'.rjust((9)), IoT_name=self.IoT_name)
            print('Sending:', packet_content)
            self.IoT_socket.sendall(packet_content.encode())

        self.turn_off()

    # TYPE 1: physical access attack 
    def emit_normal_traffic_under_physical_access_attack_to_middlebox(self):
        time_intervals = np.random.normal(self.args.normal_traffic_mu, self.args.normal_traffic_sigma, self.args.num_msgs)
        attack_point = random.randint(0, self.args.num_msgs-1)
        print('TYPE 1, physical access attack, attack point:', attack_point)
        for i in range(self.args.num_msgs):
            if i == attack_point:
                time.sleep(self.args.physical_access_time)
            else:
                time.sleep(time_intervals[i])
            
            _, self_PORT = self.IoT_socket.getsockname()
            random_val = random.randint(0, 99)
            packet_content = ' {val} | {time} | {port} | {traffic_type} | {IoT_name}'.format(val=str(random_val).rjust(3), time=str(datetime.datetime.now()).rjust(25), port=str(self_PORT).rjust(6), traffic_type='NORMAL'.rjust(9), IoT_name=self.IoT_name)
            print('Sending:', packet_content)
            self.IoT_socket.sendall(packet_content.encode())

        self.turn_off()

    # TYPE 2: contains sensitive information
    def emit_normal_traffic_with_sensitive_information_to_middlebox(self):
        time_intervals = np.random.normal(self.args.normal_traffic_mu, self.args.normal_traffic_sigma, self.args.num_msgs)
        for i in range(self.args.num_msgs):
            time.sleep(time_intervals[i])
            
            packet_content = None
            _, self_PORT = self.IoT_socket.getsockname()
            random_val = random.randint(0, 99)
            if random.random() < 0.5:
                packet_content = ' {val} | {time} | {port} | {traffic_type} | {IoT_name}'.format(val=str(random_val).rjust(3), time=str(datetime.datetime.now()).rjust(25), port=str(self_PORT).rjust(6), traffic_type='SENSITIVE'.rjust(9), IoT_name=self.IoT_name)
            else:
                packet_content = ' {val} | {time} | {port} | {traffic_type} | {IoT_name}'.format(val=str(random_val).rjust(3), time=str(datetime.datetime.now()).rjust(25), port=str(self_PORT).rjust(6), traffic_type='NORMAL'.rjust(9), IoT_name=self.IoT_name)

            print('Sending:', packet_content)
            self.IoT_socket.sendall(packet_content.encode())

        self.turn_off()

    # TYPE 3: IoT-DDoS attack 
    def emit_IoT_DDoS_traffic_to_middlebox(self):
        start_time = time.time()
        while time.time() - start_time < self.args.IoT_DDoS_traffic_time:
            time_interval = np.random.normal(self.args.IoT_DDoS_traffic_mu, self.args.IoT_DDoS_traffic_sigma, 1)[0]
            time.sleep(time_interval)

            _, self_PORT = self.IoT_socket.getsockname()
            random_val = random.randint(0, 99)
            packet_content = ' {val} | {time} | {port} | {traffic_type} | {IoT_name}'.format(val=str(random_val).rjust(3), time=str(datetime.datetime.now()).rjust(25), port=str(self_PORT).rjust(6), traffic_type='IoT-DDoS'.rjust(9), IoT_name=self.IoT_name)
            print('Sending:', packet_content)
            self.IoT_socket.sendall(packet_content.encode())

        self.turn_off()




class Guard(IoT):
    
    def __init__(self):
        super(IoT, self).__init__()

class ExperimentManager(IoT):
    
    def __init__(self):
        super(IoT, self).__init__()

parser = argparse.ArgumentParser(description='IoT instance creation')

parser.add_argument('--IoT-name', type=str, default='IoT device', metavar='name',
                    help='name of the IoT instance (default: IoT device)')
parser.add_argument('--num-msgs', type=int, default=100, metavar='N',
                    help='num of messages transmitted from an IoT device to the middlebox (default: 100)')

parser.add_argument('--physical-access-time', type=int, default=30, metavar='T',
                    help='time for a malicious attack to conduct physcial access attack in seconds (default: 30)')

parser.add_argument('--normal-traffic-mu', type=float, default=5, metavar='mu',
                    help='mean of time interval between normal packets in seconds (default: 5)') 
parser.add_argument('--normal-traffic-sigma', type=float, default=1, metavar='sigma',
                    help='std of time interval between normal packets in seconds (default: 1)') 

parser.add_argument('--IoT-DDoS-traffic-mu', type=float, default=0.001, metavar='mu',
                    help='mean of time interval between normal packets in seconds (default: 0.001)') 
parser.add_argument('--IoT-DDoS-traffic-sigma', type=float, default=0.0002, metavar='sigma',
                    help='std of time interval between normal packets in seconds (default: 0.0002)') 
parser.add_argument('--IoT-DDoS-traffic-time', type=int, default=120, metavar='T',
                    help='time of per IoT-DDoS attack in seconds (default: 120)') 

parser.add_argument('--is-IoT-DDoS', action='store_true', default=False,
                    help='enables IoT-DDoS attack')
parser.add_argument('--is-sensitive-information', action='store_true', default=False,
                    help='indicate whether traffic flow contains sensitive information')
parser.add_argument('--is-physical-access-attack', action='store_true', default=False,
                    help='enables physical access attack')
args = parser.parse_args()

print(args)
inst1 = IoT(args)
inst1.communicate_with_middlebox()


# Step 2
# go, go, go lots of experiments  

# Step 3
# write a functionality which can record the log of the server 
# draw from experiments 

# Extra:
# 1. write an GitHub readme if time allows 
# 2. actually attacks can be combined -> for instance, type 1 and type 2
