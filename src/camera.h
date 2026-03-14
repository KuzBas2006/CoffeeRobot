#pragma once

class Camera {
public:
    Camera();
    void captureFrame();
private:
    bool active;
};