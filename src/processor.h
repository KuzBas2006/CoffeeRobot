#pragma once

struct Position {
    int x, y;
};

class Processor {
public:
    Processor();
    void findHuman();
    void findRobot();
    void findDispenser();
    void recognizeGesture();
    Position getHumanPos();
    Position getRobotPos();
    Position getDispenserPos();
private:
    Position humanPos;
    Position robotPos;
    Position dispenserPos;
};