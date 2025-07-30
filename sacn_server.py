import sacn
import serial
import time
import serial_port_utility as spu
import host_protocol as hp
from threading import Event
from threading import Thread

newData = Event()

port_num = spu.findPort(0)   # Interface #2 is for the "Data" port
if port_num != -1:
    print("Serial Data Port:",port_num)
    s = serial.Serial(port_num, 10000000)
else:  print("NO SERIAL DATA PORT FOUND!!!")

bytes_per_frame = 1024

header = bytearray(hp.PACKET_HDR_SIZE + 4) #The first data word is the channel number

led_buf = bytearray(bytes_per_frame * 32)

# Send the "Bytes Per Frame" message
hp.init(s, bytes_per_frame, hp.MODULATION_3_PHASE, 1000)
hp.packet_hdr(hp.CMD_LED_DATA, hp.BYTES_PER_FIELD + bytes_per_frame*32, 0, header)

def setByte(channel,byte,val):
     b = 32 * byte + channel
     led_buf[b] = val

def setLed(channel,led,red,green,blue):
     setByte(channel,led*3,blue)
     setByte(channel,led*3+1,red)
     setByte(channel,led*3+2,green)

def callback(packet):  # packet type: sacn.DataPacket
    if packet.dmxStartCode == 0x00:  # ignore non-DMX-data packets
        universe = packet.universe
        print(f"Universe {universe}")
        channel = int(universe/2)
        start = (universe%2-1)*512
        i=0
        t0 = time.time()
        for b in packet.dmxData:
            setByte(channel,start+i,b)
            i=i+1
        newData.set()

def update(newData):
    print("Starting update")
    while True:
        if (newData.isSet()):
            t0 = time.time()
            print("Frame!")
            s.write(header+led_buf)
            s.read(s.in_waiting)
            print(time.time()-t0)
            newData.clear()

receiver = sacn.sACNreceiver()
receiver.start()  # start the receiving thread
for i in range(1,9): receiver.register_listener('universe',callback,universe=i)  # listens on universes 1-8

thread = Thread(target=update, args=(newData,))
thread.start()

thread.join()

receiver.stop()
