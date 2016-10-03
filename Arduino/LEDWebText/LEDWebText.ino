#include <Bridge.h>
#include <BridgeServer.h>
#include <BridgeClient.h>

const byte font[][5] = {
    {0x00,0x00,0x00,0x00,0x00},   //   0x20 32
    {0x00,0x00,0x6f,0x00,0x00},   // ! 0x21 33
    {0x00,0x07,0x00,0x07,0x00},   // " 0x22 34
    {0x14,0x7f,0x14,0x7f,0x14},   // # 0x23 35
    {0x00,0x07,0x04,0x1e,0x00},   // $ 0x24 36
    {0x23,0x13,0x08,0x64,0x62},   // % 0x25 37
    {0x36,0x49,0x56,0x20,0x50},   // & 0x26 38
    {0x00,0x00,0x07,0x00,0x00},   // ' 0x27 39
    {0x00,0x1c,0x22,0x41,0x00},   // ( 0x28 40
    {0x00,0x41,0x22,0x1c,0x00},   // ) 0x29 41
    {0x14,0x08,0x3e,0x08,0x14},   // * 0x2a 42
    {0x08,0x08,0x3e,0x08,0x08},   // + 0x2b 43
    {0x00,0x50,0x30,0x00,0x00},   // , 0x2c 44
    {0x08,0x08,0x08,0x08,0x08},   // - 0x2d 45
    {0x00,0x60,0x60,0x00,0x00},   // . 0x2e 46
    {0x20,0x10,0x08,0x04,0x02},   // / 0x2f 47
    {0x3e,0x51,0x49,0x45,0x3e},   // 0 0x30 48
    {0x00,0x42,0x7f,0x40,0x00},   // 1 0x31 49
    {0x42,0x61,0x51,0x49,0x46},   // 2 0x32 50
    {0x21,0x41,0x45,0x4b,0x31},   // 3 0x33 51
    {0x18,0x14,0x12,0x7f,0x10},   // 4 0x34 52
    {0x27,0x45,0x45,0x45,0x39},   // 5 0x35 53
    {0x3c,0x4a,0x49,0x49,0x30},   // 6 0x36 54
    {0x01,0x71,0x09,0x05,0x03},   // 7 0x37 55
    {0x36,0x49,0x49,0x49,0x36},   // 8 0x38 56
    {0x06,0x49,0x49,0x29,0x1e},   // 9 0x39 57
    {0x00,0x36,0x36,0x00,0x00},   // : 0x3a 58
    {0x00,0x56,0x36,0x00,0x00},   // ; 0x3b 59
    {0x08,0x14,0x22,0x41,0x00},   // < 0x3c 60
    {0x14,0x14,0x14,0x14,0x14},   // = 0x3d 61
    {0x00,0x41,0x22,0x14,0x08},   // > 0x3e 62
    {0x02,0x01,0x51,0x09,0x06},   // ? 0x3f 63
    {0x3e,0x41,0x5d,0x49,0x4e},   // @ 0x40 64
    {0x7e,0x09,0x09,0x09,0x7e},   // A 0x41 65
    {0x7f,0x49,0x49,0x49,0x36},   // B 0x42 66
    {0x3e,0x41,0x41,0x41,0x22},   // C 0x43 67
    {0x7f,0x41,0x41,0x41,0x3e},   // D 0x44 68
    {0x7f,0x49,0x49,0x49,0x41},   // E 0x45 69
    {0x7f,0x09,0x09,0x09,0x01},   // F 0x46 70
    {0x3e,0x41,0x49,0x49,0x7a},   // G 0x47 71
    {0x7f,0x08,0x08,0x08,0x7f},   // H 0x48 72
    {0x00,0x41,0x7f,0x41,0x00},   // I 0x49 73
    {0x20,0x40,0x41,0x3f,0x01},   // J 0x4a 74
    {0x7f,0x08,0x14,0x22,0x41},   // K 0x4b 75
    {0x7f,0x40,0x40,0x40,0x40},   // L 0x4c 76
    {0x7f,0x02,0x0c,0x02,0x7f},   // M 0x4d 77
    {0x7f,0x04,0x08,0x10,0x7f},   // N 0x4e 78
    {0x3e,0x41,0x41,0x41,0x3e},   // O 0x4f 79
    {0x7f,0x09,0x09,0x09,0x06},   // P 0x50 80
    {0x3e,0x41,0x51,0x21,0x5e},   // Q 0x51 81
    {0x7f,0x09,0x19,0x29,0x46},   // R 0x52 82
    {0x46,0x49,0x49,0x49,0x31},   // S 0x53 83
    {0x01,0x01,0x7f,0x01,0x01},   // T 0x54 84
    {0x3f,0x40,0x40,0x40,0x3f},   // U 0x55 85
    {0x0f,0x30,0x40,0x30,0x0f},   // V 0x56 86
    {0x3f,0x40,0x30,0x40,0x3f},   // W 0x57 87
    {0x63,0x14,0x08,0x14,0x63},   // X 0x58 88
    {0x07,0x08,0x70,0x08,0x07},   // Y 0x59 89
    {0x61,0x51,0x49,0x45,0x43},   // Z 0x5a 90
    {0x3c,0x4a,0x49,0x29,0x1e},   // [ 0x5b 91
    {0x02,0x04,0x08,0x10,0x20},   // \ 0x5c 92
    {0x00,0x41,0x7f,0x00,0x00},   // ] 0x5d 93
    {0x04,0x02,0x01,0x02,0x04},   // ^ 0x5e 94
    {0x40,0x40,0x40,0x40,0x40},   // _ 0x5f 95
    {0x00,0x00,0x03,0x04,0x00},   // ` 0x60 96
    {0x20,0x54,0x54,0x54,0x78},   // a 0x61 97
    {0x7f,0x48,0x44,0x44,0x38},   // b 0x62 98
    {0x38,0x44,0x44,0x44,0x20},   // c 0x63 99
    {0x38,0x44,0x44,0x48,0x7f},   // d 0x64 100
    {0x38,0x54,0x54,0x54,0x18},   // e 0x65 101
    {0x08,0x7e,0x09,0x01,0x02},   // f 0x66 102
    {0x0c,0x52,0x52,0x52,0x3e},   // g 0x67 103
    {0x7f,0x08,0x04,0x04,0x78},   // h 0x68 104
    {0x00,0x44,0x7d,0x40,0x00},   // i 0x69 105
    {0x20,0x40,0x44,0x3d,0x00},   // j 0x6a 106
    {0x00,0x7f,0x10,0x28,0x44},   // k 0x6b 107
    {0x00,0x41,0x7f,0x40,0x00},   // l 0x6c 108
    {0x7c,0x04,0x18,0x04,0x78},   // m 0x6d 109
    {0x7c,0x08,0x04,0x04,0x78},   // n 0x6e 110
    {0x38,0x44,0x44,0x44,0x38},   // o 0x6f 111
    {0x7c,0x14,0x14,0x14,0x08},   // p 0x70 112
    {0x08,0x14,0x14,0x18,0x7c},   // q 0x71 113
    {0x7c,0x08,0x04,0x04,0x08},   // r 0x72 114
    {0x48,0x54,0x54,0x54,0x20},   // s 0x73 115
    {0x04,0x3f,0x44,0x40,0x20},   // t 0x74 116
    {0x3c,0x40,0x40,0x20,0x7c},   // u 0x75 117
    {0x1c,0x20,0x40,0x20,0x1c},   // v 0x76 118
    {0x3c,0x40,0x30,0x40,0x3c},   // w 0x77 119
    {0x44,0x28,0x10,0x28,0x44},   // x 0x78 120
    {0x0c,0x50,0x50,0x50,0x3c},   // y 0x79 121
    {0x44,0x64,0x54,0x4c,0x44},   // z 0x7a 122
    {0x00,0x08,0x36,0x41,0x41},   // { 0x7b 123
    {0x00,0x00,0x7f,0x00,0x00},   // | 0x7c 124
    {0x41,0x41,0x36,0x08,0x00},   // } 0x7d 125
    {0x04,0x02,0x04,0x08,0x04},   // ~ 0x7e 126
  };

