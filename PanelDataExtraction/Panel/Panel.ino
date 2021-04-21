#include <LiquidCrystal.h>

///Pins
#define RS 2
#define EN 3
#define D4 9
#define D5 10
#define D6 11
#define D7 12

#define GREENINDICATOR 4
#define REDINDICATOR 7
#define REDLED 8

#define DMETER 5
#define AMETER 6

LiquidCrystal lcd(RS, EN, D4, D5, D6, D7);

uint8_t scroll = false;
uint8_t scroll_length = 0;
uint8_t scroll_pos = 0;

float readingDM=0;
float readingAM=0;
int light_r=0;
int light_g=0;
int light_s=0;

const byte serialBufferSize = 64;
char serialBuffer[serialBufferSize];

boolean newData = false;

volatile boolean schedulerTick = false;
const int schedulerSlotCount = 200;
int currentSchedulerSlot = 0;

boolean demoMode = true;
boolean sawEnabledDM = false;
boolean sawEnabledAM = false;

void setup() {
  Serial.begin(115200);
  Serial.println("starting");

  lcd.begin(8, 2);
  lcd.noCursor();
  lcd.noBlink();
  lcd.clear();

  pinMode(GREENINDICATOR, OUTPUT);
  pinMode(REDINDICATOR, OUTPUT);
  pinMode(REDLED, OUTPUT);
  pinMode(DMETER, OUTPUT);
  pinMode(AMETER, OUTPUT);

  cli();//stop interrupts

  //set timer1 interrupt at 50Hz
  TCCR1A = 0;// set entire TCCR1A register to 0
  TCCR1B = 0;// same for TCCR1B
  TCNT1  = 0;//initialize counter value to 0
  // set compare match register for 1hz increments
  OCR1A = 39999;// = (16*10^6) / (100*8) - 1 (must be <65536)
  // turn on CTC mode
  TCCR1B |= (1 << WGM12);
  // Set CS11 for 8 prescaler
  TCCR1B |= (1 << CS11) ;
  // enable timer compare interrupt
  TIMSK1 |= (1 << OCIE1A);


  sei();//allow interrupts

  printScroll("Digital Manufacturing on a Shoestring Hackathon");
}

void loop() {

  if (schedulerTick) {  //100 slots at 10ms ticks
    schedulerTick = false;
    currentSchedulerSlot++;
    if (currentSchedulerSlot >= schedulerSlotCount)
      currentSchedulerSlot = 0;
    
    switch (currentSchedulerSlot) {
      case 0 :
        toggleLEDon13();
        break;
      case 1 :
      case 51:
      case 101:
      case 151:
        scrollLCD();
        break;
      case 2:
      case 102:
        saw();
        break;
      case 3:
        demoRoutine();
        break;
    }

  Serial.print("DM:");
  Serial.print(readingDM);
  Serial.print(":");
  Serial.print("AM:");
  Serial.print(readingAM);
  Serial.print(":");
  Serial.print("GL:");
  Serial.print(light_g);
  Serial.print(":");
  Serial.print("RL:");
  Serial.print(light_r);
  Serial.print(":");
  Serial.print("SL:");
  Serial.print(light_s);
  Serial.println(":");
  }
  else
  {
    recvWithStartEndMarkers();
    parseInput();
  }


}

ISR(TIMER1_COMPA_vect)
{
  schedulerTick = true;
}

void demoRoutine()
{
  static uint8_t count = 0;
  static uint8_t givalue = LOW;
  static uint8_t rivalue = LOW;
  static uint8_t rlvalue = LOW;
  
  if(demoMode){
    if(count%2==0)
    {
      givalue = !givalue;
    }

    if(count%3==0)
    {
      rivalue = (!rivalue) ^ givalue;
    }


    if(count%5==0)
    {
      rlvalue = (!rlvalue) ^ rivalue;
    }
    
    setGreenIndicator(givalue);
    setRedIndicator(rivalue);
    setRedLED(rlvalue);
    count++;
  }
}

void saw() {
  uint8_t max_value = 255;
  static uint8_t current = 0;
  static boolean direction_up = true;
  const uint8_t total = 64;

  uint8_t value = ((current / (float) total) * max_value);

  if(sawEnabledDM || demoMode)
    doSetDM(value);
  if(sawEnabledAM || demoMode)
    doSetAM(value);

  readingDM=28.199*current+0.1776;
  readingAM=0.1108*current+4.2482; //calbration from arduino 'calbration.ino'
  
  if (current == 0)
    direction_up = true;
  else if (current == total)
    direction_up = false;

  if (direction_up)
    current++;
  else
    current--;
}

void toggleLEDon13()
{
  static uint8_t value = LOW;
  digitalWrite(13, value);
  value = !value;
}

void scrollLCD() {
  if (scroll)
  {
    if (scroll_pos >= scroll_length)
    {
      lcd.home();
      scroll_pos = 0;
    }
    else {
      lcd.scrollDisplayLeft();
      scroll_pos++;
    }
  }
}

