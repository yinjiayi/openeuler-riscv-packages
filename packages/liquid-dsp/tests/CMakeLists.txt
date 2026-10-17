# SPDX-License-Identifier: MIT
# Copyright (c) 2026 yinjiayi
cmake_minimum_required(VERSION 3.10)
project(liquid_installed_consumer C)
find_package(liquid 1.8.3 EXACT CONFIG REQUIRED)
if(NOT TARGET liquid::liquid)
    message(FATAL_ERROR "Missing original exported liquid::liquid target")
endif()
add_executable(consumer consumer.c)
target_compile_features(consumer PRIVATE c_std_11)
target_link_libraries(consumer PRIVATE liquid::liquid m)