const char rowMask[7] = {0x40,0x20,0x10,0x08,0x04,0x02,0x01};
  
  // Change this to be at least as long as your pixel string (too long will work fine, just be a little slower)
#define ROWS 7
#define COLS 6
#define CHARS 22
#define PIXELS ROWS*COLS*CHARS   // Number of pixels in the string

// These values depend on which pin your string is connected to and what board you are using 
// More info on how to find these at http://www.arduino.cc/en/Reference/PortManipulation

// These values are for the pin that connects to the Data Input pin on the LED strip. They correspond to...

// Arduino Yun:     Digital Pin 8
// DueMilinove/UNO: Digital Pin 12
// Arduino MeagL    PWM Pin 4

// You'll need to look up the port/bit combination for other boards. 

// Note that you could also include the DigitalWriteFast header file to not need to to this lookup.

#define PIXEL_PORT  PORTB  // Port of the pin the pixels are connected to
#define PIXEL_DDR   DDRB   // Port of the pin the pixels are connected to
#define PIXEL_BIT   4      // Bit of the pin the pixels are connected to

// These are the timing constraints taken mostly from the WS2812 datasheets 
// These are chosen to be conservative and avoid problems rather than for maximum throughput 

#define T1H  900    // Width of a 1 bit in ns
#define T1L  600    // Width of a 1 bit in ns

