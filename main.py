################################################################################
# PhotoEletric lap Time
#
################################################################################
import mcu
import t_cron 
import t_lcd

try:
    # start the thread that reads the values from the photoeletric sensor
    thread(t_cron.loop)
    sleep(50)
    
    # start the thread that show text into LCD
    thread(t_lcd.loop)
    sleep(50)
    
except Exception as e:
    print(e)
    mcu.reset()