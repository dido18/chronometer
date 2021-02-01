###
#
#   Thread that reads valus from the photo eletric sensor and sends them to the queue of events
#
###
import shared

__define(S_SENS_WAIT, 0x0)
__define(S_SENS_MONITOR,      0x1)


# the pin where the sensor reads the value form the photoeletric sensor
pinPhoto = D9
pinMode(pinPhoto, INPUT_PULLDOWN)

def loop():
    state = S_SENS_WAIT
    while True:
            
        if state == S_SENS_WAIT:
            try:
                print("[ThPhoto] waiting evt...")
                evt = shared.q_cmds.get()
                print("[ThPhoto] rcv evt ...", evt)
                if evt == shared.EVT_RACE_START:
                    state = S_SENS_MONITOR
            except QueueEmpty as e:
                print("[ThPhoto] no evt...")
                pass
            except Exception as e:
                print(e)  
            
        if state == S_SENS_MONITOR:
            if digitalRead(pinPhoto) == 1:
                print("[ThPhoto] Object detected")
                shared.q_cmds.put(shared.EVT_RACE_FINSIH)
                state = S_SENS_WAIT
            sleep(20)