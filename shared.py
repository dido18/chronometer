import queue

# the queue is used to communicate events between the lcd and the sensors and viceversa
q_evts = queue.Queue()

# TODO: pass the result among thread with value in the message or a shared variable ?
# events sent into the queue 
EVT_RACE_START  = {'id': 0}              # evt sent when the race starts
EVT_RACE_FINSIH = {'id': 1, 'v': None}   # evt sent when the race finishes with the final lap time (calculate the the cron thread)

# convert a time in millisecons to a triple of [minutes, seconds, milliseconds]
def from_mills_to_human(mills):
    millisec  =  mills % 1000;
    tseconds = mills // 1000
    seconds = tseconds % 60
    tseconds //= 60
    minutes = tseconds % 60
    return minutes, seconds, millisec
