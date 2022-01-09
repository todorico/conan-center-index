cmake_minimum_required(VERSION 3.1)
project(test_package CXX)

find_package(${_pkg_name} ${_pkg_version} REQUIRED CONFIG)

add_executable(${PROJECT_NAME} test_package.cpp)
target_link_libraries(${PROJECT_NAME} PRIVATE ${_pkg_name}::${_pkg_name})

install(TARGETS ${PROJECT_NAME} DESTINATION ".")

include(FeatureSummary)
feature_summary(FATAL_ON_MISSING_REQUIRED_PACKAGES WHAT ALL)
