################################################################################
# RaceCrono Project
# A chronometer based on a photoeletric sensor for measuring the a lap time.
#
################################################################################
import mcu
import streams
import t_cron 
import t_lcd

# TODO: improvements: 
# (1) send the start time in the evt 
# (2) mantinas the best 3 laps time into a struct and save them into DCZ

streams.serial()


try:
    # start the thread that reads the values from the photoeletric sensor
    thread(t_cron.loop)
    sleep(500)    
    #start the thread that shows text into LCD and read buttons values
    thread(t_lcd.loop)
    sleep(500)

    while True:
        sleep(1000)
        
except Exception as e:
    print("Exception")
    print(e)
    mcu.reset()