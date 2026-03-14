#pragma once

#include "camera.h"
#include "processor.h"
#include "robot.h"
#include "dispenser.h"

class Server {
public:
    void processOrder();
private:
    Camera camera;
    Processor processor;
    Robot robot;
    Dispenser dispenser;
};