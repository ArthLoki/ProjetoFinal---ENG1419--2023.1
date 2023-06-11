#include <Servo.h>

// VARIABLES

// Servos
Servo mouth1, mouth2;

// Mouth moviment angle. It starts in the middle (angle = 90 degrees)
int mouthAngle1 = 90;
int mouthAngle2 = 90;

// min and max angle related to the energy given
int minMouthAngle1 = 90;
int maxMouthAngle2 = 90;

// energy
int mouthEnergy = 0;
// int minMouthEnergy = 15;
int characterEnergy = 0;

// FUNCTIONS

// default functions
void setup(){
    Serial.begin(9600);

    mouth1.attach(4, 1000, 2000);
    mouth2.attach(5, 1000, 2000);

    mouth1.write(90)
    mouth2.write(90)
}

void loop(){
  getCommandFromSerial();
}

// Aux functions
void getCommandFromSerial(){
  if (Serial.available() > 0) {
    String comando = Serial.readStringUntil('\n');
    comando.trim();

    if (comando.startsWith("personalidade ")) {
      characterEnergy = (comando.substring(14,17)).toInt();
    }

    if (comando.startsWith("boca ")) {
      mouthEnergy = (comando.substring(5,8)).toInt();

      minMouthAngle1 = map(mouthEnergy, 0, 100, 90, 30);
      maxMouthAngle2 = map(mouthEnergy, 0, 100, 90, 150);
    }

    if (comando == "falando"){
      changeMouthMovementAngle();
    }

    if (comando == "fim"){
      mouth1.write(90);
      mouth2.write(90);
    }
  }
}

// Function to change the angle of the mouth while talking
void changeMouthMovementAngle(){
  // mouth1
  mouthAngle1 = mouth1.read();

  if (mouthAngle1 <= minMouthAngle1){
    mouth1.write(90);
  } else if (mouthAngle1 >= 90){
    mouth1.write(minMouthAngle1);
  }

  // mouth2
  mouthAngle2 = mouth2.read();

  if (mouthAngle2 >= maxMouthAngle2){
    mouth2.write(90);
  } else if (mouthAngle2 <= 90){
    mouth2.write(maxMouthAngle2);
  }
}