void recvWithStartEndMarkers() {
  static boolean recvInProgress = false;
  static byte ndx = 0;
  static const char startMarker = '(';
  static const char endMarker = ')';
  char rc;

  if (Serial.available() > 0 && newData == false) {
    rc = Serial.read();

    if (recvInProgress == true) {
      if (rc != endMarker) {
        serialBuffer[ndx] = rc;
        ndx++;
        if (ndx >= serialBufferSize) {
          ndx = serialBufferSize - 1;
        }
      }
      else {
        serialBuffer[ndx] = '\0'; // terminate the string
        recvInProgress = false;
        ndx = 0;
        newData = true;
      }
    }

    else if (rc == startMarker) {
      recvInProgress = true;
    }
  }
}

void parseInput() {
  if (newData == true) {
    newData = false;
    if (keyEquals('d', 'e', 'm', 'o')) {
      demoMode = true;
      return;
    }
    else if (keyEquals('g', 'i'))
      setGreenIndicator(getHighLow());
    else if (keyEquals('r', 'i'))
      setRedIndicator(getHighLow());
    else if (keyEquals('r', 'l'))
      setRedLED(getHighLow());
    else if (keyEquals('d', 'm'))
      setDigitalMeter(getPercentage());
    else if (keyEquals('a', 'm'))
      setAnalogueMeter(getPercentage());

    else if (keyEquals('l', 'c', 'd', 'p'))
      print16char(serialBuffer + 5);
    else if (keyEquals('l', 'c', 'd', 's'))
      printScroll(serialBuffer + 5);

    demoMode = false;
  }
}

boolean keyEquals(char char1, char char2)
{
  return (serialBuffer[0] == char1 && serialBuffer[1] == char2 && serialBuffer[2] == ',');
}

boolean keyEquals(char char1, char char2, char char3, char char4)
{
  return (serialBuffer[0] == char1 && serialBuffer[1] == char2 && serialBuffer[2] == char3 && serialBuffer[3] == char4 && serialBuffer[4] == ',');
}

uint8_t getHighLow() {
  if (serialBuffer[3] == '1' || serialBuffer[3] == 't' || serialBuffer[3] == 'T' || serialBuffer[3] == 'H' || serialBuffer[3] == 'h')
    return HIGH;
  else
    return LOW;
}

uint8_t getPercentage() {
  char value[4];
  value[0] = serialBuffer[3];
  value[1] = serialBuffer[4];
  value[2] = serialBuffer[5];
  value[3] = '\0';

  uint8_t num = atoi(value);
  if (num > 100)
    num = 100;
  return num;
}

void setGreenIndicator(uint8_t value) {
  digitalWrite(GREENINDICATOR, value);
  light_g=value;
  //Serial.print("Set Green Indicator to: ");
  //Serial.println(value ? "HIGH" : "LOW");
}

void setRedIndicator(uint8_t value) {
  digitalWrite(REDINDICATOR, value);
  light_r=value;
  //Serial.print("Set Red Indicator to: ");
  //Serial.println(value ? "HIGH" : "LOW");
}

void setRedLED(uint8_t value) {
  digitalWrite(REDLED, value);
  light_s=value;

  //Serial.println(value ? "HIGH" : "LOW");
}

void setDigitalMeter(uint8_t percentage)
{
  doSetDM(percentage * 2.55);
  Serial.print("Set Digital Meter to: ");
  Serial.print(percentage);
  Serial.println("%");
}

void doSetDM(uint8_t value)
{
  analogWrite(DMETER, value);
}

void setAnalogueMeter(uint8_t percentage)
{
  doSetAM(percentage * 2.55);
  Serial.print("Set Analogue Meter to: ");
  Serial.print(percentage);
  Serial.println("%");
}

void doSetAM(uint8_t value)
{
  analogWrite(AMETER,value);
}

void print16char(char* chars) {
  Serial.print("Printed to LCD: ");
  Serial.println(chars);

  scroll = false;
  lcd.clear();
  uint8_t l = len(chars);
  lcd.noAutoscroll();
  lcd.setCursor(0, 0);
  if (l <= 8) {
    lcd.print(chars);
  }
  else {
    char subset[9];
    memcpy(subset, chars, sizeof(char) * 8);
    subset[9] = '\0';
    lcd.print(subset);
    lcd.setCursor(0, 1);
    memcpy(subset, chars + 8, sizeof(char) * 8);
    subset[9] = '\0';
    lcd.print(subset);
  }
}

void printScroll(char* chars) {
  Serial.print("Scrolling on LCD: ");
  Serial.println(chars);

  lcd.clear();
  uint8_t l = len(chars);
  lcd.setCursor(0, 0);
  if (l <= 8) {
    lcd.print(chars);
  }
  else
  {
    lcd.print(chars);
    lcd.setCursor(0, 1);
    lcd.print(chars + 8);
  }

  if (l > 16) {
    scroll = true;
    scroll_length = l - 16;
    scroll_pos = 0;
  }
}

uint8_t len(char* chars) {
  uint8_t n = 0;
  while (chars[n] != 0 && n != 127) {
    n++;
  }
  return n;
}
