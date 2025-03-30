This dir must be which must be cloned to your ros2 workspace --- as a suggestion: ros2_ws/src directory in ubuntu. It contains the ros2 code to handle the ADS communications with the PLC and to publish the measured wrench across the ROS2 network.

The code has a dependecy on the python3 'pyads' package, which handles communication with the Beckhoff PLC across the ADS network (a specific flavour of TCP/IP)

Publish the node by:

'''
ros2 run loadcell PublishWrench.py
'''