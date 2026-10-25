# SPDX-License-Identifier: Apache-2.0
%global debug_package %{nil}

Name:           termox
Version:        2.0.0
Release:        5%{?dist}
Summary:        C++20 terminal UI static library with private pinned dependencies
License:        MIT
URL:            https://github.com/a-n-t-h-o-n-y/TermOx
Source0:        termox-2.0.0.tar.gz
Source1:        zzz-9d7c047f47c81a95a5ea824075253618356593a2.tar.gz
Source2:        Escape-f797e8194b531663f01873f43007d2439fa89276.tar.gz
Source3:        signals-light-5b873d0aa515a2085138359e69746cd7d7a5362f.tar.gz
BuildRequires:  bash
BuildRequires:  binutils
BuildRequires:  cmake
BuildRequires:  coreutils
BuildRequires:  diffutils
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  git
BuildRequires:  glibc-devel
BuildRequires:  grep
BuildRequires:  libicu-devel
BuildRequires:  make
BuildRequires:  pkgconf-pkg-config
BuildRequires:  sed
BuildRequires:  tar
BuildRequires:  gzip
# Static installed-consumer QA is an explicit developer/test contract.
Requires:       bash
Requires:       binutils
Requires:       coreutils
Requires:       diffutils
Requires:       grep
Requires:       sed
Requires:       gcc-c++
Requires:       libicu-devel
Requires:       pkgconf-pkg-config

%description
TermOx is a C++ terminal user interface static library. The exact upstream
Escape, zzz and signals-light dependencies are installed in a package-private
layout. Its installed consumer requires C++20 and ICU development inputs.

%prep
%setup -q -n TermOx-%{version}
# Preserve original files before creating API code or running configuration.
mkdir .source-notices
find . -path './.source-notices' -prune -o -type f -printf '%%P\n' | LC_ALL=C sort > ../termox-original-files
while IFS= read -r p; do
    install -Dpm 0644 "$p" ".source-notices/TermOx/$p.notice"
done < ../termox-original-files
mkdir -p .packaging-deps/zzz .packaging-deps/Escape .packaging-deps/signals-light
tar -xzf %{SOURCE1} --strip-components=1 -C .packaging-deps/zzz
tar -xzf %{SOURCE2} --strip-components=1 -C .packaging-deps/Escape
tar -xzf %{SOURCE3} --strip-components=1 -C .packaging-deps/signals-light
for project in zzz Escape signals-light; do
    find ".packaging-deps/$project" -type f -printf '%%P\n' | LC_ALL=C sort > "../$project-original-files"
    while IFS= read -r p; do
        install -Dpm 0644 ".packaging-deps/$project/$p" ".source-notices/$project/$p.notice"
    done < "../$project-original-files"
done
test "$(find .source-notices/TermOx -type f | grep -c '\.notice$')" -eq 55
test "$(find .source-notices/zzz -type f | grep -c '\.notice$')" -eq 19
test "$(find .source-notices/Escape -type f | grep -c '\.notice$')" -eq 43
test "$(find .source-notices/signals-light -type f | grep -c '\.notice$')" -eq 9
(cd .source-notices; find . -type f -name '*.notice' -printf '%%P\n' | LC_ALL=C sort | while IFS= read -r p; do sha256sum "$p"; done > SHA256SUMS; sha256sum -c SHA256SUMS)
%autopatch -p1
cat > .packaging-api.cpp <<'TERMOX_API_EOF'
// SPDX-License-Identifier: MIT
// Proposed additional target-only QA, not an upstream test or locally run result.
// No Terminal/Timer construction, interactive I/O, threads, or network.
#include <ox/core/terminal.hpp>
#include <ox/core/glyph.hpp>
#include <signals_light/signal.hpp>
#include <cstdio>
#include <cstdlib>
#include <stdexcept>
#include <string_view>

