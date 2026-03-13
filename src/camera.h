#pragma once

class Camera {
private:
    bool active;
    
public:
    Camera();
    void captureFrame();
};