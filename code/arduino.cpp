#include <LiquidCrystal_I2C.h>
#define I2C_ADDR 0x27
#define LCD_COLUMNS 20
#define LCD_LINES 4

LiquidCrystal_I2C lcd(I2C_ADDR, LCD_COLUMNS, LCD_LINES);

void setup() {
    lcd.init();
    lcd.backlight();
    Serial.begin(9600);

    pinMode(7, OUTPUT);   // 蜂鸣器
    pinMode(13, OUTPUT);  // RGBLED 信号
    pinMode(3, OUTPUT);   // Trig
    pinMode(2, INPUT);    // Echo
}

void loop() {
    float celsius = 25;   // 默认室温
    float speed = 0.033145 * sqrt((273.15 + celsius) / 273.15); // cm/μs

    digitalWrite(3, HIGH);
    delayMicroseconds(10);
    digitalWrite(3, LOW);

    int duration = pulseIn(2, HIGH);
    float distance = (duration * speed) / 2;

    Serial.print("Distance: ");
    Serial.print(distance);
    Serial.println(" cm");

    // 距离小于 20 cm 触发报警，频率随距离减小而加快
    if (distance < 20) {
        digitalWrite(13, HIGH);
        tone(7, 261);                // 发声音调 261Hz
        int times = distance * 20;   // 延迟时间与距离挂钩
        delay(times);
        digitalWrite(13, LOW);
        noTone(7);
    }

    lcd.setCursor(0, 0);
    lcd.print("Distance:");
    lcd.setCursor(10, 0);
    lcd.print(distance);
    lcd.print(" cm   ");

    delay(10);
}
