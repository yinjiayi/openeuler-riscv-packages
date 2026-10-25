// SPDX-License-Identifier: LGPL-2.1-or-later
// Copyright (c) 2026 yinjiayi
#include <claw/version.hpp>
#include <claw/graphic/image.hpp>
#include <claw/tween/easing/easing_linear.hpp>
#include <cassert>
#include <cmath>
int main() {
  static_assert(CLAW_MAJOR_VERSION == 1 && CLAW_MINOR_VERSION == 9 &&
                CLAW_RELEASE_NUMBER == 0, "Original tag1.9.1 reports project1.9.0");
  claw::graphic::image image(3, 2);
  assert(image.width() == 3 && image.height() == 2);
  assert(std::isfinite(claw::tween::easing_linear_func(0.25)));
  assert(claw::tween::easing_linear_func(0.25) == 0.25);
  return 0;
}
