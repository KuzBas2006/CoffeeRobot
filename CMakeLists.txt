cmake_minimum_required(VERSION 3.18)

project(CoffeeRobot)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
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

# Подключаем nlohmann/json через FetchContent
include(FetchContent)
FetchContent_Declare(
    nlohmann_json
    GIT_REPOSITORY https://github.com/nlohmann/json.git
    GIT_TAG v3.11.3
    GIT_SHALLOW TRUE
)

FetchContent_MakeAvailable(nlohmann_json)

add_executable(${PROJECT_NAME} ${SOURCES} ${HEADERS})

# Подключаем nlohmann/json
target_link_libraries(${PROJECT_NAME} PRIVATE nlohmann_json::nlohmann_json)
