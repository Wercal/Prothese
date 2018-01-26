/*
* Mouvement de l'index - Prosthetic-hand-prog - SynapsETS @ ETS.
* Fait par: Mubashar Hussain
* Date de création: 09/01/2018
* Dernière modif: 09/01/2018
*/


// Adafruit Motor shield library
// copyright Adafruit Industries LLC, 2009
// this code is public domain, enjoy!

#include <AFMotor.h>

AF_DCMotor motor(3);         //possition du moteur sur le shield

void setup() {
  Serial.begin(9600);           // set up Serial library at 9600 bps
  Serial.println("Motor test!");

  // turn on motor
  motor.setSpeed(200);
 
  motor.run(RELEASE);

  String status = "free";
  char lastCommand ='0';
}

void loop () { 

  int vitesse = 255;//vitesse de 0 a 255
  int repos = 1;//l'index block a la fin du mouvement si != 0
  int duree = 13000;//duree du mouvement de l'index

  char serialListener = Serial.read();

  Serial.println("free");
  
        
  if (serialListener == 'a')
  {
    Serial.print("ouverture de l'index\n");     //ouverture de l'index
    motor.run(FORWARD);
    motor.setSpeed(vitesse);  
    delay(duree);
  }else if (serialListener == 'b')
  {
    Serial.print("fermeture de l'index\n");     //fermeture de l'index
    motor.run(BACKWARD);
    motor.setSpeed(vitesse);  
    delay(duree);
  }

  motor.setSpeed(0);      //immobilisation du doit


  if (repos == 0)
  {
    Serial.print("repos\n");        //permet au doit de bouger librement
    motor.run(RELEASE);
  }

}
