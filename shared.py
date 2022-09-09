import queue
import timers
import threading

# the queue is used to communicate events between the lcd and the sensors and viceversa
q_evts = queue.Queue()

# TODO: pass the result among thread with value in the message or a shared variable ?
# events sent into the queue 
EVT_RACE_START  = {'id': 0}              # evt sent when the race starts
EVT_RACE_FINSIH = {'id': 1, 'v': None}   # evt sent when the race finishes with the final lap time (calculate the the cron thread)
EVT_RACE_FINSIH = {'id': 1, 'v': None}   # evt sent when the photoeletric is sensed

# convert a time in millisecons to a triple of [minutes, seconds, milliseconds]
def from_mills_to_human(mills):
    millisec  =  mills % 1000;
    tseconds = mills // 1000
    seconds = tseconds % 60
    tseconds //= 60
    minutes = tseconds % 60
    return minutes, seconds, millisec

# the critical section is both the times and the lap_time variable
#t = timers.timer()
#lap_time = 0
#tLock = threading.Lock() # thread used to lock the timers and lap_time resource