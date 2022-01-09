cmake_minimum_required(VERSION 3.1)
project(test_package CXX)

# Print tested package info
message(STATUS "Tested package informations:")
message("")
foreach(var IN LISTS _pkg_variables)
    message(" * ${var} = \"${${var}}\"")
endforeach()
message("")

# Find tested package
find_package(${_pkg_cmake_file_name} ${_pkg_version} REQUIRED CONFIG)

# Print required package(s) info
include(FeatureSummary)
feature_summary(FATAL_ON_MISSING_REQUIRED_PACKAGES WHAT ALL)

# Build test program
add_executable(${PROJECT_NAME} test_package.cpp)
target_link_libraries(${PROJECT_NAME} PRIVATE ${_pkg_cmake_target_name})

# Install test program in package folder
install(TARGETS ${PROJECT_NAME} DESTINATION ".")
