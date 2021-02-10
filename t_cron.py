###
#   This thread is responsabile to 
#    1) read value of photo eletric sensor.
#    2) mantains the timer of the lap time.
#  
###
import shared
import timers

__define(S_SENS_WAIT,         0x0)
__define(S_SENS_MONITOR,      0x1)
__define(S_SENS_EXIT,         0x2)


# photoeletric sensor pin

pinPhoto = D9
pinMode(pinPhoto, INPUT_PULLDOWN)

def loop():
    state = S_SENS_WAIT
    
    # timer used to calculate the lap time.
    t = timers.timer()
    while True:
        if state == S_SENS_WAIT:
            try:
                evt = shared.q_evts.peek()
                if evt == shared.EVT_RACE_START:
                    t.start()
                    print("    [ThPhoto] receive race start")
                    # delete the event only if it is a RACE START, beacuse otherwose it can get also the RACE_FINISH event
                    shared.q_evts.clear()
                    # TODO wait some delay (or define another START_STATE) in order to avoid to finish immediately because it can enter into MONITOR state
                    state = S_SENS_MONITOR
            except QueueEmpty as e:
                pass
            except Exception as e:
                print(e)  
            
        elif state == S_SENS_MONITOR:
            if digitalRead(pinPhoto) == 0:
                lap_time = t.get()
                #print("[ThPhoto] lap time", lap_time)
                shared.EVT_RACE_FINSIH['v'] = lap_time
                print("    [ThPhoto] sent race finish", shared.EVT_RACE_FINSIH)
                shared.q_evts.put(shared.EVT_RACE_FINSIH)
                state = S_SENS_WAIT
    