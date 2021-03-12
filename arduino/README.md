# Arduino (Veggino ¯\_(ツ)_/¯)

In order to be able to get analog readings in the raspberry, analog sensors need to pass through the Arduino that acts as a DAC for the setup.

To ensure standardize the analog inputs across different kits, please make sure to respect the following order when connecting your sensor 


|       	|         Top of the arduino         	|    	|          	|
|-------	|:----------------------------------:	|----	|----------	|
| --    	|                                    	| ** 	|      SCL 	|
| --    	|                                    	| ** 	|      SDA 	|
| --    	|                                    	| ** 	|     AREF 	|
| --    	|                                    	| ** 	|      GND 	|
| void  	|                                    	| ** 	|      D13 	|
| IOREF 	|                                    	| ** 	|      D12 	|
| RESET 	|                                    	| ** 	|      D11 	|
| 3.3V  	|                                    	| ** 	|      D10 	|
| 5V    	| Power for the sensors              	| ** 	|       D9 	|
| GND   	| Ground for the sensors             	| ** 	|       D8 	|
| GND   	| Ground for the sensors             	| ** 	|       -- 	|
| VIN   	|                                    	| ** 	|       D7 	|
| --    	|                                    	| ** 	|       D6 	|
| A0    	| vp - EC sensor data passthrough    	| ** 	|       D5 	|
| A1    	| vp - PH sensor p0 data passthrough 	| ** 	|       D4 	|
| A2    	| vp - PH sensor t0 data passthrough 	| ** 	|       D3 	|
| A3    	|                                    	| ** 	|       D2 	|
| A4    	|                                    	| ** 	| (tx1) D1 	|
| A5    	|                                    	| ** 	| (rx1) D0 	|

# Flow meter

In order for the flow meter to work, you need to connect its VCC to the arduino's 5v pin, the ground to the ground, and the data to to the _DIGITAL PIN 2_ of the arduino. You also need to short the ciruit between the data and the VCC with a 10k ohm resistor. 
