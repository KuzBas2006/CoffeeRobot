#include "processor.h"

Processor::Processor() : humanPos{0,0}, robotPos{0,0}, dispenserPos{0,0} {}

void Processor::findHuman() {
    humanPos = {10, 20};
}

void Processor::findRobot() {
    robotPos = {0, 0};
}

void Processor::findDispenser() {
    dispenserPos = {5, 5};
}

void Processor::recognizeGesture() {
    // Gesture recognition logic
}

Position Processor::getHumanPos() { return humanPos; }
Position Processor::getRobotPos() { return robotPos; }
Position Processor::getDispenserPos() { return dispenserPos; }