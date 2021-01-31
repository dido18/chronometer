import shared
import streams
import lcd2
import timers

streams.serial()

# states of the FSM
__define(STATE_READY ,          0x0)
#__define(S_INVALID ,        0x1)
__define(STATE_GO,              0x2)
__define(STATE_ARRIVED,         0x3)


PRESSED = LOW # the button is pressed if LOW

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
        

def loop():
    # INIT LCD
    init_lcd()
    print("LCD init")
    
    # set initial state
    state        = STATE_READY
    lap_time     = 0        # store the lap time in milliseconds
    elapsed_time = 0        # store the elaspsed time in milliseconds
    
    # timer used to calculate the time of each lap and elapsed time
    t = timers.timer()
    
    while True:
        btnResetV = digitalRead(bntReset)
        
        cmd = None
        try:
            print("[ThLCD] waiting ...")
            cmd = shared.q_cmds.get(timeout=1000)
        except QueueEmpty as e:
            pass
        except Exception as e:
            print(e)    
       
        if state == STATE_READY:
            lcd.clear()
            lcd.pprint("ready...")
            if cmd == shared.CMD_OBJ_PRESENCE:
                print("[ThLCD] new object") 
                t.start()
                state = STATE_GO

        elif state == STATE_GO:
            elapsed_time = t.get()
            s = elapsed_time // 1000
            print("[ThLCD] Elapsed time:", s,"(s)")
            lcd.clear()
            lcd.pprint("%d"%(s))
            if cmd == shared.CMD_OBJ_PRESENCE:
                print("[ThLCD] arrived") 
                t.start()
                state = STATE_ARRIVED
                lap_time = elapsed_time
        elif state == STATE_ARRIVED:
            lcd.set_cursor(0,0)
            lcd.pprint("time ")
            
            min, sec, mil = shared.from_mills_to_human(lap_time)
            t_s = "%d:%d.%d"%(min, sec, mil)
            lcd.set_cursor(0,1)
            lcd.pprint(t_s)
            
            print("[ThLCD] Lap Time:", min, ":", sec, ":", mil);
            if btnResetV == 1: 
                state = STATE_READY
        sleep(50)