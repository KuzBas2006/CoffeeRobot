#include "robot.h"

Robot::Robot() : pos{0,0} {}

void Robot::moveTo(int x, int y) {
    pos.x = x;
    pos.y = y;
}

void Robot::stop() {

}