<!-- SPDX-License-Identifier: Apache-2.0 -->
# ember-plus

This directory packages upstream `https://github.com/Lawo/ember-plus` version `1.8.2.2` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

The complete aggregate CMake project builds the Ember libraries and both
TinyEmber applications. Because upstream only adds its four libember self-test
programs when libember is configured as the top-level project, the RPM build
creates a separate test build and executes every one of those programs.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
