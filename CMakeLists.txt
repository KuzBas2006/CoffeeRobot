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
    GIT_SHALLOW TRUE
)

FetchContent_MakeAvailable(nlohmann_json)

FetchContent_Declare(
  httplib
  GIT_REPOSITORY https://github.com/yhirose/cpp-httplib.git
  GIT_SHALLOW    TRUE
  GIT_TAG v0.21.0 # Use a specific tag, commit hash, or branch
)
  
FetchContent_MakeAvailable(httplib)


add_executable(${PROJECT_NAME} ${SOURCES} ${HEADERS})

# On Windows ensure WSAPoll is exposed and link Winsock library
if (WIN32)
  # Require at least Windows 7 APIs (WSAPoll is available on Vista+/Server2008+)
  target_compile_definitions(${PROJECT_NAME} PRIVATE _WIN32_WINNT=0x0601 WIN32_LEAN_AND_MEAN)
  target_link_libraries(${PROJECT_NAME} PRIVATE Ws2_32)
endif()

# Подключаем nlohmann/json
target_link_libraries(${PROJECT_NAME} PRIVATE nlohmann_json::nlohmann_json)
target_link_libraries(${PROJECT_NAME} PRIVATE httplib)