//Anchor
// ANCHOR (Fixed Unit)

void setup() {
    Serial.begin(115200);     
    Serial2.begin(115200, SERIAL_8N1, 17, 16);

    Serial.println("Setting UWB as Anchor...");

    delay(500);
    Serial2.println("AT");               
    delay(500);
    Serial2.println("AT+RST");           
    delay(1000);
    Serial2.println("AT+anchor_tag=1,3");  // (MODE,ID)
    delay(500);
    Serial2.println("AT+interval=10");    
    delay(500);
    Serial2.println("AT+switchdis=1");   
    delay(1000);

    Serial.println("UWB Anchor Setup Complete.");
}

void loop() {
    if (Serial2.available()) {
        String input = Serial2.readStringUntil('\n');  
        Serial.println("Received: " + input);

        // If the TAG requests distance, respond with real distance
        if (input.startsWith("AT+DIST?")) {  
            Serial2.println("AT+RNG");  // Start distance measurement
            delay(200);

            if (Serial2.available()) {
                String distanceResponse = Serial2.readStringUntil('\n');
                Serial.println("Distance Measured: " + distanceResponse);
                Serial2.println(distanceResponse);  // Send back to TAG
            }
        }
    }
 delay(100);
}
