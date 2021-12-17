cmake_minimum_required(VERSION 3.1)

project(test_package C)

find_package(${_package_name} ${_package_version} REQUIRED CONFIG)

add_executable(${PROJECT_NAME} test_package.c)

target_link_libraries(${PROJECT_NAME} ${_package_name}::${_package_name})
