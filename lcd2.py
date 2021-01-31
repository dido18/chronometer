import i2c

# 40 caratteri, 2 righe, buffer circolare

# commands
LCD_CLEARDISPLAY    = 0x01
LCD_RETURNHOME      = 0x02
LCD_ENTRYMODESET    = 0x04
LCD_DISPLAYCONTROL  = 0x08
LCD_CURSORSHIFT     = 0x10
LCD_FUNCTIONSET     = 0x20
LCD_SETCGRAMADDR    = 0x40
LCD_SETDDRAMADDR    = 0x80

# flags for display entry mode
LCD_ENTRYRIGHT          = 0x00
LCD_ENTRYLEFT           = 0x02
LCD_ENTRYSHIFTINCREMENT = 0x01
LCD_ENTRYSHIFTDECREMENT = 0x00

# flags for display on/off control
LCD_DISPLAYON   = 0x04
LCD_DISPLAYOFF  = 0x00
LCD_CURSORON    = 0x02
LCD_CURSOROFF   = 0x00
LCD_BLINKON     = 0x01
LCD_BLINKOFF    = 0x00

# flags for display/cursor shift
LCD_DISPLAYMOVE = 0x08
LCD_CURSORMOVE  = 0x00
LCD_MOVERIGHT   = 0x04
LCD_MOVELEFT    = 0x00

# flags for function set
LCD_8BITMODE    = 0x10
LCD_4BITMODE    = 0x00
LCD_2LINE       = 0x08
LCD_1LINE       = 0x00
LCD_5x10DOTS    = 0x04
LCD_5x8DOTS     = 0x00


# flags for backlight control
LCD_BACKLIGHT   = 0x08
LCD_NOBACKLIGHT = 0x00


En  = 0b00000100
Rw  = 0b00000010
Rs  = 0b00000001



class LCD(i2c.I2C):
    def __init__(self, i2cdrv, lcd_cols=16, lcd_rows=2, charsize= LCD_5x8DOTS ,addr=0x27, clk=100000):
        i2c.I2C.__init__(self, i2cdrv, addr, clk)
        
        self._addr = addr
        self._cols = lcd_cols
        self._rows = lcd_rows
        self._charsize = charsize
        self._backlightval = LCD_BACKLIGHT
        
        i2c.I2C.start(self)
        # print("start ok")
        self._displayfunction = LCD_4BITMODE | LCD_1LINE | LCD_5x8DOTS
#   _displayfunction = LCD_4BITMODE | LCD_1LINE | LCD_5x8DOTS;
        
        if self._rows > 1:
            self._displayfunction |= LCD_2LINE
#   if (_rows > 1) {
#       _displayfunction |= LCD_2LINE;
#   }
        
        if (self._charsize != 0) and (self._rows == 1):
            self._displayfunction |= LCD_5x10DOTS
#   // for some 1 line displays you can select a 10 pixel high font
#   if ((_charsize != 0) && (_rows == 1)) {
#       _displayfunction |= LCD_5x10DOTS;
#   }
        
        sleep(80)
#   // SEE PAGE 45/46 FOR INITIALIZATION SPECIFICATION!
#   // according to datasheet, we need at least 40ms after power rises above 2.7V
#   // before sending commands. Arduino can turn on way befer 4.5V so we'll wait 50
#   delay(50);

        
        self._expander_write(self._backlightval)
#   // Now we pull both RS and R/W low to begin commands
#   expanderWrite(_backlightval);   // reset expanderand turn backlight off (Bit 8 =1)
        # print("init 1")
        sleep(1000)
#   delay(1000);

        self.write4bits(0x03 << 4)
        sleep(5)
        
#   //put the LCD into 4 bit mode
#   // this is according to the hitachi HD44780 datasheet
#   // figure 24, pg 46

