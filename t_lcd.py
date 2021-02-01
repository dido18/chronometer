import shared
import streams
import lcd2
import timers

streams.serial()

# states of the FSM
__define(STATE_READY,          0x0)
__define(STATE_SHOW_ELAPSED,   0x1)
__define(STATE_SHOW_RESULT,    0x2)


# button use to reset the lcd after a lap is finished
bntReset  = D10
pinMode(bntReset, INPUT_PULLDOWN)

# global lcd object
lcd = None

def init_lcd():
    global lcd
    while True:
        try:
            lcd = lcd2.LCD(I2C0, addr=39)
            break
        except Exception as e:
            print(e)
        sleep(100)

# function to show the countdown sequence to the lcd screen
def countdown_sequence():
    global lcd
    lcd.clear()
    for col in range(5, 0, -1):
        lcd.set_cursor(col-1, 0)
        lcd.pprint("#")
        lcd.set_cursor(col-1, 1)
        lcd.pprint("#")
        sleep(1000)
    lcd.clear()
    # play a sound to the buzzer

def loop():
    init_lcd()
    print("LCD initialized")
    
    # set initial state
    state        = STATE_READY
    lap_time     = 0        # store the lap time in milliseconds
    
    # timer used to calculate the time of each lap and elapsed time
    t = timers.timer()
    
    while True:
        btnVal = digitalRead(bntReset)
        evt = None
          
        if state == STATE_READY:
            lcd.clear()
            lcd.pprint("Ready ")
            if btnVal == 1: 
                countdown_sequence()
                t.start()
                shared.q_cmds.put(shared.EVT_RACE_START)
                state = STATE_SHOW_ELAPSED

        elif state == STATE_SHOW_ELAPSED:
            elapsed_time = t.get()
            s = elapsed_time // 1000
            print("[ThLCD] Elapsed time:", s,"(s)")
            lcd.clear()
            lcd.pprint("%d"%(s))
            try:
                print("[ThLCD] waiting stop race...")
                # TODO: how to define correct timeout values in order to 
                evt = shared.q_cmds.get(timeout=10)
                if evt == shared.EVT_RACE_FINSIH:
                    lap_time = t.get()
                    print("[ThLCD] FINISH race.", lap_time)
                    state = STATE_SHOW_RESULT
            except QueueEmpty as e:
                pass
            except Exception as e:
                print(e)  
            # TODO: the value of the button in unstable even with INPUT_PULLDONW
            #if btnVal == 1:
            #    lap_time = t.get()
            #    print("[ThLCD] Interrupted race, time.", lap_time)
            #    state = STATE_SHOW_RESULT
           
            
        elif state == STATE_SHOW_RESULT:
            lcd.set_cursor(0,0)
            lcd.pprint("Lap time ")
            
            min, sec, mil = shared.from_mills_to_human(lap_time)
            t_s = "%d:%d.%d"%(min, sec, mil)
            lcd.set_cursor(0,1)
            lcd.pprint(t_s)
            
            print("[ThLCD] Lap Time:", min, ":", sec, ":", mil);
            if btnVal == 1: 
                state = STATE_READY
        # TODO: is this sleep value enough ??
        sleep(50)