static void require(bool ok, char const* what) {
    if (!ok) { std::fprintf(stderr, "TermOx API failure: %s\n", what); std::exit(1); }
}
static void passed(int n, char const* name) {
    std::printf("TERMOX_API_CASE_%d %s PASS\n", n, name);
}
int main() {
    std::setvbuf(stdout, nullptr, _IONBF, 0);
    ox::ScreenBuffer b{ox::Area{3, 2}};
    require(b.size() == ox::Area{3, 2}, "constructor dimensions");
    for (int y = 0; y != 2; ++y)
        for (int x = 0; x != 3; ++x)
            require(b[ox::Point{x, y}] == ox::Glyph{}, "default cell");
    ox::Glyph const fill{.symbol = U'λ'};
    b.fill(fill);
    for (int y = 0; y != 2; ++y)
        for (int x = 0; x != 3; ++x)
            require(b[ox::Point{x, y}] == fill, "fill all six cells");
    passed(1, "construct-and-fill");

    b[ox::Point{2, 1}] = ox::Glyph{.symbol = U'X'};
    ox::ScreenBuffer const& cb = b;
    require(cb[ox::Point{2, 1}].symbol == U'X', "const access sees mutation");
    require(cb[ox::Point{1, 1}] == fill && cb[ox::Point{2, 0}] == fill,
            "distinct row/column cells unchanged");
    passed(2, "mutable-and-const-index");

    ox::Canvas c{.buffer = b, .at = {1, 0}, .size = {2, 2}};
    c[ox::Point{1, 1}] = ox::Glyph{.symbol = U'Ω'};
    ox::Canvas const& cc = c;
    require(cc[ox::Point{1, 1}].symbol == U'Ω', "const Canvas access");
    require(cb[ox::Point{2, 1}].symbol == U'Ω', "Canvas exact translated index");
    require(cb[ox::Point{1, 1}] == fill, "Canvas adjacent cell untouched");
    passed(3, "canvas-offset");

    b.resize(ox::Area{2, 3});
    require(b.size() == ox::Area{2, 3}, "resize dimensions");
    // Upstream explicitly does not promise preserved resize contents: fill
    // before reading, rather than asserting invented preservation semantics.
    b.fill(ox::Glyph{.symbol = U'R'});
    for (int y = 0; y != 3; ++y)
        for (int x = 0; x != 2; ++x)
            require(cb[ox::Point{x, y}].symbol == U'R', "resized fill");
    passed(4, "resize-then-fill");

    using ox::operator""_gs;
    auto glyphs = "Aλ"_gs;
    require(glyphs.size() == 2 && glyphs[0].symbol == U'A' && glyphs[1].symbol == U'λ',
            "UTF-8 glyph conversion");
    require(esc::detail::u32_to_u8(U'λ') == "λ", "Unicode reverse conversion");
    bool rejected = false;
    try { (void)esc::detail::utf8_to_glyphs(std::string_view{"\xff", 1}); }
    catch (std::runtime_error const&) { rejected = true; }
    require(rejected, "invalid UTF-8 rejected by original decoder");
    passed(5, "unicode-and-invalid-input");

    int total = 0;
    sl::Signal<void(int)> signal;
    auto id = signal.connect([&](int v) { total += v; });
    signal(3); require(total == 3 && signal.slot_count() == 1, "signal delivery");
    auto removed = signal.disconnect(id);
    signal(4); require(total == 3 && signal.is_empty(), "disconnected slot not called");
    removed(2); require(total == 5, "returned slot retains callable");
    {
        sl::Lifetime life;
        sl::Slot<void(int)> tracked{[&](int v) { total += v; }};
        tracked.track(life);
        (void)signal.connect(tracked);
        signal(2); require(total == 7, "live tracked slot");
    }
    signal(9); require(total == 7, "expired tracked slot not invoked");
    passed(6, "signal-disconnect-and-lifetime");
    std::puts("TERMOX_API_TOTAL=6 PASS");
    return 0;
}
TERMOX_API_EOF

%build
%set_build_flags
%cmake -S . -B %{_vpath_builddir} \
    -DFETCHCONTENT_FULLY_DISCONNECTED=ON \
    -DFETCHCONTENT_SOURCE_DIR_ZZZ="$PWD/.packaging-deps/zzz" \
    -DFETCHCONTENT_SOURCE_DIR_ESCAPE="$PWD/.packaging-deps/Escape" \
    -DFETCHCONTENT_SOURCE_DIR_SIGNALS-LIGHT="$PWD/.packaging-deps/signals-light"
