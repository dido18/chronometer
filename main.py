################################################################################
# RaceCrono
# A chronometer based on a photoeletric sensor for measuring the lap time.
#
################################################################################
import mcu
import t_cron 
import t_lcd

# TODO: improvements: (1) send the start time in the evt, (2) mantina the best 3 lap time into a struct and save them into DCZ

try:
    # start the thread that reads the values from the photoeletric sensor
    thread(t_cron.loop)
    sleep(50)
    
    # start the thread that shows text into LCD and read buttons values
    thread(t_lcd.loop)
    sleep(50)
    
except Exception as e:
    print(e)
    mcu.reset()