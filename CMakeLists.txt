cmake_minimum_required(VERSION 3.18)

project(CoffeeRobot)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

# Подключаем RapidJSON через FetchContent
include(FetchContent)

FetchContent_Declare(
    rapidjson
    GIT_REPOSITORY https://github.com/Tencent/rapidjson.git
    GIT_TAG v1.1.0
)

FetchContent_MakeAvailable(rapidjson)

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

add_executable(${PROJECT_NAME} ${SOURCES} ${HEADES})

target_include_directories(${PROJECT_NAME} PRIVATE ${rapidjson_SOURCE_DIR}/include)

target_compile_definitions(${PROJECT_NAME} PRIVATE RAPIDJSON_HAS_STDSTRING=1)