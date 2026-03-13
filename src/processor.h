#pragma once

struct Position {
    int x, y;
};

class Processor {
private:
    Position humanPos;
    Position robotPos;
    Position dispenserPos;
    
public:
    Processor();
    void findHuman();
    void findRobot();
    void findDispenser();
    void recognizeGesture();
    Position getHumanPos();
    Position getRobotPos();
    Position getDispenserPos();
};