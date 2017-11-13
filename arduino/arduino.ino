// the setup function runs once when you press reset or power the board

void setup() {
    pinMode(LED_BUILTIN, OUTPUT);
    Serial.begin(9600);
}

void loop() {
    if (Serial.available()) {
        char serialListener = Serial.read();
        if (serialListener == 'H') {
            digitalWrite(LED_BUILTIN, HIGH);
        }
        else if (serialListener == 'L') {
            digitalWrite(LED_BUILTIN, LOW);
        }
    }
}
