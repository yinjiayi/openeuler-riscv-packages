# SPDX-License-Identifier: LGPL-2.1-or-later
# Copyright (c) 2026 yinjiayi
cmake_minimum_required(VERSION 3.14)
project(claw_installed_consumer LANGUAGES CXX)
find_package(claw 1.9 REQUIRED)
add_executable(consumer consumer.cpp)
target_compile_features(consumer PRIVATE cxx_std_11)
target_compile_options(consumer PRIVATE -UNDEBUG)
target_link_libraries(consumer PRIVATE claw_application claw_configuration_file
  claw_dynamic_library claw_graphic claw_logger claw_net claw_tween claw_core)