#   // we start in 8bit mode, try to set 4 bit mode
#   write4bits(0x03 << 4);
#   delayMicroseconds(4500); // wait min 4.1ms
        
        self.write4bits(0x03 << 4)
        sleep(5)
        
#   // second try
#   write4bits(0x03 << 4);
#   delayMicroseconds(4500); // wait min 4.1ms
        
        self.write4bits(0x03 << 4)
        sleep(1)
        
#   // third go!
#   write4bits(0x03 << 4);
#   delayMicroseconds(150);
        
        self.write4bits(0x02 << 4)
        
#   // finally, set to 4-bit interface
#   write4bits(0x02 << 4);
        
        self.command(LCD_FUNCTIONSET | self._displayfunction)
#   // set # lines, font size, etc.
#   command(LCD_FUNCTIONSET | _displayfunction);

        self._displaycontrol = LCD_DISPLAYON | LCD_CURSOROFF | LCD_BLINKOFF
#   // turn the display on with no cursor or blinking default
#   _displaycontrol = LCD_DISPLAYON | LCD_CURSOROFF | LCD_BLINKOFF;
    
        self.enable_display()
#   display();
        
        self.clear()
#   // clear it off
#   clear();

        self._displaymode = LCD_ENTRYLEFT | LCD_ENTRYSHIFTDECREMENT
#   // Initialize to default text direction (for roman languages)
#   _displaymode = LCD_ENTRYLEFT | LCD_ENTRYSHIFTDECREMENT;
        
        self.command(LCD_ENTRYMODESET | self._displaymode)
#   // set the entry mode
#   command(LCD_ENTRYMODESET | _displaymode);
        
        self.home()
#   home();

    def clear(self):
        self.command(LCD_CLEARDISPLAY)
        sleep(3)
    
# /********** high level commands, for the user! */
# void LiquidCrystal_I2C::clear(){
#   command(LCD_CLEARDISPLAY);// clear display, set cursor position to zero
#   delayMicroseconds(2000);  // this command takes a long time!
# }

    def home(self):
        self.command(LCD_RETURNHOME)
        sleep(3)
# void LiquidCrystal_I2C::home(){
#   command(LCD_RETURNHOME);  // set cursor position to zero
#   delayMicroseconds(2000);  // this command takes a long time!
# }
    
    def set_cursor(self, col, row):
        row_offsets = [ 0x00, 0x40, 0x14, 0x54]
        if row > self._rows:
            row = self._rows-1
        self.command(LCD_SETDDRAMADDR | (col + row_offsets[row]))
# void LiquidCrystal_I2C::setCursor(uint8_t col, uint8_t row){
#   int row_offsets[] = { 0x00, 0x40, 0x14, 0x54 };
#   if (row > _rows) {
#       row = _rows-1;    // we count rows starting w/0
#   }
#   command(LCD_SETDDRAMADDR | (col + row_offsets[row]));
# }

    def disable_display(self):
        self._displaycontrol &= ~LCD_DISPLAYON
        self.command(LCD_DISPLAYCONTROL | self._displaycontrol)
# // Turn the display on/off (quickly)
# void LiquidCrystal_I2C::noDisplay() {
#   _displaycontrol &= ~LCD_DISPLAYON;
#   command(LCD_DISPLAYCONTROL | _displaycontrol);
# }

    def enable_display(self):
        self._displaycontrol |= LCD_DISPLAYON
        self.command(LCD_DISPLAYCONTROL | self._displaycontrol)
# void LiquidCrystal_I2C::display() {
#   _displaycontrol |= LCD_DISPLAYON;
#   command(LCD_DISPLAYCONTROL | _displaycontrol);
# }

    def disable_cursor(self):
        self._displaycontrol &= ~LCD_CURSORON
        self.command(LCD_DISPLAYCONTROL | self._displaycontrol)
