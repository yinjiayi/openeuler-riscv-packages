# SPDX-License-Identifier: MIT
# Copyright (c) 2026 yinjiayi
cmake_minimum_required(VERSION 3.10)
project(tinycbor_installed_consumer C)
find_package(tinycbor 7.0 CONFIG REQUIRED)
if(NOT TARGET tinycbor)
  message(FATAL_ERROR "Original non-namespaced tinycbor imported target missing")
endif()
add_executable(consumer consumer.c)
target_compile_definitions(consumer PRIVATE USE_CMAKE_EXPORT)
target_compile_options(consumer PRIVATE -UNDEBUG)
target_link_libraries(consumer PRIVATE tinycbor)
