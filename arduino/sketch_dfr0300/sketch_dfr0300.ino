#include "DFRobot_EC.h"
#include <EEPROM.h>

#define EC_PIN A0
float  voltageEC,ecValue,temperature = 25;
DFRobot_EC ec;

void setup()
{
    Serial.begin(115200);  
    ec.begin();
}

void loop()
{
    char cmd[10];
    static unsigned long timepoint = millis();
    if(millis()-timepoint>1000U){                            //time interval: 1s
        timepoint = millis();
        //temperature = readTemperature();                   // read your temperature sensor to execute temperature compensation
        voltageEC = analogRead(EC_PIN)/1024.0*5000;
        ecValue    = ec.readEC(voltageEC,temperature);       // convert voltage to EC with temperature compensation
        Serial.print(ecValue,2);
    }
    if(readSerial(cmd)){
        strupr(cmd);
        if(strstr(cmd,"EC")){
            ec.calibration(voltageEC,temperature,cmd);       //EC calibration process by Serail CMD
        }
    }
}

int i = 0;
bool readSerial(char result[]){
    while(Serial.available() > 0){
        char inChar = Serial.read();
        if(inChar == '\n'){
             result[i] = '\0';
             Serial.flush();
             i=0;
             return true;
        }
        if(inChar != '\r'){
             result[i] = inChar;
             i++;
        }
        delay(1);
    }
    return false;
}

float readTemperature()
{
  //add your code here to get the temperature from your temperature sensor
  return 25.0;
}
