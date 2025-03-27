cmake_minimum_required(VERSION 3.5)
project(loadcell)

# Default to C++14
set(CMAKE_CXX_STANDARD 14)

# Find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclpy REQUIRED)
find_package(geometry_msgs REQUIRED)

# Install Python executables
install(PROGRAMS
  scripts/PublishWrench.py
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
