# SPDX-License-Identifier: Apache-2.0
Name:           libptytty
Version:        2.0
Release:        1%{?dist}
Summary:        Portable pseudo-terminal and session handling library
License:        GPL-2.0-or-later AND BSD-2-Clause AND MIT
URL:            https://software.schmorp.de/pkg/libptytty.html
Source0:        libptytty-2.0.tar.gz
BuildRequires:  bash
BuildRequires:  binutils
BuildRequires:  cmake
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  glibc-devel
BuildRequires:  grep
BuildRequires:  make
BuildRequires:  sed
BuildRequires:  tar
BuildRequires:  gzip
BuildRequires:  util-linux
Requires:       bash
Requires:       coreutils
Requires:       util-linux

%description
libptytty offers C and C++ pseudo-terminal management and optional session
database handling. This package retains the original shared-library, helper,
reentrant and session-feature defaults. Its added functional test uses only
an unprivileged PTY pair, without starting a shell or a login session.

%package devel
Summary:        Development files for libptytty
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Public header, unversioned library link and pkg-config metadata for libptytty.

%prep
%autosetup -p1
# Preserve all19 original members before CMake generation; suffixes prevent
# basename-matching helper replacement from rewriting retained notices.
mkdir license-notices
for original in Changes CMakeLists.txt COPYING README config.h.cmake libptytty.pc.in doc/libptytty.3.pod doc/libptytty.3 eg/c-sample.c src/logging.C src/fdpass.C src/libptytty.h src/c-api.C src/ptytty.C src/ptytty_conf.h src/estl.h src/ecb.h src/ptytty.h src/proxy.C; do
    install -D -m0644 "$original" "license-notices/$original.notice"
