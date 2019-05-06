import socket
import sys
import argparse
from _thread import *
import time
import numpy as np
import math

class Middlebox():

    def __init__(self, args):
        self.args = args
        self.middlebox_name = self.args.middlebox_name
        print(self.middlebox_name)

        self.middleboxSocket = None

        self.turn_on()

    def turn_on(self):
        HOST = socket.gethostbyname('localhost')
        PORT = 5622

        self.middleboxSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(self.middlebox_name, 'socket is created')
        try:
            self.middleboxSocket.bind((HOST, PORT))
        except socket.error:
            print(self.middlebox_name, 'socket binding failed')
            sys.exit()

        self.middleboxSocket.settimeout(self.args.alive_time)
        print(self.middlebox_name, 'socket is succesfully initialized and ready.')

    def turn_off(self):
        self.middleboxSocket.close()

    def encrypt_sensitive_information(self, msg):
        print('Sending:'.rjust(15), msg, '(-> Guard)')
        time_interval = np.random.normal(0.8075, 0.1260, 1)[0]
        time.sleep(time_interval)

        # change SENSITIVE -> ENCRYPTED
        # change the name of IoT deivce to 'Guard'
        IoT_name = msg[57:]
        replaced_msg = msg.replace('SENSITIVE', 'ENCRYPTED')
        replaced_msg = replaced_msg.replace(IoT_name, 'Guard')

        # print completed msg
        print('Receiving:'.rjust(15), replaced_msg)

    def clientthread(self, conn, addr):
        # TYPE 1
        last_time_point = time.time()
        current_time_point = None 

        # TYPE 3
        last_time_sec = math.floor(last_time_point)
        last_time_count = 0        
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    break
                data_msg = data.decode()
                if len(data_msg) > 75:
                    continue
                
                print('Receiving:'.rjust(15), data_msg)

                # TYPE 2
                if data_msg[45:54] == 'SENSITIVE':
                    start_new_thread(self.encrypt_sensitive_information, (data_msg, ))

                # TYPE 1
                current_time_point = time.time()
                time_interval = current_time_point - last_time_point
                if time_interval >= 25:
                    self.print_detect_physical_access_attack()
                last_time_point = current_time_point

                # TYPE 3
                current_time_sec = math.floor(current_time_point)
                if current_time_sec == last_time_sec:
                    last_time_count += 1
                    if last_time_count > 10:
                        self.print_detect_IoT_DDoS() 
                else:
                    last_time_sec = current_time_sec
                    last_time_count = 0

            except:
                break 

        print('Connection to', addr[0], ':', str(addr[1]), 'is closed')
        print()
        conn.close()

    def start_listening(self):
        self.middleboxSocket.listen(10)
        print(self.middlebox_name, 'is listening...')
        print()

        while True:
            conn, addr = self.middleboxSocket.accept()
            print('Conneted with', addr[0], ':', str(addr[1]))
            start_new_thread(self.clientthread, (conn, addr, ))

        self.turn_off()

    def print_detect_physical_access_attack(self):
        print('Warning:'.rjust(15), 'Detecting suspicious physcial access attack!!!')     

    def print_detect_IoT_DDoS(self):
        print('Warning:'.rjust(15), 'Detecting suspicious IoT-DDoS attack!!!')           
        
parser = argparse.ArgumentParser(description='Middlebox instance creation')
parser.add_argument('--middlebox-name', type=str, default='Middlebox device', metavar='name',
                    help='name of the middlebox instance (default: Middlebox device)')
parser.add_argument('--alive-time', type=int, default=120, metavar='N',
                    help='Alive time of middlebox instances in seconds (default: 120)')
args = parser.parse_args()

print(args)
gateway = Middlebox(args)
gateway.start_listening()