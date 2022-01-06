cmake_minimum_required(VERSION 3.1)

project(test_package C)

include(FeatureSummary)

# find_package(PkgConfig REQUIRED)
# pkg_check_modules(GPG_ERROR REQUIRED gpg-error)
# find_library(MY_LIBRARY NAMES gpg-error)
find_package(${_package_name} ${_package_version} REQUIRED CONFIG)

add_executable(${PROJECT_NAME} test_package.c)

target_link_libraries(${PROJECT_NAME} PRIVATE ${_package_name}::${_package_name})

# message(STATUS "LIBRARIES: \${${GPG_ERROR}_LIBRARIES}")

feature_summary(FATAL_ON_MISSING_REQUIRED_PACKAGES WHAT ALL)
