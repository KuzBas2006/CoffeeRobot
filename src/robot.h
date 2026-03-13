#pragma once

#include "processor.h"

class Robot {
private:
    Position pos;
    
public:
    Robot();
    void moveTo(int x, int y);
    void stop();
};