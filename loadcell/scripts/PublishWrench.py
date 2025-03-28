#!/usr/bin/env python3

import rclpy
import pyads
import numpy as np
from rclpy.node import Node
from geometry_msgs.msg import Wrench, Vector3

class LoadCellPublisher(Node):

    def __init__(self):
        super().__init__('loadcell_publisher')

        # Initialise the publisher for ROS2
        self.publisher = self.create_publisher(Wrench, 'loadcell_data', 10)

        # Create a timer to publish data every 0.01 seconds
        self.timer = self.create_timer(0.01, self.timer_callback)

        # Define the calibration matrix
        self.calibration_matrix = np.array([[-0.0161159, 0.040467, -0.707786, -14.2766, 0.193801, 13.8452],
                                            [0.579572, 16.4595, -0.571547, -8.2168, -0.0727457, -8.02511],
                                            [25.0472, 0.026137, 25.0513, -0.244966, 25.2247, -0.182197],
                                            [0.0119462, 0.198209, -0.727862, -0.0917548, 0.727238, -0.102356],
                                            [0.836814, -0.000669803, -0.404076, 0.176913, -0.418491, -0.163965],
                                            [-0.0131681, -0.445029, -0.0225798, -0.446901, -0.0100986, -0.435543]])

        # Connect to Beckhoff PLC
        self.plc = pyads.Connection('5.162.109.168.1.1', pyads.PORT_TC3PLC1, '172.31.1.90')
        self.plc.open()

        # Set local AMS address for Ubuntu machine
        pyads.set_local_address('172.31.1.50.1.1')

        # Write to the PLC to prepare for data transmission
        self.plc.write_by_name('GVL_Receive.bCalculateOffset', True, pyads.PLCTYPE_BOOL)
        self.plc.write_by_name('GVL_Receive.bTransmitVoltages', True, pyads.PLCTYPE_BOOL)

    def timer_callback(self):
        # Receive the scaled voltages from the PLC
        v1 = self.plc.read_by_name('GVL_Transmit.fTransmitAI1', pyads.PLCTYPE_REAL)
        v2 = self.plc.read_by_name('GVL_Transmit.fTransmitAI2', pyads.PLCTYPE_REAL)
        v3 = self.plc.read_by_name('GVL_Transmit.fTransmitAI3', pyads.PLCTYPE_REAL)
        v4 = self.plc.read_by_name('GVL_Transmit.fTransmitAI4', pyads.PLCTYPE_REAL)
        v5 = self.plc.read_by_name('GVL_Transmit.fTransmitAI5', pyads.PLCTYPE_REAL)
        v6 = self.plc.read_by_name('GVL_Transmit.fTransmitAI6', pyads.PLCTYPE_REAL)

        # Encode the voltages into a vector
        volts = np.array([v1, v2, v3, v4, v5, v6])

        # Apply calibration matrix to calculate forces and torques
        FT = np.dot(self.calibration_matrix, volts)

        # Extract force and torque components
        force = Vector3(x=FT[0], y=FT[1], z=FT[2])  # Forces in N
        torque = Vector3(x=FT[3], y=FT[4], z=FT[5])  # Torques in Nm

        # Create the message and publish
        msg = Wrench()
        msg.force = force
        msg.torque = torque
        self.publisher.publish(msg)

        #self.get_logger().info(f'Publishing load cell data: Force: {force}, Torque: {torque}')

    def __del__(self):
        # Close the connection when the node is destroyed
        self.plc.close()

def main(args=None):
    rclpy.init(args=args)
    node = LoadCellPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