#define T0H  400    // Width of a 0 bit in ns
#define T0L  900    // Width of a 0 bit in ns

#define RES 6000    // Width of the low gap between bits to cause a frame to latch

// Here are some convience defines for using nanoseconds specs to generate actual CPU delays

#define NS_PER_SEC (1000000000L)          // Note that this has to be SIGNED since we want to be able to check for negative values of derivatives

#define CYCLES_PER_SEC (F_CPU)

#define NS_PER_CYCLE ( NS_PER_SEC / CYCLES_PER_SEC )

#define NS_TO_CYCLES(n) ( (n) / NS_PER_CYCLE )

// Actually send a bit to the string. We must to drop to asm to enusre that the complier does
// not reorder things and make it so the delay happens in the wrong place.

inline void sendBit( bool bitVal ) {
  
    if (  bitVal ) {        // 0 bit
      
    asm volatile (
      "sbi %[port], %[bit] \n\t"        // Set the output bit
      ".rept %[onCycles] \n\t"                                // Execute NOPs to delay exactly the specified number of cycles
      "nop \n\t"
      ".endr \n\t"
      "cbi %[port], %[bit] \n\t"                              // Clear the output bit
      ".rept %[offCycles] \n\t"                               // Execute NOPs to delay exactly the specified number of cycles
      "nop \n\t"
      ".endr \n\t"
      ::
      [port]    "I" (_SFR_IO_ADDR(PIXEL_PORT)),
      [bit]   "I" (PIXEL_BIT),
      [onCycles]  "I" (NS_TO_CYCLES(T1H) - 2),    // 1-bit width less overhead  for the actual bit setting, note that this delay could be longer and everything would still work
      [offCycles]   "I" (NS_TO_CYCLES(T1L) - 2)     // Minimum interbit delay. Note that we probably don't need this at all since the loop overhead will be enough, but here for correctness

    );
                                  
    } else {          // 1 bit

    // **************************************************************************
    // This line is really the only tight goldilocks timing in the whole program!
    // **************************************************************************


    asm volatile (
      "sbi %[port], %[bit] \n\t"        // Set the output bit
      ".rept %[onCycles] \n\t"        // Now timing actually matters. The 0-bit must be long enough to be detected but not too long or it will be a 1-bit
      "nop \n\t"                                              // Execute NOPs to delay exactly the specified number of cycles
      ".endr \n\t"
      "cbi %[port], %[bit] \n\t"                              // Clear the output bit
      ".rept %[offCycles] \n\t"                               // Execute NOPs to delay exactly the specified number of cycles
      "nop \n\t"
      ".endr \n\t"
      ::
      [port]    "I" (_SFR_IO_ADDR(PIXEL_PORT)),
      [bit]   "I" (PIXEL_BIT),
      [onCycles]  "I" (NS_TO_CYCLES(T0H) - 2),
      [offCycles] "I" (NS_TO_CYCLES(T0L) - 2)

    );
      
    }
    
    // Note that the inter-bit gap can be as long as you want as long as it doesn't exceed the 5us reset timeout (which is A long time)
    // Here I have been generous and not tried to squeeze the gap tight but instead erred on the side of lots of extra time.
    // This has thenice side effect of avoid glitches on very long strings becuase 

    
}  

  
inline void sendByte( unsigned char byte ) {
    
    for( unsigned char bit = 0 ; bit < 8 ; bit++ ) {
      
      sendBit( bitRead( byte , 7 ) );                // Neopixel wants bit in highest-to-lowest order
                                                     // so send highest bit (bit #7 in an 8-bit byte since they start at 0)
      byte <<= 1;                                    // and then shift left so bit 6 moves into 7, 5 moves into 6, etc
      
    }           
} 

