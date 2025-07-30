import serial.tools.list_ports

ports = serial.tools.list_ports.comports()

# Search for the Bridgertron Serial Ports
def findPort(interface_num):
    for port in ports:
        #print(f"Port: {port.device}, Description: {port.description}, Hardware ID: {port.hwid}, Location: {port.location}")
        #if BRIDGERTRON_USB_VID_PID in port.hwid
        #print(port.hwid)
        usb_pid_vid_index = port.hwid.find("=")
        # Was "=" found, indicating the USB VID/PID, which is the first "=" in the port.hwid
        if usb_pid_vid_index != -1:
            usb_pid_vid_index = usb_pid_vid_index + 1
            usb_vid_pid = port.hwid[usb_pid_vid_index : usb_pid_vid_index + 9] # USB_PID_VID_LEN
            #print(usb_vid_pid)
            # Is this the Bridgertron Board USB VID/PID?
            if usb_vid_pid == "1FC9:00A3": # BRIDGERTRON_USB_VID_PID
                # print("Bridgertron Serial Port!!")
                location_index = port.hwid.find("LOCATION")
                # Was "location" found in the port.hwid
                if location_index != -1:
                    # print("Location Index:", location_index)
                    location = port.hwid[location_index : ]
                    # Does the location field exist?
                    if location != "None":
                        # print(location)
                        interface_index = location.find(":")
                        if interface_index != -1:
                            #print("Interface Index:", interface_index)
                            interface_index = interface_index + 1
                            interface = location[interface_index + 2 : ]
                            # print("Interface:", interface)
                            if int(interface) == interface_num:
                                #print("  Serial Port =", port.device, "For Interface:", interface_num)
                                return port.device
                                
                else:
                    print("`Location` Not Found for Bridgertron, ALLOWING THIS ANYWAY!!!", port.device)
                    return port.device # TODO: THIS REALLY SHOULD RETURN -1
                    #return -1

    print("No Device Found!")
    return -1
