# SPDX-License-Identifier: MIT
# Copyright (c) 2026 yinjiayi
cmake_minimum_required(VERSION 3.11)
project(bioparser_installed_qa LANGUAGES CXX)
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
find_package(bioparser 3.1.0 REQUIRED CONFIG)
find_package(GTest 1.10.0 REQUIRED)
get_target_property(actual_includes bioparser::bioparser INTERFACE_INCLUDE_DIRECTORIES)
if(NOT actual_includes STREQUAL EXPECTED_INCLUDE)
  message(FATAL_ERROR "Wrong installed Bioparser include: ${actual_includes}")
endif()
if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/include/bioparser")
  message(FATAL_ERROR "Source headers must not shadow the installed target")
endif()
set(BIOPARSER_TEST_DATA "${CMAKE_CURRENT_SOURCE_DIR}/tests/data/")
configure_file(tests/bioparser_test_config.h.in bioparser_test_config.h)
add_executable(original_suite
  tests/parser_test.cpp tests/fasta_parser_test.cpp tests/fastq_parser_test.cpp
  tests/mhap_parser_test.cpp tests/paf_parser_test.cpp tests/sam_parser_test.cpp)
target_include_directories(original_suite PRIVATE
  "${CMAKE_CURRENT_BINARY_DIR}" "${CMAKE_CURRENT_SOURCE_DIR}/biosoup/include")
target_link_libraries(original_suite PRIVATE bioparser::bioparser GTest::Main)
add_executable(installed_consumer consumer.cpp)
target_link_libraries(installed_consumer PRIVATE bioparser::bioparser)
