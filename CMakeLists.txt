cmake_minimum_required(VERSION 3.8)
project(stick_balancing)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclpy REQUIRED)
find_package(std_msgs REQUIRED)



if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  set(ament_cmake_copyright_FOUND TRUE)
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()


install(PROGRAMS
  src/main_position.py
  src/main_velocity.py
  src/stick_balance.py
  DESTINATION lib/${PROJECT_NAME}
  # PERMISSIONS OWNER_READ OWNER_WRITE OWNER_EXECUTE
  # GROUP_READ GROUP_WRITE GROUP_EXECUTE
  # WORLD_READ WORLD_WRITE WORLD_EXECUTE
)

install (DIRECTORY
  launch 
  urdf
  worlds
  config
DESTINATION share/${PROJECT_NAME}/
)
