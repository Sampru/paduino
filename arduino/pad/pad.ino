#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <Keypad.h>

#include "screen.h"

#define OFFLINE 1
#define ONLINE 2
#define SCREENSAVER 3

// Rows and cols layout
const byte nrow = 3;
const byte ncol = 4;
byte rows[nrow] = { 7, 8, 9 };
byte cols[ncol] = { 10, 16, 14, 15 };

// Button matrix layout
char keys[nrow][ncol] = {
  { '1', '2', '3', 'u' },
  { '4', '5', '6', 'd' },
  { 'D', 'S', 'M', 'H' }
};

// Keypad and display
Keypad keypad = Keypad(makeKeymap(keys), rows, cols, nrow, ncol);
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

// Animation variables
byte status = OFFLINE;
int x_animation = -w_not_connected;

// Clock variables
unsigned long epochTime = 0; // ms since epoch
unsigned long lastSync = 0;  // ms since sync
bool blink = true;

void setup() {
  Serial.begin(9600);

  // Init display
  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {  // 0x3C is the common I2C dir
    Serial.println(F("SSD1306 allocation failed"));
    for (;;)
      ;
  }

  //Config display
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.setTextWrap(false);
  display.clearDisplay();

  delay(2000);
}

void loop() {
  // Read serial if available
  if (Serial.available() > 0) {
    handleSerial();
  }

  // Check status
  switch (status) {
    case OFFLINE:
      // Do animation
      offlineAnimation();
      break;
    case SCREENSAVER:
      // Show a clock
      clockAnimation();
    case ONLINE:
      // Manage keyboard
      manageKeyboard();
      break;
  }
}

void handleSerial() {
  String msg = Serial.readStringUntil('\n');
  if (msg == "_OK") {
    status = ONLINE;
    saveTime();
  } else if (msg == "_MS") {
    status = ONLINE;
    manageScreen();
  } else if (msg == "_SS") {
    status = SCREENSAVER;
  } else if (msg == "_KO"){
    status = OFFLINE;
  }
}


// Screen the offline animation with a moving x
void offlineAnimation() {
  display.clearDisplay();
  display.drawBitmap(x_animation, 0, not_connected, w_not_connected, h_not_connected, WHITE);
  display.display();
  if (x_animation > SCREEN_WIDTH) {
    x_animation = -w_not_connected;
  } else {
    x_animation++;
  }
}

void saveTime() {
  if (Serial.available() > 0) {
    String epochTimeStr = Serial.readStringUntil('\n');
    epochTime = epochTimeStr.toInt();
    lastSync = millis() / 1000;
  }
}

void clockAnimation() {
  // Get the actual time
  unsigned long elapsedSeconds = (millis() / 1000) - lastSync;
  unsigned long currentEpochTime = epochTime + elapsedSeconds;
  String currentTime = epochToString(currentEpochTime);

  display.clearDisplay();
  display.setTextSize(2);
  display.setCursor(x_animation, 8); //Text is 96x16, so it appears centered
  display.print(currentTime);
  display.display();

  if (x_animation > SCREEN_WIDTH) {
    x_animation = -96;
  } else {
    x_animation++;
  }
}

// Screen information comes right after a _MS\n and separated by lines, read and display it
void manageScreen() {
  display.clearDisplay();
  display.setTextSize(1);
  display.setCursor(0, 0);
  while (Serial.available() > 0) {
    String screenText = Serial.readStringUntil('\n');
    display.println(screenText);
  }
  display.display();
}

// Read pressed key, then send it from terminal with $ prefix
void manageKeyboard() {
  char key = keypad.getKey();
  if (key) {
    Serial.print('$');
    Serial.println(key);
  }
}