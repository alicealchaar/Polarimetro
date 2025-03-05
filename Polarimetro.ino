void setup() {
    Serial.begin(9600);  // Inicia a comunicação serial
}

void loop() {
    int sensor1 = analogRead(A0);  // Lê a entrada analógica A0
    int sensor2 = analogRead(A1);  // Lê a entrada analógica A1
    int sensor3 = analogRead(A2);  // Lê a entrada analógica A2
    int sensor4 = analogRead(A3);  // Lê a entrada analógica A3

    // Envia os valores para o PC separados por vírgula
    Serial.print(sensor1);
    Serial.print(",");
    Serial.print(sensor2);
    Serial.print(",");
    Serial.print(sensor3);
    Serial.print(",");
    Serial.println(sensor4); // Último valor com println para marcar fim da linha

    delay(100);  // Pequena pausa para evitar sobrecarga na comunicação
}
