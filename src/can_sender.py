#! /usr/bin/env python3

import rospy
import can
from can_master.msg import can_out
from time import sleep


class CANSender:
    def __init__(self) -> None:
        rospy.init_node("can_sender")
        self.can_sub = rospy.Subscriber("can_out", can_out, self.can_cb, queue_size=20)
        self.outgoing = dict()

    def can_cb(self, msg: can_out):
        self.outgoing[(msg.arb_id, msg.sub_id)] = msg.data

    def loop(self):
        with can.interface.Bus(
            bustype="socketcan", channel="can0", is_extended_id=False, bitrate=500000
        ) as bus:
            while not rospy.is_shutdown():
                # Swap outgoing dictionary with snapshot so that snapshot is no longer updated
                msgs, self.outgoing = self.outgoing, dict()
                for id, msg in msgs.items():
                    can_msg = can.Message(
                        arbitration_id=id[0], data=msg, is_extended_id=False
                    )

                    sleep(0.01)

                    try:
                        bus.send(can_msg)
                        # bus.flush_tx_buffer()
                    except can.CanError as e:
                        print(e)
                        bus.flush_tx_buffer()
                    except Exception as e:
                        print("Error Sending...")
                        bus.flush_tx_buffer()
                        print(e)
            

def main():
    can_sender = CANSender()
    can_sender.loop()


if __name__ == "__main__":
    main()
