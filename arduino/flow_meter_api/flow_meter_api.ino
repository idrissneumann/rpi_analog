#include <WiFi.h>
#include "aREST.h"

// REST CONFIGS
const char* ssid     = "ooredoo_70AD08";
const char* password = "WX43VTRAWX474";
String header;

WiFiServer server(80);

IPAddress local_IP(192, 168, 1, 181);
IPAddress gateway(192, 168, 1, 1);
IPAddress subnet(255, 255, 255, 0);

// REST CONFIGS
//aREST rest = aREST();

// FLOW CONFIGS
volatile int NbTopsFan; //measuring the rising edges of the signal
int Calc;
int hallsensor = 2;    //The pin location of the sensor


float printFlow() {
  Calc = (NbTopsFan * 60 / 7.5);
  return Calc;
}

void rpm () {
  NbTopsFan++;
}

void setup() {
  Serial.begin(115200);

  // FLOW SETUP
  pinMode(hallsensor, INPUT);
  attachInterrupt(0, rpm, RISING);

  // REST SETUP
  //rest.function("flow", printFlow);

  if (!WiFi.config(local_IP, gateway, subnet)) {
    Serial.println("STA Failed to configure");
  }

  // HTTP SETUP
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("WiFi connected with IP: ");
  Serial.println(WiFi.localIP());
  server.begin();


}

void loop ()
{
  NbTopsFan = 0;
  sei();
  //  delay (1000);
  cli();

  WiFiClient client = server.available();
  if (client) {

    while (!client.available()) {
      delay(5);
    }
    //rest.handle(client);

    String currentLine = "";                // make a String to hold incoming data from the client
    while (client.connected()) {            // loop while the client's connected
      if (client.available()) {             // if there's bytes to read from the client,
        char c = client.read();             // read a byte, then
        Serial.write(c);                    // print it out the serial monitor
        header += c;
        if (c == '\n') {                    // if the byte is a newline character
          if (currentLine.length() == 0) {
            client.println("HTTP/1.1 200 OK");
            client.println("Content-type:text/html");
            client.println("Connection: close");
            client.println();
            if (header.indexOf("GET /flow") >= 0) {
              client.println(printFlow());
            }
            
            // The HTTP response ends with another blank line
            client.println();
            break;
          } else {
            currentLine = "";
          }
        } else if (c != '\r') {  // if you got anything else but a carriage return character,
          currentLine += c;      // add it to the end of the currentLine
        }
      }
    }
    header = "";
    // Close the connection
    client.stop();
  }
}
