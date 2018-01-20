// the setup function runs once when you press reset or power the board

void setup() {
    pinMode(9, OUTPUT);
    pinMode(10, OUTPUT);
    Serial.begin(9600);
}

void loop() {
    if (Serial.available()) {
        char serialListener = Serial.read();
        if (serialListener == 'a') {
            analogWrite(9, 120);
            analogWrite(10, 0);
            delay(300);
        }
        else if (serialListener == 'b') {
            analogWrite(10, 120);
            analogWrite(9, 0);
            delay(300);
        }
        else {
          analogWrite(9, 0);
          analogWrite(10, 0);
        }
    }
}
