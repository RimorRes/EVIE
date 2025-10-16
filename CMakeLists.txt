cmake_minimum_required(VERSION 4.0)
project(EVIE)

set(CMAKE_CXX_STANDARD 20)

add_executable(EVIE
        src/evie.cpp
)
target_include_directories(${PROJECT_NAME} PRIVATE /include)
