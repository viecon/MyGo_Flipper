#include <Stepper.h>
#include <WiFi.h>
#include <WebServer.h>
#include <ArduinoJson.h>  // Optional: For JSON parsing

// Replace with your network credentials
const char* ssid = "SSID";
const char* password = "PASSWORD";

// Create a WebServer object on port 80
WebServer server(80);

const int stepsPerRevolution = 2048;  // change this to fit the number of steps per revolution

// ULN2003 Motor Driver Pins
#define IN1 15
#define IN2 13
#define IN3 12
#define IN4 14

// initialize the stepper library
Stepper myStepper(stepsPerRevolution, IN1, IN3, IN2, IN4);
int position[32] = { 0, -64, -128, -192, -256, -320, -384, -448, -512, -576, -640,
                     -704, -768, -832, -896, -960, -1024, -1088, -1152, -1216, -1280, -1344, -1408,
                     -1472, -1536, -1600, -1664, -1728, -1792, -1856, -1920, -1984 };
int cur_pos = position[0]; // change if not 0

#define IR_PIN 27

void move_to(int tar) {
  tar--;
  int diff = position[tar] - cur_pos;
  if (diff > 0)
    diff = diff - 2048;
  myStepper.step(diff);
  cur_pos = position[tar];
}

// Handle POST request on "/spin"
void handlePostSpin() {
  if (server.method() == HTTP_POST) {
    String body = server.arg("plain");  // Get the raw body as a string

    Serial.println("Received Body:");
    Serial.println(body);

    // Optional: Parse JSON using ArduinoJson
    StaticJsonDocument<200> doc;
    DeserializationError error = deserializeJson(doc, body);

    if (error) {
      Serial.print("JSON Parse Error: ");
      Serial.println(error.c_str());
      server.send(400, "application/json", "{\"error\":\"Invalid JSON\"}");
      return;
    }

    int position = doc["position"];
    Serial.println(position);
    // Respond with the received data
    String jsonResponse = "{\"received\":\"received\"}";
    server.send(200, "application/json", jsonResponse);
    move_to(position);
    Serial.println(cur_pos);
  } else {
    server.send(405, "application/json", "{\"error\":\"Method Not Allowed\"}");
  }
}

void setup() {
  // Start Serial communication
  Serial.begin(115200);

  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected to WiFi");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());

  // Define routes
  server.on("/spin", HTTP_POST, handlePostSpin);

  // Start the server
  server.begin();

  myStepper.setSpeed(5);
  
  pinMode(IR_PIN, INPUT);
  while (digitalRead(IR_PIN) == HIGH) {
    myStepper.step(-1);
    delay(10);
  }
  myStepper.step(0);

  Serial.begin(115200);
}


void loop() {
  server.handleClient();
}
