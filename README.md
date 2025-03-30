![CI/CD Status](https://github.com/Stormlabuk/ATIBeckhoff/actions/workflows/ros2_ci.yaml/badge.svg)

This Repo contains code for reading the ATI loadcell through the Beckhoff PLC.

## dir descriptions
The repo contains four directies.

1. BeckhoffPLCCode contains the PLC code that runs on the PLC. This code reads the AI, zeroes the AI readings and handles communication with external PCs.
2. PythonReceiveADS contains python code which can be run either on Windows or on Ubuntu to test communications with the Beckhoff PLC.
3. calibrationFile contains the calibration matrix for the ATI loadcell.
4. loadcell is the dir which must be cloned to your ros2_ws/src directory in ubuntu. It contains the ros2 code to handle the ADS communications with the PLC and to publish the measured wrench across the ROS2 network.


## Network setup

The PLC has been given the static IP address 172.31.1.90. This allows it to coexist on the same network as a KUKA iiwa.
The Ubuntu PC must have the IP address 172.31.1.50, since this has been set as a network path in the PLC configuration parameters.
The Windows PC (if required) must have an IP address of 172.31.1.xxx.


## Dependencies

1. For setup, the windows PC must have Beckhoff TwinCAT3 IDE installed. Just for running this is unnecessary.
2. For normal running, the PLC code has already been downloaded to the PLC, and should begin as soon as power has been provided.
3. Both windows and Ubuntu must have the python3 package 'pyads' for communication with the PLC over the ADS connection (a specific flavour of TCP/IP)