import pyads            # For communication with PLC over ADS protocol
import time
import numpy

# Define calibration matrix
cal = numpy.array([[-0.0161159, 0.040467, -0.707786,-14.2766, 0.193801, 13.8452],
                   [0.579572, 16.4595, -0.571547, -8.2168, -0.0727457, -8.02511],
                   [25.0472, 0.026137, 25.0513, -0.244966, 25.2247, -0.182197],
                   [0.0119462, 0.198209, -0.727862, -0.0917548, 0.727238, -0.102356],
                   [0.836814, -0.000669803, -0.404076, 0.176913, -0.418491, -0.163965],
                   [-0.0131681, -0.445029, -0.0225798, -0.446901, -0.0100986, -0.435543]])

# connect to the PLC
plc = pyads.Connection('5.162.109.168.1.1', pyads.PORT_TC3PLC1)  # pyads.PORT_TC3PLC1 = default port 851

# open the connection
plc.open()

# Write to calculate voltage offsets
plc.write_by_name('GVL_Receive.bCalculateOffset', True, pyads.PLCTYPE_BOOL)

# Write ready to recieve - set the PLC to transmit the scaled voltages
plc.write_by_name('GVL_Receive.bTransmitVoltages', True, pyads.PLCTYPE_BOOL)

for x in range(100):

    # Receive the scaled voltages
    v1 = plc.read_by_name('GVL_Transmit.fTransmitAI1', pyads.PLCTYPE_REAL)
    v2 = plc.read_by_name('GVL_Transmit.fTransmitAI2', pyads.PLCTYPE_REAL)
    v3 = plc.read_by_name('GVL_Transmit.fTransmitAI3', pyads.PLCTYPE_REAL)
    v4 = plc.read_by_name('GVL_Transmit.fTransmitAI4', pyads.PLCTYPE_REAL)
    v5 = plc.read_by_name('GVL_Transmit.fTransmitAI5', pyads.PLCTYPE_REAL)
    v6 = plc.read_by_name('GVL_Transmit.fTransmitAI6', pyads.PLCTYPE_REAL)

    # Encode into a vector and multiply for cal matrix (as a column vector)
    volts = numpy.array([v1,v2,v3,v4,v5,v6])

    # Matrix multiplication to get Forces/Torques
    FT = numpy.dot(cal, volts);
    print(FT)




# close connection
plc.close()