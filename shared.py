import queue

# the queue is used to communicate events between the lcd and the sensors and viceversa
q_cmds = queue.Queue()

# events sent into the queue 
EVT_RACE_START = 0   # evt sent when the race starts
EVT_RACE_FINSIH = 0  # evt sent when the race finishes


# convert a time in millisecons to a triple of [minutes, seconds, milliseconds]
def from_mills_to_human(mills):
    millisec  =  mills % 1000;
    tseconds = mills // 1000
    seconds = tseconds % 60
    tseconds //= 60
    minutes = tseconds % 60
    return minutes, seconds, millisec