%cmake_build
# Original recipe explicitly selected this upstream EXCLUDE_FROM_ALL target.
%cmake_build --target TermOx.tests.unit

${CXX:-c++} $CXXFLAGS -std=c++20 -pthread \
    -I include -I .packaging-deps/zzz/include \
    -I .packaging-deps/Escape/include -I .packaging-deps/signals-light/include \
    .packaging-api.cpp %{_vpath_builddir}/libTermOx.a \
    %{_vpath_builddir}/_deps/escape-build/libescape.a \
    $(pkg-config --libs icu-uc icu-i18n) $LDFLAGS -o .packaging-api

%check
%{_vpath_builddir}/tests/TermOx.tests.unit
printf 'TERMOX_ORIGINAL_REGISTERED=2 EFFECTIVE_ASSERTIONS=0\n'
if ./.packaging-api > .packaging-api.stdout 2> .packaging-api.stderr; then
    api_status=0
else
    api_status=$?
fi
cat .packaging-api.stdout .packaging-api.stderr
test "$api_status" -eq 0
test ! -s .packaging-api.stderr
cat > .packaging-api.expected <<'TERMOX_EXPECTED_EOF'
TERMOX_API_CASE_1 construct-and-fill PASS
TERMOX_API_CASE_2 mutable-and-const-index PASS
TERMOX_API_CASE_3 canvas-offset PASS
TERMOX_API_CASE_4 resize-then-fill PASS
TERMOX_API_CASE_5 unicode-and-invalid-input PASS
TERMOX_API_CASE_6 signal-disconnect-and-lifetime PASS
TERMOX_API_TOTAL=6 PASS
TERMOX_EXPECTED_EOF
cmp .packaging-api.expected .packaging-api.stdout

%install
install -Dpm 0644 %{_vpath_builddir}/libTermOx.a %{buildroot}%{_libdir}/libTermOx.a
install -Dpm 0644 %{_vpath_builddir}/_deps/escape-build/libescape.a %{buildroot}%{_libdir}/termox/libescape.a
install -d %{buildroot}%{_includedir} %{buildroot}%{_includedir}/termox/third-party
cp -a include/ox %{buildroot}%{_includedir}/
cp -a .packaging-deps/zzz/include/zzz %{buildroot}%{_includedir}/termox/third-party/
cp -a .packaging-deps/Escape/include/esc %{buildroot}%{_includedir}/termox/third-party/
cp -a .packaging-deps/signals-light/include/signals_light %{buildroot}%{_includedir}/termox/third-party/
install -Dpm 0755 .packaging-api %{buildroot}%{_libexecdir}/termox/api-smoke
install -Dpm 0644 .packaging-api.cpp %{buildroot}%{_datadir}/termox-tests/api-smoke.cpp
install -d %{buildroot}%{_datadir}/licenses/termox
cp -a .source-notices %{buildroot}%{_datadir}/licenses/termox/source-notices
install -d %{buildroot}%{_libdir}/pkgconfig
cat > %{buildroot}%{_libdir}/pkgconfig/termox.pc <<'TERMOX_PC_EOF'
prefix=%{_prefix}
libdir=%{_libdir}
includedir=%{_includedir}

Name: TermOx
Description: TermOx static library with package-private pinned dependencies
Version: %{version}
Requires: icu-uc icu-i18n
Libs: -L${libdir} -lTermOx ${libdir}/termox/libescape.a -pthread
Cflags: -std=c++20 -I${includedir} -I${includedir}/termox/third-party -pthread
TERMOX_PC_EOF
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%files -f %{name}.files
%license LICENSE
%doc README.md

%changelog
* Sun Oct 25 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.0.0-5
- Pin all original dependency archives for offline unprivileged configuration.
- Preserve all 126 source notices and complete installed static-consumer closure.
- Retain the original two no-op tests and add six strict noninteractive API cases.
