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

# 5 leds for start sequence 
ledPin0   = D23
ledPin1   = D22
ledPin2   = D1
ledPin3   = D3
ledPin4   = D21
ledPins   = [ledPin0, ledPin1, ledPin2, ledPin3, ledPin4]

for ld in ledPins:
    pinMode(ld, OUTPUT)
print("Leds initialised")

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

# perform the countdown sequence before the start
def countdown_sequence():
    global lcd
    lcd.clear()
    for led in ledPins:
        digitalWrite(led, HIGH)
    for col in range(0, 5, 1):
        lcd.set_cursor(col, 0)
        lcd.pprint("#")
        sleep(1000)
        print("Led on ", ledPins[col])
        digitalWrite(ledPins[col], LOW)   # turn the LED OFF by setting the voltage LOW
        
    lcd.clear()
    # play a sound to the buzzer

def loop():
    init_lcd()
    print("LCD initialized")
    
    # set initial state
    state        = STATE_READY
    lap_time     = 0        # store the lap time in milliseconds
    
    # only used to show the elapsed time. The real lap time is calucalated in a separated thread.
    et = timers.timer()
    
    while True:
        btnVal = digitalRead(bntReset)
        evt = None
        if state == STATE_READY:
            lcd.clear()
            lcd.pprint("Ready ")
            if btnVal == 1: 
                countdown_sequence()
                # TODO: here it can be some delay (order of centiseconds) from the end of the count down and when the evt reach the other thread
                # Maybe pass the start time in the EVT_RACE_START event ??
                print("[ThLCD] put START before"),

                shared.q_evts.put(shared.EVT_RACE_START)
                print("[ThLCD] put START after")
                et.start()
                print("[ThLCD] time started")
                state = STATE_SHOW_ELAPSED
                print("[ThLCD] setted state", state)

        elif state == STATE_SHOW_ELAPSED:
            elapsed_time = et.get()
            print("[ThLCD] elapsed_time", elapsed_time)
            min, sec, mil = shared.from_mills_to_human(elapsed_time)
            t_s = "%d:%d.%d"%(min, sec, mil)
            lcd.clear()
            lcd.pprint(t_s)
            print("[ThLCD] Elapsed time:", t_s)
            try:
                # TODO: how to define correct timeout values of the get ???
                evt = shared.q_evts.get(timeout=500)
                if evt['id'] == shared.EVT_RACE_FINSIH['id']:
                    lap_time = evt['v']
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
            
            if btnVal == 1: 
                state = STATE_READY
        # TODO: is this sleep value enough ??
        sleep(50)