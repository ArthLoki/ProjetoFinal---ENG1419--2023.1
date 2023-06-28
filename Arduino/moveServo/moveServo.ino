#include <Servo.h>

// VARIABLES

// Servos
Servo mouth1, mouth2, eye1, eye2, eyebrow1, eyebrow2;

int pinMouth1 = 2, pinMouth2 = 3;
int pinEye1 = 4, pinEye2 = 5;
int pinEyebrow1 = 6, pinEyebrow2 = 7;

// Mouth moviment angle. It starts in the middle (angle = 90 degrees)
int mouthAngle1 = 90;
int mouthAngle2 = 90;

// min and max angle related to the energy given
int serialMouthAngle1 = 90;
int serialMouthAngle2 = 90;
int mouthMaxOpening = 40;

// energy
int mouthEnergy = 0;
int mouthEnergyConstrain1 = 0;
int mouthEnergyConstrain2 = 0;

// personality
String characterPersonality = "";

// FUNCTIONS

// default functions
void setup(){
    Serial.begin(115200);

    // Mouth
    mouth1.attach(pinMouth1);
    mouth2.attach(pinMouth2);
  
    // Eye
    eye1.attach(pinEye1);
    eye2.attach(pinEye2);
  
    // Eyebrow
    eyebrow1.attach(pinEyebrow1);
    eyebrow2.attach(pinEyebrow2);

    mouth1.write(90);
    mouth2.write(90);

    eye1.write(90);
    eye2.write(90);

    eyebrow1.write(90);
    eyebrow2.write(90);
}

void loop(){
  getCommandFromSerial();
}

// Aux functions
void getCommandFromSerial(){
  if (Serial.available() > 0) {
    String comando = Serial.readStringUntil('\n');
    comando.trim();

    // Serial.println(comando);

    if (comando.startsWith("personalidade ")) {
      characterPersonality = comando.substring(14);
      changeEyebrowMovementAngle();     
    }

    if (comando.startsWith("falando ")){
      mouthEnergy = (comando.substring(8,11)).toInt();

      serialMouthAngle1 = map(mouthEnergy, 0, 100, 90, 90 + mouthMaxOpening);
      serialMouthAngle2 = map(mouthEnergy, 0, 100, 90, 90 - mouthMaxOpening);

      serialMouthAngle1 = constrain(serialMouthAngle1, 90, 90 + mouthMaxOpening);
      serialMouthAngle2 = constrain(serialMouthAngle2, 90, 90 - mouthMaxOpening);

      changeMouthMovementAngle();
    }

    if (comando == "fim"){
      mouth1.write(90);
      mouth2.write(90);
      
      eyebrow1.write(90);
      eyebrow2.write(90);
    }
  }
}

// Function to change the angle of the mouth while talking
void changeMouthMovementAngle(){
  // mouth1
  mouthAngle1 = mouth1.read();

  if (mouthAngle1 >= serialMouthAngle1){
    mouth1.write(90);
  } else if (mouthAngle1 <= 90){
    mouth1.write(serialMouthAngle1);
  }

  // mouth2
  mouthAngle2 = mouth2.read();

  if (mouthAngle2 <= serialMouthAngle2){
    mouth2.write(90);
  } else if (mouthAngle2 >= 90){
    mouth2.write(serialMouthAngle2);
  }

  // delay(5);
}

void changeEyebrowMovementAngle(){
  if (characterPersonality == "triste" || characterPersonality == "cansado"){
    eyebrow1.write(60);
    eyebrow2.write(130);
  } else if (characterPersonality == "normal" || characterPersonality == "feliz"){
    eyebrow1.write(90);
    eyebrow2.write(90);
  } else if (characterPersonality == "zangado"){
    eyebrow1.write(120);
    eyebrow2.write(60);
  } else {
    eyebrow1.write(90);
    eyebrow2.write(90);
  }

  // delay(5);
}
