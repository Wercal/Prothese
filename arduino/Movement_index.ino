/*
* Movement of the index - Prosthetic-hand-prog - SynapsETS @ ETS.
* Made by: Mubashar Hussain
* Creation date: 09/01/2018
* Last change: 26/01/2018
*/


// Adafruit Motor shield library
// copyright Adafruit Industries LLC, 2009
// this code is public domain, enjoy!

#include <AFMotor.h>

AF_DCMotor motor(3);         //motor position on the shield

void setup() {
  Serial.begin(9600);           // set up Serial library at 9600 bps
  Serial.println("Motor test!");

  // turn on motor
  motor.setSpeed(200);
 
  motor.run(RELEASE);
}

void loop () { 

  int vitesse = 255;                            //speed from 0 to 255
  int repos = 1;                                //the index block at the end of the movement if != 0
  int duree = 12000;                            //duration of the movement of the index

  char serialListener = Serial.read();


        
  if (serialListener == 'a')
  {
    Serial.print("ouverture de l'index\n");     //opening the index
    motor.run(FORWARD);
    motor.setSpeed(vitesse);  
    delay(duree);
  }else if (serialListener == 'b')
  {
    Serial.print("fermeture de l'index\n");     //closing the index
    motor.run(BACKWARD);
    motor.setSpeed(vitesse);  
    delay(duree);
  }

  motor.setSpeed(0);                            //immobilization of the finger
  

  if (repos == 0)
  {
    Serial.print("repos\n");                    //allows the finger to move freely
    motor.run(RELEASE);
  }

}
