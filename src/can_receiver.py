#! /usr/bin/env python3

import rospy
import can
from can_master.msg import can_in
import time
import os
from std_msgs.msg import Float64

class CAN_Receiver:
    def __init__(self) -> None:
        rospy.init_node("can_receiver")

        print('Bring up CAN0....\n')
        try:
            os.system("sudo /sbin/ip link set can0 down")
            time.sleep(0.1)
        except Exception as e:
            print(e)

        try:
            os.system("sudo /sbin/ip link set can0 up type can bitrate 500000")
            # os.system("sudo -S ifconfig can0 txqueuelen 1000")
            time.sleep(0.1)
        except Exception as e:
            print(e)

        can_pub = rospy.Publisher("can_in", can_in, queue_size=10)
        # self.response = dict()
        filters = [{"can_id":0x200, "can_mask":0x200}]
        with can.interface.Bus(bustype='socketcan', channel='can0', is_extended_id=False, bitrate=500000, can_filters=filters) as bus:
            while not rospy.is_shutdown():
                # try:
                #     msg = bus.recv(1)
                #     if msg:
                #         out_msg = can_in()
                #         out_msg.arb_id = msg.arbitration_id 
                #         out_msg.data = msg.data
                #         can_pub.publish(out_msg)                    
                # except Exception as e:
                #     print(e)
                msg = bus.recv()
                # self.response[msg.arbitration_id] = msg.data
                response = can_in(arb_id=msg.arbitration_id, data=msg.data, t_stamp=Float64(msg.timestamp))
                # self.response[msg.arbitration_id] = can_in(data=msg.data, t_stamp=msg.timestamp)
                can_pub.publish(response)


def main():
    can_receiver = CAN_Receiver()


if __name__ == "__main__":
    main()