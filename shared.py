import queue

# commands received in the queue
CMD_OBJ_PRESENCE = 0   # an object has been sensed
#CMD_OBJ_ABSEMCE  = 1  # no object has 

# queue of commands used to exchange cmd between sensors and lcd
q_cmds = queue.Queue()

# convert a time in millisecons to a triple of [minutes, seconds, milliseconds]
def from_mills_to_human(mills):
    millisec  =  mills % 1000;
    tseconds = mills // 1000
    seconds = tseconds % 60
    tseconds //= 60
    minutes = tseconds % 60
    return minutes, seconds, millisec