/*

  The following three functions are the public API:
  
  ledSetup() - set up the pin that is connected to the string. Call once at the begining of the program.  
  sendPixel( r g , b ) - send a single pixel to the string. Call this once for each pixel in a frame.
  show() - show the recently sent pixel on the LEDs . Call once per frame. 
  
*/

int hexToInt(const String & str)
{
  int value;
  value = 0;
  for (int i=0; i<str.length(); i++) {
    if (str[i]>='0' && str[i]<= '9') {
      value = (value << 4) + (str[i]-'0');
    } else if (str[i]>='A' && str[i]<= 'F') {
      value = (value << 4) + (str[i]-'A'+10);
    } else if (str[i]>='a' && str[i]<= 'f') {
      value = (value << 4) + (str[i]-'a'+10);
    } else {
      value = value << 4;
    }
  }
  return value;
}


struct ledTextChar {
      char  ch;
      byte  red;
      byte  green;
      byte  blue;
};

class ledText {
  public:
    int numChar;
    struct ledTextChar text[150];

  public:
    ledText();
    void clear() 
      { numChar = 0; };
    int length()
      { return numChar; };
    ledTextChar & operator[] (int i);
    void addText(const String & str, int start, byte r, byte g, byte b);
    void addChar(char ch, byte r, byte g, byte b);
    void parseText(const String & str, int start);
} ;

ledText::ledText()
{
  numChar = 0;
  text[0].ch = '?';
  text[0].red = 10; text[0].green = 10; text[0].blue = 10;
}

struct ledTextChar & ledText::operator[] (int i) 
{
  if (i<0 || i>numChar ) {
    return text[0];
  } else {
    return text[i+1];
  }
}

void ledText::addText(const String & str, int start, byte r, byte g, byte b)
{
  for (int i=start; i<str.length() && numChar<sizeof text; i++) {
    addChar(str[i], r, g, b);
  }
}


void ledText::addChar(char ch, byte r, byte g, byte b)
{
  if (numChar<sizeof text) {
    numChar++;
    text[numChar].ch = ch;
    text[numChar].red = r;
    text[numChar].green = g;
    text[numChar].blue = b;
  }
}

void ledText::parseText(const String & str, int start)
{
  char  ch;
  byte r, g, b;
  int br;
  String value;
  r = 10; b = 10; g = 10;
  for (int i=start; i<str.length(); i++) {
    ch = str[i];
    if (ch == '~') {
      if (i+9<=str.length()) {
         r = hexToInt(str.substring(i+1, i+3));
         g = hexToInt(str.substring(i+3, i+5));
         b = hexToInt(str.substring(i+5, i+7));
         br = hexToInt(str.substring(i+7, i+9));
         r = (byte)((((long)r) * br)>>8);
         g = (byte)((((long)g) * br)>>8);
         b = (byte)((((long)b) * br)>>8);
      }
      i+=8;
    } else {
       addChar(ch, r, g, b);  
    }
  }
}

String cmdStr;
//char cmdColor;
//char cmdInt;
//String cmdText;
long cmdIteration;
ledText  cmdLedText;
bool cmdDisplayed = true;

void ledSetup() {
  
  bitSet( PIXEL_DDR , PIXEL_BIT );
  
}

inline void sendPixel( unsigned char r, unsigned char g , unsigned char b )  {  
  
  sendByte(g);          // Neopixel wants colors in green then red then blue order
  sendByte(r);
  sendByte(b);
  
}


// Just wait long enough without sending any bots to cause the pixels to latch and display the last sent frame

void show() {
  _delay_us( (RES / 1000UL) + 1);       // Round up since the delay must be _at_least_ this long (too short might not work, too long not a problem)
}

void showColor( unsigned char r , unsigned char g , unsigned char b ) {
  
  cli();  
  for( int p=0; p<PIXELS; p++ ) {
    sendPixel( r , g , b );
  }
  sei();
  show();
  
}


void convertColor (char color, char br, byte &r, byte &g, byte &b) 
{
    int in;
    in = 20;
    if (br == '0') in = 25; 
    if (br == '1') in = 50; 
    if (br == '2') in = 75; 
    if (br == '3') in = 100; 
    if (br == '4') in = 125; 
    if (br == '5') in = 150; 
    if (br == '6') in = 175; 
    if (br == '7') in = 200; 
    if (br == '8') in = 225; 
    if (br == '9') in = 250; 
    if (color == 'R') {
      r = in; g = 0; b = 0;
    } else if (color == 'G') {
      r = 0; g = in; b = 0;
    } else if (color == 'B') {
      r = 0; g = 0; b = in;
    } else if (color == 'Y') {
      r = in/2; g = in/2; b = 0;
    } else if (color == 'O') {
      r = in/2; g = in/4; b = 0;
    } else if (color == 'V') {
      r = in/3; g = 0; b = in/2;
    } else if (color == 'W') {
      r = in; g = in; b = in;
    } else {
      r = in/3; g = in/3; b = in/3;
    }
}

