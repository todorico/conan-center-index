cmake_minimum_required(VERSION 3.1)

project(test_package CXX)

include(FeatureSummary)

find_package(${_package_name} ${_package_version} REQUIRED CONFIG)

if (VTK_VERSION VERSION_LESS "8.90.0")
  # old system
    # include(${VTK_USE_FILE})

    add_executable(${PROJECT_NAME} test_package.cpp)

    target_link_libraries(${PROJECT_NAME} PRIVATE ${${_package_name}_LIBRARIES})

endif()

feature_summary(FATAL_ON_MISSING_REQUIRED_PACKAGES WHAT ALL)