# // Turns the underline cursor on/off
# void LiquidCrystal_I2C::noCursor() {
#   _displaycontrol &= ~LCD_CURSORON;
#   command(LCD_DISPLAYCONTROL | _displaycontrol);
# }

    def enable_cursor(self):
        self._displaycontrol |= LCD_CURSORON
        self.command(LCD_DISPLAYCONTROL | self._displaycontrol)
# void LiquidCrystal_I2C::cursor() {
#   _displaycontrol |= LCD_CURSORON;
#   command(LCD_DISPLAYCONTROL | _displaycontrol);
# }

    def disable_blink(self):
        self._displaycontrol &= ~LCD_BLINKON
        self.command(LCD_DISPLAYCONTROL | self._displaycontrol)
# // Turn on and off the blinking cursor
# void LiquidCrystal_I2C::noBlink() {
#   _displaycontrol &= ~LCD_BLINKON;
#   command(LCD_DISPLAYCONTROL | _displaycontrol);
# }

    def enable_blink(self):
        self._displaycontrol |= LCD_BLINKON
        self.command(LCD_DISPLAYCONTROL | self._displaycontrol)
# void LiquidCrystal_I2C::blink() {
#   _displaycontrol |= LCD_BLINKON;
#   command(LCD_DISPLAYCONTROL | _displaycontrol);
# }


    def scroll_display_left(self):
        self.command(LCD_CURSORSHIFT | LCD_DISPLAYMOVE | LCD_MOVELEFT)
# // These commands scroll the display without changing the RAM
# void LiquidCrystal_I2C::scrollDisplayLeft(void) {
#   command(LCD_CURSORSHIFT | LCD_DISPLAYMOVE | LCD_MOVELEFT);
# }

    def scroll_display_right(self):
        self.command(LCD_CURSORSHIFT | LCD_DISPLAYMOVE | LCD_MOVERIGHT)
# void LiquidCrystal_I2C::scrollDisplayRight(void) {
#   command(LCD_CURSORSHIFT | LCD_DISPLAYMOVE | LCD_MOVERIGHT);
# }


    def left_to_right(self):
        self._displaymode |= LCD_ENTRYLEFT
        self.command(LCD_ENTRYMODESET | self._displaymode)
# // This is for text that flows Left to Right
# void LiquidCrystal_I2C::leftToRight(void) {
#   _displaymode |= LCD_ENTRYLEFT;
#   command(LCD_ENTRYMODESET | _displaymode);
# }

    def right_to_left(self):
        self._displaymode &= ~LCD_ENTRYLEFT
        self.command(LCD_ENTRYMODESET | self._displaymode)
# // This is for text that flows Right to Left
# void LiquidCrystal_I2C::rightToLeft(void) {
#   _displaymode &= ~LCD_ENTRYLEFT;
#   command(LCD_ENTRYMODESET | _displaymode);
# }

    def enable_autoscroll(self):
        self._displaymode |= LCD_ENTRYSHIFTINCREMENT
        self.command(LCD_ENTRYMODESET | self._displaymode)
# // This will 'right justify' text from the cursor
# void LiquidCrystal_I2C::autoscroll(void) {
#   _displaymode |= LCD_ENTRYSHIFTINCREMENT;
#   command(LCD_ENTRYMODESET | _displaymode);
# }

    def disable_autoscroll(self):
        self._displaymode &= ~LCD_ENTRYSHIFTINCREMENT
        self.command(LCD_ENTRYMODESET | self._displaymode)
# // This will 'left justify' text from the cursor
# void LiquidCrystal_I2C::noAutoscroll(void) {
#   _displaymode &= ~LCD_ENTRYSHIFTINCREMENT;
#   command(LCD_ENTRYMODESET | _displaymode);
# }

    def create_char(self, location, charmap):
        location &= 0x7
        self.command(LCD_SETCGRAMADDR | (location << 3))
        for c in charmap:
            self._write(c)
