#include <Servo.h>

Servo mouth1, mouth2, eye1, eye2, eyebrow1, eyebrow2;

int pinMouth1 = 2, pinMouth2 = 3;
int pinEye1 = 4, pinEye2 = 5;
int pinEyebrow1 = 6, pinEyebrow2 = 7;

int pinChoice, angleChoice;

void setup(){
  Serial.begin(9600);

  // Mouth
  mouth1.attach(pinMouth1);
  mouth2.attach(pinMouth2);

  // Eye
  eye1.attach(pinEye1);
  eye2.attach(pinEye2);

  // Eyebrow
  eyebrow1.attach(pinEyebrow1);
  eyebrow2.attach(pinEyebrow2);


    // Mouth
  mouth1.write(90);
  mouth2.write(90);

  // Eye
  eye1.write(90);
  eye2.write(90);

  // Eyebrow
  eyebrow1.write(90);
  eyebrow2.write(90);
}

void loop(){
  getCommandFromSerial();
}


void changeMouthMovementAngle(int pinServo, int servoAngle){

  if (pinServo == 2 || pinServo == 3){
    mouth1.write(90 - servoAngle);
    mouth2.write(90 + servoAngle);
  } else if (pinServo == 4 || pinServo == 5) {
    eye1.write(servoAngle);
    eye2.write(servoAngle);    
  } else if (pinServo == 6 || pinServo == 7) {
    eyebrow1.write(90 - servoAngle);
    eyebrow2.write(90 - servoAngle);
  }
  delay(5);
}

void getCommandFromSerial(){
  if (Serial.available() > 0) {
    String comando = Serial.readStringUntil('\n');
    comando.trim();

    Serial.println(comando);

    if (comando.startsWith("servo ")){
      pinChoice = (comando.substring(6,7)).toInt();
      angleChoice = (comando.substring(8,11)).toInt();

      Serial.println(angleChoice);

      changeMouthMovementAngle(pinChoice, angleChoice);
    }
  }
}
