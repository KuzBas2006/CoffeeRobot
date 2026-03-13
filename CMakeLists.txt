cmake_minimum_required(VERSION 3.18)

project(CoffeeRobot)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Указываем, куда класть exe
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

set(SOURCES
    ./src/main.cpp
    ./src/server.cpp
    ./src/camera.cpp
    ./src/processor.cpp
    ./src/robot.cpp
    ./src/dispenser.cpp
)

set(HEADERS
    ./src/server.h
    ./src/camera.h
    ./src/processor.h
    ./src/robot.h
    ./src/dispenser.h
)

add_executable(${PROJECT_NAME} ${SOURCES} ${HEADERS})