/*  
int ledTextDisplay2 (const String & str) {
  char ch;
  int p;
  byte r, g, b;

  int offset, chbeg, colbeg, chcur, colcur;
  convertTextColor(cmdColor, cmdInt, r, g, b);
  
  offset = cmdIteration++;
  if (cmdIteration >= (str.length()+3)*COLS) cmdIteration = 0;
    chbeg = offset/COLS;
    colbeg = offset-(chbeg*COLS);
    p = 0;

    cli();
    for (int row=ROWS-1; row>=0; row--) {
      if ((row&1)) {
        chcur = chbeg;
        colcur = colbeg;
        for(int idx=0; idx<CHARS*COLS; idx++) {
          if (chcur < str.length()) {
            ch = str[chcur];
            if (ch<32 || ch>126) ch = ' ';
          } else if (chcur >= str.length()+3 && str.length() > CHARS) {
            ch = str[chcur-str.length()-3];
            if (ch<32 || ch>126) ch = ' ';
          } else {
            ch = ' ';
          }
          if (colcur < COLS-1) {
              if (font[ch-32][colcur]&rowMask[row]) {
                sendPixel(r,g,b);
              } else {
                sendPixel(0,0,0);
              }
          } else {
            sendPixel(0,0,0);
          }
          if (++colcur >= COLS) {
            colcur = 0;
            chcur++;
          }
        }
      } else {
        chcur = chbeg + CHARS;
        colcur = colbeg;
        for(int idx=0; idx<CHARS*COLS; idx++) {
          if (--colcur < 0) {
            colcur = COLS-1;
            chcur--;
          }
          if (chcur < str.length()) {
            ch = str[chcur];
            if (ch<32 || ch>126) ch = ' ';
          } else if (chcur >= str.length()+3 && str.length() > CHARS) {
            ch = str[chcur-str.length()-3];
            if (ch<32 || ch>126) ch = ' ';
          } else {
            ch = ' ';
          }
          if (colcur < COLS-1) {
              if (font[ch-32][colcur]&rowMask[row]) {
                sendPixel(r,g,b);
              } else {
                sendPixel(0,0,0);
              }
          } else {
            sendPixel(0,0,0);
          }
        }
      }
    }
    sei();
    show();
    delay(1);
    if (str.length() <= CHARS) cmdStr = "";
    //if (offset == 0) delay(500);
  //}
  return 0;
}
*/

int ledTextDisplay (/*ledText & text*/) {
  char ch;
  byte r, g, b;
  ledText & text = cmdLedText;

  int offset, chbeg, colbeg, chcur, colcur, chIdx;
  
  offset = cmdIteration++;
  if (cmdIteration >= (text.length()+3)*COLS) {
    cmdIteration = 0;
    cmdDisplayed = true;
  }

    chbeg = offset/COLS;
    colbeg = offset-(chbeg*COLS);

    cli();
    for (int row=ROWS-1; row>=0; row--) {
      if ((row&1)) {
        chcur = chbeg;
        colcur = colbeg;
        for(int idx=0; idx<CHARS*COLS; idx++) {
          if (chcur < text.length()) {
            chIdx = chcur;
            ch = text[chIdx].ch;
            if (ch<32 || ch>126) ch = ' ';
          } else if (chcur >= text.length()+3 && text.length() > CHARS) {
            chIdx = chcur-text.length()-3;
            ch = text[chIdx].ch;
            if (ch<32 || ch>126) ch = ' ';
          } else {
            chIdx = -1;
            ch = ' ';
          }

          if (colcur < COLS-1) {
              if (font[ch-32][colcur]&rowMask[row]) {
                sendPixel(text[chIdx].red,text[chIdx].green,text[chIdx].blue);
              } else {
                sendPixel(0,0,0);
              }
          } else {
            sendPixel(0,0,0);
          }
          if (++colcur >= COLS) {
            colcur = 0;
            chcur++;
          }
        }
      } else {
        chcur = chbeg + CHARS;
        colcur = colbeg;
        for(int idx=0; idx<CHARS*COLS; idx++) {
          if (--colcur < 0) {
            colcur = COLS-1;
            chcur--;
          }
          if (chcur < text.length()) {
            chIdx = chcur;
            ch = text[chIdx].ch;
            if (ch<32 || ch>126) ch = ' ';
          } else if (chcur >= text.length()+3 && text.length() > CHARS) {
            chIdx = chcur - text.length() - 3;
            ch = text[chIdx].ch;
            if (ch<32 || ch>126) ch = ' ';
          } else {
            chIdx = -1;
            ch = ' ';
          }
          if (colcur < COLS-1) {
              if (font[ch-32][colcur]&rowMask[row]) {
                sendPixel(text[chIdx].red,text[chIdx].green,text[chIdx].blue);
              } else {
                sendPixel(0,0,0);
              }
          } else {
            sendPixel(0,0,0);
          }
        }
      }
    }
    sei();
    show();
    delay(1);
    if (text.length() <= CHARS) {
      cmdStr = "";
      cmdDisplayed = true;
      delay(2000);
    }
    //if (offset == 0) delay(500);
  //}
  return 0;
}
// Listen to the default port 5555, the Yún webserver
// will forward there all the HTTP requests you send
BridgeServer server;
#define PIN 8

