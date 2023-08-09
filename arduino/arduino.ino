#include <Arduino_LED_Matrix.h>
#include "Bad_Apple.h"

ArduinoLEDMatrix Matrix;

void setup() {
  Serial.begin(9600);
  Matrix.begin();

  delay(1000);
}

const int frame_count = 6569;
int current_frame = 0;

void loop() {
  if (current_frame == 0) {
    Serial.println("Bad Apple Start!");
  }

  Matrix.loadFrame(frames[current_frame]);
  
  current_frame = (current_frame + 1) % frame_count;

  delay(33);
}
