//Tag
// TAG (Mobile Unit)

#include <WiFi.h>
#include <WiFiUdp.h>

const char* ssid = "...........";
const char* password = ".........";
String response;
WiFiUDP udp;
IPAddress serverIP(192,168,225,147);  
const unsigned int serverPort = 8080;  

void setup() {
    Serial.begin(115200);
     Serial.begin(115200);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");



    Serial2.begin(115200, SERIAL_8N1, 16, 17); // Use GPIO16 (RX2) & GPIO17 (TX2)

    Serial.println("Setting UWB as TAG...");

    delay(500);
    Serial2.println("AT");  // Test UWB module
    delay(500);
    Serial2.println("AT+RST");  // Reset UWB module
    delay(1000);
    Serial2.println("AT+anchor_tag=0,1");  // Set as TAG
    delay(500);
    Serial2.println("AT+interval=5");  // Set update interval (5ms)
    delay(500);
    Serial2.println("AT+switchdis=1");  // Enable ranging mode
    delay(1000);

    Serial.println("UWB TAG Setup Complete.");
}

void loop() {
    Serial2.println("AT+DIST?");  // Request distance from Anchor
    delay(200);  // Give time for response

    if (Serial2.available()) {
        response = Serial2.readStringUntil('\n');  // Read response
          Serial.println(response);
        
    }
    delay(200);
  udp.beginPacket(serverIP, serverPort);
   
    String data = response;

  udp.print(data);
  udp.endPacket();

  delay(20);  // Adjust delay according to your requirements
}
