#include "DFRobot_EC.h"
#include <EEPROM.h>
// Water temp libs
#include <OneWire.h>
#include <DallasTemperature.h>

// EC vars
#define EC_PIN A0
float  voltageEC, ecValue, temperature = 25;
DFRobot_EC ec;

// PH vars
const int PHPin = A1;
int sensorValue = 0;
unsigned long int avgValue;
float b;
int buf[10], temp;

// Water temp vars

#define ONE_WIRE_BUS 2
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

//Flow meter vars
volatile int NbTopsFan; //measuring the rising edges of the signal
int Calc;                              
int hallsensor = 2;    //The pin location of the sensor

void setup()
{
  Serial.begin(9600);

  ec_botstrap();
  water_temp_bootstrap();
  flowmeter_bootstrap();
}

void loop()
{
  float ec_val = ec_loop();
  float ph_val = ph_loop();
  float water_tmp = water_temp_loop();
  float flow_meter = flow_loop();
  
  Serial.print("vp-io-0 : ");
  Serial.print(ec_val);
  Serial.print("-vp-sep-");
  Serial.print("vp-io-1 : ");
  Serial.print(ph_val);
  Serial.print("-vp-sep-");
  Serial.print("vp-io-2 : ");
  Serial.print(water_tmp);
  Serial.print("-vp-sep-");
  Serial.print("vp-io-3 : ");
  Serial.println(flow_meter);

  delay(1000);
}

float ec_loop() {
  char cmd[10];
  static unsigned long timepoint = millis();
  if (millis() - timepoint > 1000U) {
    timepoint = millis();
    //temperature = readTemperature();
    voltageEC = analogRead(EC_PIN) / 1024.0 * 5000;
    ecValue    = ec.readEC(voltageEC, temperature);
  }
  if (ec_readSerial(cmd)) {
    strupr(cmd);
    if (strstr(cmd, "EC")) {
      ec.calibration(voltageEC, temperature, cmd);
    }
  }
  return (ecValue);
}

int i = 0;
bool ec_readSerial(char result[]) {
  while (Serial.available() > 0) {
    char inChar = Serial.read();
    if (inChar == '\n') {
      result[i] = '\0';
      Serial.flush();
      i = 0;
      return true;
    }
    if (inChar != '\r') {
      result[i] = inChar;
      i++;
    }
  }
  return false;
}

void flowmeter_bootstrap(){
   pinMode(hallsensor, INPUT);
   attachInterrupt(0, rpm, RISING);
}
void ec_botstrap() {
  ec.begin();
}

void water_temp_bootstrap() {
  sensors.begin();
}

float water_temp_loop(){
  sensors.requestTemperatures();
  return sensors.getTempCByIndex(0);
}

float ph_loop() {
  for (int i = 0; i < 10; i++)
  {
    buf[i] = analogRead(PHPin);
    delay(30);
  }
  for (int i = 0; i < 9; i++)
  {
    for (int j = i + 1; j < 10; j++)
    {
      if (buf[i] > buf[j])
      {
        temp = buf[i];
        buf[i] = buf[j];
        buf[j] = temp;
      }
    }
  }
  avgValue = 0;
  for (int i = 2; i < 8; i++)
    avgValue += buf[i];
  float pHVol = (float)avgValue * 5.0 / 1024 / 6;
  float phValue = -5.70 * pHVol;

  return (phValue);
}

float flow_loop(){
 NbTopsFan = 0;
 sei();
 cli();
 Calc = (NbTopsFan * 60 / 7.5);
 return Calc;
}
void rpm ()
{
 NbTopsFan++;
}
