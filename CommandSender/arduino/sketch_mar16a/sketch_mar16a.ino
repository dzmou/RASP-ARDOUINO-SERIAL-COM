String command;

#define blueLed 8
#define greenLed 9
#define redLed 10

void setup() {
  Serial.begin(9600);
  pinMode(blueLed, OUTPUT);
  pinMode(greenLed, OUTPUT);
  pinMode(redLed, OUTPUT);
  
  delay(1000);
  // check   
  digitalWrite(blueLed, HIGH);
  digitalWrite(greenLed, HIGH);
  digitalWrite(redLed, HIGH);

  delay(2000);
  digitalWrite(blueLed, LOW);
  digitalWrite(greenLed, LOW);
  digitalWrite(redLed, LOW);

  Serial.println("Type Command (green, blue, red, all, off)");
}

void loop() {
  if (Serial.available()) {
    command = Serial.readStringUntil('\n');
    command.trim();
    if (command.equals("green")) {
      digitalWrite(greenLed, HIGH);
      digitalWrite(blueLed, LOW);
      digitalWrite(redLed, LOW);
    }

    else if (command.equals("blue")) {
      digitalWrite(greenLed, LOW);
      digitalWrite(blueLed, HIGH);
      digitalWrite(redLed, LOW);
    }
    else if (command.equals("red")) {
      digitalWrite(greenLed, LOW);
      digitalWrite(blueLed, LOW);
      digitalWrite(redLed, HIGH);
    }
    else if (command.equals("all")) {
      digitalWrite(greenLed, HIGH);
      digitalWrite(blueLed, HIGH);
      digitalWrite(redLed, HIGH);
    }
    else if (command.equals("off")) {
      digitalWrite(greenLed, LOW);
      digitalWrite(blueLed, LOW);
      digitalWrite(redLed, LOW);
    }
    else {
      Serial.println("bad command");
    }
    Serial.print("Command: ");
    Serial.println(command);
  }
}