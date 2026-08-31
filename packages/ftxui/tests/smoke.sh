#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- ftxui ftxui-devel
test "$(rpm -q --qf '%{VERSION}' ftxui)" = '7.0.3'
test -s /usr/include/ftxui/dom/elements.hpp
test -s /usr/lib64/cmake/ftxui/ftxui-config.cmake
test "$(pkg-config --modversion ftxui)" = '7.0.3'

tmpdir=$(mktemp -d)
trap 'rm -rf -- "$tmpdir"' EXIT
cat >"$tmpdir/smoke.cc" <<'EOF'
#include <ftxui/dom/elements.hpp>
#include <ftxui/dom/node.hpp>
#include <ftxui/screen/screen.hpp>

#include <string>

int main() {
    using namespace ftxui;
    auto document = hbox({text("RISC-V"), separator(), text("FTXUI")}) | border;
    auto screen = Screen::Create(Dimension::Fixed(24), Dimension::Fixed(3));
    Render(screen, document);
    return screen.ToString().find("FTXUI") == std::string::npos ? 1 : 0;
}
EOF
read -r -a pkg_flags <<< "$(pkg-config --cflags --libs ftxui)"
${CXX:-c++} -std=c++17 ${CXXFLAGS:-} "$tmpdir/smoke.cc" \
  "${pkg_flags[@]}" -o "$tmpdir/smoke"
"$tmpdir/smoke"
