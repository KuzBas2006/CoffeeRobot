#pragma once

#include "camera.h"
#include "processor.h"
#include "robot.h"
#include "dispenser.h"

class Server {
private:
    Camera camera;
    Processor processor;
    Robot robot;
    Dispenser dispenser;
    
public:
    void processOrder();
};