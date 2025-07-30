# Host Protocol Definitions

# The "Packet Header" that contains control information, see:
# `host_protcol.py`
# Bytes   description
#   4     Magic Number Constant - For Synchronization
#   4     Command
#   4     Size of Data[] contained in the Packet
PACKET_HDR_FIELDS = 3
BYTES_PER_FIELD   = 4
PACKET_HDR_SIZE = PACKET_HDR_FIELDS * BYTES_PER_FIELD

# Host commands
CMD_DEV_INFO_REQ     = 1
CMD_BYTES_PER_FRAME  = 2
CMD_MODULATION       = 3
CMD_BLANKING_TIME_US = 4
CMD_LED_DATA         = 5
CMD_LED_DATA_RESP    = 6

MODULATION_3_PHASE = 3
MODULATION_4_PHASE = 4

BLANKING_TIME_US_MIN  = 100
BLANKING_TIME_US_MAX  = ((0xFFFFFFFF * 125) / (100 * 4))

MAGIC_NUMBER_CONSTANT = 0x03773DFC

def init(ser_data, bytes_per_frame, modulation_type, blanking_time_us):
    send_buf = bytearray(PACKET_HDR_SIZE + BYTES_PER_FIELD) # Add a "Field" for the Payload Data to Send

    # Get Device Info
    # Note: The "Device Info Request" doesn't have any associated data
    print("Get Device Info")
    packet_hdr(CMD_DEV_INFO_REQ, PACKET_HDR_SIZE, 0, send_buf)
    ser_data.write(send_buf)
    response = ser_data.readline().decode('utf-8').strip()
    print("Response:", response)

    # Send "Bytes Per Frame" = Bytes/LED * Number of LED's    
    print("Send Bytes Per Frame:", bytes_per_frame)
    packet_hdr(CMD_BYTES_PER_FRAME, (PACKET_HDR_SIZE + BYTES_PER_FIELD), bytes_per_frame, send_buf)
    ser_data.write(send_buf)
    response = ser_data.readline().decode('utf-8').strip()
    print("Response:", response)

    # Send "Modulation Type" = 3 or 4 Phase
    # NOTE: The "Bytes Per Frame" must be send before the "Modulation Type"
    print("Send Modulation Type:", modulation_type)
    packet_hdr(CMD_MODULATION, (PACKET_HDR_SIZE + BYTES_PER_FIELD), modulation_type, send_buf)
    ser_data.write(send_buf)
    response = ser_data.readline().decode('utf-8').strip()
    print("Response:", response)

    # Send "Blanking Time in us (micro seconds)" = Must be greater than 100 us    
    print("Send Blanking Time:", blanking_time_us)
    packet_hdr(CMD_BLANKING_TIME_US, (PACKET_HDR_SIZE + BYTES_PER_FIELD), blanking_time_us, send_buf)
    ser_data.write(send_buf)
    response = ser_data.readline().decode('utf-8').strip()
    print("Response:", response)

def packet_hdr(cmd, size, value, buf):
    # Magic Number Constant
    buf[0]  = 0xFC
    buf[1]  = 0x3D
    buf[2]  = 0x77
    buf[3]  = 0x03

    # Command (1 byte)
    buf[4]  = cmd
    buf[5]  = 0
    buf[6]  = 0
    buf[7]  = 0

    # Size of the Data[]
    buf[8]  = size & 0xFF
    buf[9]  = (size >> 8) & 0xFF
    buf[10] = (size >> 16) & 0xFF 
    buf[11] = (size >> 24) & 0xFF   

    # Value associated with Command
    buf[12] = value & 0xFF
    buf[13] = (value >> 8) & 0xFF
    buf[14] = (value >> 16) & 0xFF
    buf[15] = (value >> 24) & 0xFF
