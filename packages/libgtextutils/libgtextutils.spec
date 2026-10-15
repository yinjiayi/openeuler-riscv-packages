# SPDX-License-Identifier: Apache-2.0
Name:           libgtextutils
Version:        0.7
Release:        1%{?dist}
Summary:        Gordon text utility streams, natural sorting and tokenization
License:        AGPL-3.0-or-later AND Zlib AND LicenseRef-Josuttis-1999
URL:            https://github.com/agordon/libgtextutils
Source0:        https://codeload.github.com/agordon/libgtextutils/tar.gz/1f03f41e7c4740164aae44570fa8d05c3f3e7ed6#/libgtextutils-0.7.tar.gz
Patch0:         0001-preserve-stream-and-sort-interfaces-with-current-cxx.patch
BuildRequires:  gcc gcc-c++ glibc-devel libstdc++-devel make autoconf automake libtool
BuildRequires:  pkgconf gzip coreutils findutils grep sed patch binutils

%description
Text utility streams, natural string comparisons, tokenization and container
formatting. Original default features, debug and strict warnings are retained.

%package devel
Summary:        Development files and installed-library original tests
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       gcc gcc-c++ glibc-devel libstdc++-devel pkgconf gzip coreutils grep

%description devel
Headers, pkg-config metadata, static/link libraries and original default test
sources, replayed against the installed shared library with assertions.

%prep
%setup -q -n libgtextutils-1f03f41e7c4740164aae44570fa8d05c3f3e7ed6
%patch -P 0 -p1
autoreconf --force --install --verbose
cat > run-installed-tests.sh <<'SH'
#!/usr/bin/env bash
set -euo pipefail
root=${1:-}
test -z "$root" || test "${root:0:1}" = /
sources="$root/usr/share/libgtextutils/tests"
cd "$sources"
sha256sum -c SHA256SUMS
work=$(mktemp -d)
trap 'rm -rf -- "$work"' EXIT
flags=(-O1 -g -DDEBUG -UNDEBUG -Wall -Wextra -Wformat-nonliteral -Wformat-security -Wswitch-default -Wswitch-enum -Wunused-parameter -Wfloat-equal -Werror)
read -r -a cflags <<< "$(PKG_CONFIG_SYSROOT_DIR="$root" PKG_CONFIG_LIBDIR="$root/usr/lib64/pkgconfig" pkg-config --cflags gtextutils)"
read -r -a libs <<< "$(PKG_CONFIG_SYSROOT_DIR="$root" PKG_CONFIG_LIBDIR="$root/usr/lib64/pkgconfig" pkg-config --libs gtextutils)"
programs=(test_container_join test_natural_sort test_input_stream_wrapper test_text_reader test_text_reader_unget test_fd_outbuf test_fd_inbuf test_in_out_buf test_pipe_fitter test_string_tokenize)
linked_programs=0
for testname in "${programs[@]}"; do
    if test "$testname" = test_pipe_fitter; then
        gcc "${flags[@]}" "${cflags[@]}" "$sources/$testname.c" "${libs[@]}" -o "$work/$testname"
    else
        g++ -std=gnu++17 "${flags[@]}" "${cflags[@]}" "$sources/$testname.cpp" "${libs[@]}" -o "$work/$testname"
    fi
    ldd "$work/$testname" > "$work/$testname.ldd"
    linked=$(awk '$1 == "libgtextutils-0.7.so.0" && $2 == "=>" {print $3}' "$work/$testname.ldd")
    # Header-only tests may have no DT_NEEDED entry with --as-needed.
    if test -n "$linked"; then
        test "$(readlink -f "$linked")" = "$(readlink -f "$root/usr/lib64/libgtextutils-0.7.so.0")"
        linked_programs=$((linked_programs + 1))
    fi
    mkdir "$work/$testname-work"
    (cd "$work/$testname-work"; printf 'first line\nsecond line\nthird line\nfourth line\n' > test.txt; "$work/$testname")
    printf 'PASS installed-original %s\n' "$testname"
done
test "$linked_programs" -gt 0
printf 'PASS installed-original programs=10 skips=0 assertions=enabled\n'
SH

%build
# Keep upstream default wall/debug and tuple-parser-check=false. Modernize
# interfaces rather than suppressing warnings or lowering the C++ language.
%configure CFLAGS="%{optflags} -UNDEBUG" CXXFLAGS="%{optflags} -UNDEBUG -std=gnu++17"
%make_build

%install
%make_install
find %{buildroot}%{_libdir} -name '*.la' -delete
install -d %{buildroot}%{_datadir}/libgtextutils/tests
install -m 0644 tests/*.cpp tests/*.c tests/tests_assertion.h %{buildroot}%{_datadir}/libgtextutils/tests/
install -m 0755 run-installed-tests.sh %{buildroot}%{_datadir}/libgtextutils/tests/
(cd %{buildroot}%{_datadir}/libgtextutils/tests; sha256sum -- *.cpp *.c tests_assertion.h > SHA256SUMS)

%check
# No TESTS/check_PROGRAMS override: all ten original default Automake programs.
make -j1 check VERBOSE=1
for name in test_container_join test_natural_sort test_input_stream_wrapper test_text_reader test_text_reader_unget test_fd_outbuf test_fd_inbuf test_in_out_buf test_pipe_fitter test_string_tokenize; do
    cat "tests/$name.log"
    grep -Fx ':test-result: PASS' "tests/$name.trs"
done
grep -Eq '^# TOTAL: *10$' tests/test-suite.log
grep -Eq '^# PASS: *10$' tests/test-suite.log
grep -Eq '^# SKIP: *0$' tests/test-suite.log
grep -Eq '^# FAIL: *0$' tests/test-suite.log
LD_LIBRARY_PATH="%{buildroot}%{_libdir}" bash %{buildroot}%{_datadir}/libgtextutils/tests/run-installed-tests.sh "%{buildroot}"

%files
%license COPYING src/gtextutils/strnatcmp.c src/gtextutils/strnatcmp.h src/gtextutils/inbuf1.hpp src/gtextutils/outbuf3.hpp
%doc AUTHORS README NEWS THANKS
%{_libdir}/libgtextutils-0.7.so.0*

%files devel
%{_includedir}/gtextutils/
%{_libdir}/libgtextutils.so
%{_libdir}/libgtextutils.a
%{_libdir}/pkgconfig/gtextutils.pc
%{_datadir}/libgtextutils/

%changelog
* Thu Oct 15 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.7-1
- Pin official source, retain complete default tests and strict flags.
- Preserve modern stream/comparator interfaces and initialize one test buffer.
