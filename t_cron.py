###
#
#   Thread that reads valus from the photo eletric sensor and sends them to the queue of events
#
###
import shared

pinPhoto = D9
pinMode(pinPhoto, INPUT_PULLDOWN)

def loop():
    while True:
        #print("[ThPhoto] no object ")
        if digitalRead(pinPhoto) == 1:
            print("[ThPhoto] Object detected")
            shared.q_cmds.put(shared.CMD_OBJ_PRESENCE)
            
        sleep(200)