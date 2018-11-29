#include <Wire.h> 
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x3F,16,2);  /* или 0x27. */
const char TERM_SYMBOL = '#';
const char TERM_ENTER_SYMBOL = '%';
const int LED_PINS[] = {7, 8, 9, 10, 11, 12};
const String NAME_SIGNAL_UNKNOWN_FACE = "Unknown";
String inputString = "";


void ledInit()
{
   for( int i = 0; i < sizeof(LED_PINS); ++i )
      pinMode(LED_PINS[i], OUTPUT);
}

void ledOn()
{
   for( int i = 0; i < sizeof(LED_PINS); ++i)
   {
      digitalWrite(LED_PINS[i], HIGH );
      delay(100);
   } 
}

void ledOff()
{
   for( int i = 0; i < sizeof(LED_PINS); ++i)
   {
      digitalWrite(LED_PINS[i], LOW );
      delay(10);
   } 
}

void onBuzzer()
{
  for( int i = 0; i < 3; ++i )
  {
    analogWrite(3, 50);
    delay(200);
    analogWrite(3, 0);
    delay(200);    
  }
}

void clearDisplay(int idStroka)
{
  lcd.setCursor(0, idStroka);
  lcd.print ("                ");
}

void printDisplay(String str, int idStr, int curPos)
{
   lcd.setCursor(curPos, idStr);
   lcd.print(str);
   inputString = ""; 
}
void waitFunc(bool flag)
{
  if(flag)
    ledOff();
  delay(5000);
  clearDisplay(0);
  clearDisplay(1);
  lcd.setCursor(6, 0);    
  lcd.print("Wait");
}

void serialEvent() 
{
  clearDisplay(0);
  clearDisplay(1);
  while (Serial.available()) {
    char inChar = (char)Serial.read();  // Получение нового байта
    Serial.print(inChar);
    if(inChar != TERM_SYMBOL && inChar != TERM_ENTER_SYMBOL) {
      inputString += inChar;
    }
    else {
      if( inputString == NAME_SIGNAL_UNKNOWN_FACE && inChar != TERM_ENTER_SYMBOL )
      {
          clearDisplay(0);
          clearDisplay(1);
          printDisplay(inputString, 0, 5);
          ledOn();
          onBuzzer();
          waitFunc(true);
          break;
      }
      if(inChar == TERM_ENTER_SYMBOL){
         printDisplay(inputString, 0, 5);  
      }
      else{
         printDisplay(inputString, 1, 4);
      }  
    }
  }
  waitFunc(false);
}
void setup()
{
  ledInit();
  pinMode(3, OUTPUT);
  Serial.begin(9600);
  Serial.println("Hi Computer");
  lcd.begin();                  // Инициализация 
  lcd.backlight();             // Включаем подсветку
  lcd.print("Ready to work");  // Выводим текст
}
void loop()  // цикл
{

  
}
