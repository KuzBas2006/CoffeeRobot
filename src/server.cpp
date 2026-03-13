#include "server.h"

void Server::processOrder() {
    // 1. Get frame
    camera.captureFrame();
    
    // 2. Process image
    processor.findHuman();
    processor.findRobot();
    processor.findDispenser();
    processor.recognizeGesture();
    
    // 3. Move robot
    robot.moveTo(10, 20);
    
    // 4. Dispense coffee
    dispenser.dispenseCoffee();
}