# // Allows us to fill the first 8 CGRAM locations
# // with custom characters
# void LiquidCrystal_I2C::createChar(uint8_t location, uint8_t charmap[]) {
#   location &= 0x7; // we only have 8 locations 0-7
#   command(LCD_SETCGRAMADDR | (location << 3));
#   for (int i=0; i<8; i++) {
#       write(charmap[i]);
#   }
# }
    
    
    
    def disable_backlight(self):
        self._backlightval = LCD_NOBACKLIGHT
        self._expander_write(0)
    
# // Turn the (optional) backlight off/on
# void LiquidCrystal_I2C::noBacklight(void) {
#   _backlightval=LCD_NOBACKLIGHT;
#   expanderWrite(0);
# }

    def enable_backlight(self):
        self._backlightval = LCD_BACKLIGHT
        self._expander_write(0)
# void LiquidCrystal_I2C::backlight(void) {
#   _backlightval=LCD_BACKLIGHT;
#   expanderWrite(0);
# }

    def get_backlight(self):
        return self._backlightval == LCD_BACKLIGHT
# bool LiquidCrystal_I2C::getBacklight() {
#   return _backlightval == LCD_BACKLIGHT;
# }
    
    
    


    def command(self, value):
        self.send(value, 0)
# inline void LiquidCrystal_I2C::command(uint8_t value) {
#   send(value, 0);
# }
    
    
    def _write(self, value):
        self.send(value, Rs)
# inline size_t LiquidCrystal_I2C::write(uint8_t value) {
#   send(value, Rs);
#   return 1;
# }


# /************ low level data pushing commands **********/
    def send(self, value, mode):
        high = value & 0xf0
        low = (value << 4) & 0xf0
        self.write4bits(high|mode)
        self.write4bits(low|mode)
# // write either command or data
# void LiquidCrystal_I2C::send(uint8_t value, uint8_t mode) {
#   uint8_t highnib=value&0xf0;
#   uint8_t lownib=(value<<4)&0xf0;
#   write4bits((highnib)|mode);
#   write4bits((lownib)|mode);
# }

    def write4bits(self, value):
        self._expander_write(value)
        self.pulseEnable(value)
# void LiquidCrystal_I2C::write4bits(uint8_t value) {
#   expanderWrite(value);
#   pulseEnable(value);
# }

    def _expander_write(self, data):
        a = data | self._backlightval
        self.write(a)
# void LiquidCrystal_I2C::expanderWrite(uint8_t _data){
#   Wire.beginTransmission(_addr);
#   Wire.write((int)(_data) | _backlightval);
#   Wire.endTransmission();
# }
    
    def pulseEnable(self, data):
        self._expander_write(data | En)
        sleep(1)
        self._expander_write(data & ~En)
        sleep(1)
# void LiquidCrystal_I2C::pulseEnable(uint8_t _data){
#   expanderWrite(_data | En);  // En high
#   delayMicroseconds(1);       // enable pulse must be >450ns

#   expanderWrite(_data & ~En); // En low
#   delayMicroseconds(50);      // commands need > 37us to settle
# }
    def print_string(self, s):
        for ch in s:
            self._write(ord(ch))
        # print("mprint", s)
        # a = [ord(e) for e in s]
        # print(a)
        # self.write(a)
    
    # def print_bytes(self, b):
    #   if
    def _print_str(self, s):
        for ch in s:
            self._write(ord(ch))

    def _print_bytes(self, buf):
        for b in buf:
            self._write(b)

    def _print(self, obj):
        t = type(obj)
        if t == PSTRING:
            self._print_str(obj)
        elif t >= PBYTES and t <= PSHORTARRAY:
            self._print_bytes(obj)
        elif t <= PINTEGER:
            self._write(obj)
        else:
            self._print_str(str(obj))
            # raise TypeError

    def pprint(self, *args, sep=' '):
        l = len(args)
        for i in range(l-1):
            self._print(args[i])
            self._print(sep)

        if l:
            self._print(args[-1])