done
(cd license-notices; sha256sum ./*.notice doc/*.notice eg/*.notice src/*.notice) > original-source.sha256
mv original-source.sha256 license-notices/SHA256SUMS
cat > api-smoke.c <<'API_EOF'
/* SPDX-License-Identifier: MIT
 * Copyright (c) 2026 openEuler RISC-V package contributors
 * Permission is hereby granted, free of charge, to any person obtaining a
 * copy of this software and associated documentation files (the "Software"),
 * to deal in the Software without restriction, including without limitation
 * the rights to use, copy, modify, merge, publish, distribute, sublicense,
 * and/or sell copies of the Software, and to permit persons to whom the
 * Software is furnished to do so, subject to the following conditions:
 * The above copyright notice and this permission notice shall be included
 * in all copies or substantial portions of the Software.
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
 * OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
 * THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 * FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
 * DEALINGS IN THE SOFTWARE.
 */
#define _DEFAULT_SOURCE 1
#include <libptytty.h>
#include <assert.h>
#include <errno.h>
#include <fcntl.h>
#include <poll.h>
#include <stdio.h>
#include <string.h>
#include <termios.h>
#include <unistd.h>

static void transfer(int output, int input, const unsigned char *bytes, size_t count) {
    size_t offset = 0;
    while (offset < count) {
        ssize_t n = write(output, bytes + offset, count - offset);
        if (n < 0 && errno == EINTR) continue;
        assert(n > 0);
        offset += (size_t)n;
    }
    unsigned char actual[64];
    assert(count <= sizeof actual);
    offset = 0;
    while (offset < count) {
        struct pollfd ready = {input, POLLIN, 0};
        int result;
        do { result = poll(&ready, 1, 5000); } while (result < 0 && errno == EINTR);
        assert(result == 1 && (ready.revents & POLLIN));
        ssize_t n = read(input, actual + offset, count - offset);
        if (n < 0 && errno == EINTR) continue;
        assert(n > 0);
        offset += (size_t)n;
    }
    assert(memcmp(actual, bytes, count) == 0);
}

int main(void) {
    /* Upstream requires init first. No setuid/setgid binary is installed. */
    ptytty_init();
    assert(getuid() != 0 && getuid() == geteuid() && getgid() == getegid());
    PTYTTY pair = ptytty_create();
    assert(pair && ptytty_pty(pair) == -1 && ptytty_tty(pair) == -1);
    puts("PASS: unprivileged initialization and empty object");
    assert(ptytty_get(pair) != 0);
    int master = ptytty_pty(pair), slave = ptytty_tty(pair);
    assert(master >= 0 && slave >= 0 && master != slave);
    assert(fcntl(master, F_GETFD) >= 0 && fcntl(slave, F_GETFD) >= 0);
    assert(isatty(master) == 1 && isatty(slave) == 1);
    puts("PASS: allocated PTY descriptors");
    struct termios original, raw, observed;
    assert(tcgetattr(slave, &original) == 0);
    raw = original;
    cfmakeraw(&raw);
    assert(tcsetattr(slave, TCSANOW, &raw) == 0);
    const unsigned char incoming[] = {0, 1, 10, 13, 127, 128, 255, 'i', 'n'};
    transfer(master, slave, incoming, sizeof incoming);
    puts("PASS: master to raw slave exact bytes");
    const unsigned char outgoing[] = {'o', 'u', 't', 0, 10, 13, 128, 255};
    transfer(slave, master, outgoing, sizeof outgoing);
    puts("PASS: raw slave to master exact bytes");
#ifndef IUTF8
#error Linux target must expose IUTF8 for this explicit functional case
#endif
    ptytty_set_utf8_mode(pair, 1);
    assert(tcgetattr(master, &observed) == 0 && (observed.c_iflag & IUTF8));
    ptytty_set_utf8_mode(pair, 0);
    assert(tcgetattr(master, &observed) == 0 && !(observed.c_iflag & IUTF8));
    assert(tcsetattr(slave, TCSANOW, &original) == 0);
    puts("PASS: UTF8 input flag on and off");
    ptytty_close_tty(pair);
    assert(ptytty_tty(pair) == -1);
    errno = 0;
    assert(fcntl(slave, F_GETFD) == -1 && errno == EBADF);
    ptytty_close_tty(pair);
    ptytty_delete(pair);
    errno = 0;
    assert(fcntl(master, F_GETFD) == -1 && errno == EBADF);
    puts("PASS: idempotent slave close and object teardown");
    return 0;
}
API_EOF
sed -n '1,/^ \*\//p' api-smoke.c > PACKAGING-COPYING

%build
# Preserve every original option/probe, session support and default C-sample.
cmake -S . -B build -DCMAKE_INSTALL_PREFIX=%{_prefix} -DCMAKE_INSTALL_LIBDIR=%{_lib} \
    -DCMAKE_C_FLAGS="%{optflags}" -DCMAKE_CXX_FLAGS="%{optflags}" \
    -DCMAKE_EXE_LINKER_FLAGS="%{?build_ldflags}" -DCMAKE_SHARED_LINKER_FLAGS="%{?build_ldflags}"
cmake --build build --parallel %{?_smp_build_ncpus}
gcc %{optflags} -UNDEBUG -Isrc api-smoke.c -Lbuild \
    -Wl,-rpath-link,"$PWD/build" %{?build_ldflags} -lptytty -o api-smoke

%install
DESTDIR=%{buildroot} cmake --install build
install -D -m0755 api-smoke %{buildroot}%{_libexecdir}/libptytty-tests/api-smoke
install -m0644 api-smoke.c %{buildroot}%{_libexecdir}/libptytty-tests/api-smoke.c

%check
(cd license-notices; sha256sum -c SHA256SUMS)
test "$(wc -l < license-notices/SHA256SUMS)" -eq 19
grep -Fx 'BUILD_SHARED_LIBS:BOOL=ON' build/CMakeCache.txt
grep -Fx 'UTMP_SUPPORT:BOOL=ON' build/CMakeCache.txt
grep -Fx 'WTMP_SUPPORT:BOOL=ON' build/CMakeCache.txt
grep -Fx 'LASTLOG_SUPPORT:BOOL=ON' build/CMakeCache.txt
test -x build/c-sample
test -f build/libptytty.so.0
# Upstream defines no CTest/check target or runtime cases; none is removed.
# C-sample is built, not executed: it logs in and starts a shell.
LD_LIBRARY_PATH="$PWD/build${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}" ./api-smoke
# Bind actual post-install-post/stripping bytes, not the prestrip build binary.
(cd %{buildroot}%{_libexecdir}/libptytty-tests; sha256sum api-smoke api-smoke.c > SHA256SUMS)

%files
%license COPYING PACKAGING-COPYING license-notices
%doc README Changes
%{_libdir}/libptytty.so.0
%{_libexecdir}/libptytty-tests/

%files devel
%{_includedir}/libptytty.h
%{_libdir}/libptytty.so
%{_libdir}/pkgconfig/libptytty.pc
%{_mandir}/man3/libptytty.3*

%changelog
* Sat Oct 24 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.0-1
- Pin official stable source; preserve original notices, defaults and sample.
