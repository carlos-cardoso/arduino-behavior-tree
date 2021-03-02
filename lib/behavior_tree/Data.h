#ifndef DATA_H
#define DATA_H

#include "stdint.h"
#include "Arduino.h"

struct Data{
    public:
    uint32_t start{0};
    const uint32_t led; // the pin the LED is connected to
    Data(const uint32_t pin): led(pin){
    };
    void initialize(const uint32_t _millis){
        this->start = _millis;
        pinMode(led, OUTPUT); // Declare the LED as an output
    }

};

#endif //DATA_H
