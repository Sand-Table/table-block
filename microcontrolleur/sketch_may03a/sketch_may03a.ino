const int dirPin = 3;
const int stepPin = 2;


void setup() {
  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(115200); // opens serial port, sets data rate to 115200 bps
}

void loop() {
  Serial.print("Starting!");
  digitalWrite(dirPin, HIGH);
   delay(1000);
 digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
  for (int x = 0; x < 200; x++) {
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(2200);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(2200);
  }
  digitalWrite(dirPin, LOW);
  delay(1000);
  digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
  for (int x = 0; x < 200; x++) {
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(2200);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(2200);
  }
}