void setup() {
  // Bridge startup
  pinMode(13, OUTPUT);
  digitalWrite(13, LOW);
  Bridge.begin();
  digitalWrite(13, HIGH);
  //Console.begin();
  //while (!Console) ;

  ledSetup();
  // Listen for incoming connection only from localhost
  // (no one from the external network could connect)
  server.listenOnLocalhost();
  server.begin();

  showColor(0,0,0);

  cmdStr = "text";
  //cmdText = "";
  //cmdColor = 'B';
  //cmdInt = '2';
  cmdLedText.clear();
  //cmdLedText.addText("DET vs. COL 11:00 PM be there now 2",10,0,0);
  //cmdLedText.parseText("~FF000010DET~FFFFFF10 vs. ~0000FF10COL~FFFFFF10 11:00 PM");
  cmdLedText.parseText("~FF000008system init", 0);
  cmdDisplayed = false;
}

void loop() {
  String url;
  // Get clients coming from server
  digitalWrite(13, LOW);
  if (cmdDisplayed) {
    //if (lastStatus != cmdDisplayed) Bridge.put("displayed","1");
    BridgeClient client = server.accept();

    if (client) {
      // Process request
      url = client.readString();
      cmdParse(url);
  
      // Close connection and free resources.
      client.stop();
    }
  }
  cmdDisplay();
  digitalWrite(13, HIGH);
}


void cmdParse(String & url) {
  // read the command
  String command;
  int len;
  char ch;

  int beg, pos;
  beg = 0;
  if (url.length() > 0) {
    beg = 0;
    pos = url.indexOf('/',beg);
    if (pos < 0) pos = url.length();
    command = url.substring(beg,pos);

    // is "mode" command?
    if (command == "clear") {
      cmdStr = "text";
      cmdLedText.clear();
      cmdIteration = 0;
    } else if (command == "text2") {
      cmdStr = "text";
      byte r, g, b;
      if (url.length() >= pos+3) {
        convertColor(url[pos+1], url[pos+2], r, g, b);
      } else {
        r = 30; g = 30; b = 30;
      }
      cmdLedText.clear();
      cmdLedText.addText(url,pos+3, r, g, b);
      cmdIteration = 0;
      cmdDisplayed = false;
  //} else if (command == "text3") {
  //    cmdStr = "text3";
  //    int r, g, b;
  //    if (options.length() >= 2) {
  //      cmdColor = options[0];
  //      cmdInt = options[1];
  //      cmdText = options.substring(2);
  //    } else {
  //      //cmdColor = 'R';
  //      //cmdInt = '1';
  //      //cmdText = "Empty";
  //    }
  //    cmdIteration = 0;
    } else if (command == "text") {
      cmdStr = "text";
      cmdLedText.clear();
      cmdLedText.parseText(url,pos+1);
      cmdIteration = 0;
      cmdDisplayed = false;
    }
  }
}


void cmdDisplay() {
  // is "mode" command?
  if (cmdStr == "text") {
    ledTextDisplay();
  //} else if (cmdStr == "text3") {
  //  ledTextDisplay2(cmdText);
  } 
}



