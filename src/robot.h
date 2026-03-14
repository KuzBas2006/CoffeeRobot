#pragma once
#include "processor.h"
#include <string>

using namespace std;

class Robot {
public:
    Robot();
    void moveTo(int x, int y);
    void stop();
private:
    Position pos;
};

class AReceiver {
public:
    virtual string receive() = 0;
};

class FooReceive: public AReceiver {
public:
    string receive() override;
};

class AEngine {
public:
    virtual void forward() = 0;
    virtual void left() = 0;
    virtual void right() = 0;
    virtual void stop() = 0;
};

class FooEngine: public AEngine {
public:
    void forward() override;
    void left() override;
    void right() override;
    void stop() override;
};

class App{
    void run();
};