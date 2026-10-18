# SPDX-License-Identifier: Apache-2.0
Name:           libgeneral
Version:        90
Release:        1%{?dist}
Summary:        Common C++ utilities for tihmstar tools
License:        LGPL-2.1-only
URL:            https://github.com/tihmstar/libgeneral
Source0:        https://codeload.github.com/tihmstar/libgeneral/tar.gz/81e4636784f1bc3fda6a90911fc15bf529975577#/libgeneral-90.tar.gz
Patch0:         0001-fixed-release-version-and-consumer-link-flags.patch
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  glibc-devel
BuildRequires:  make
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  pkgconf
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  grep
BuildRequires:  sed
BuildRequires:  patch
BuildRequires:  binutils


%description
Common C++ utilities including exceptions, memory buffers, byte-order helpers,
events, guarded access and manager interfaces. The full default build is retained.

%package devel
Summary:        Headers, static library and downstream libgeneral consumer
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       gcc-c++ glibc-devel pkgconf binutils coreutils grep gawk

%description devel
All original public headers, shared linking interface, static library,
pkg-config metadata and an explicitly downstream deterministic API fixture.

%prep
%setup -q -n libgeneral-81e4636784f1bc3fda6a90911fc15bf529975577
%patch -P 0 -p1
mkdir -p m4
autoreconf --force --install --verbose
cat > verify-general.cpp <<'CPP'
#include <libgeneral/macros.h>
#include <libgeneral/exception.hpp>
#include <libgeneral/ByteOrder.hpp>
#include <libgeneral/Event.hpp>
#include <libgeneral/DeliveryEvent.hpp>
#include <libgeneral/GuardAccess.hpp>
#include <libgeneral/Manager.hpp>
#include <libgeneral/Mem.hpp>
#include <libgeneral/Utils.hpp>
#include <cstring>
#include <cstdlib>
#include <iostream>
#include <utility>
#define CHECK(x) do { if (!(x)) { std::cerr << "FAIL " #x << '\n'; std::exit(1); } ++checks; } while (0)
int main() {
    int checks = 0;
    const unsigned char bytes[] = {1, 2, 3, 4};
    tihmstar::Mem m(static_cast<const void*>(bytes), sizeof(bytes));
    CHECK(m.size() == 4);
    CHECK(std::memcmp(m.data(), bytes, 4) == 0);
    tihmstar::Mem copy(m);
    m.data()[0] = 9;
    CHECK(copy.data()[0] == 1);
    copy.append(bytes, 2);
    CHECK(copy.size() == 6 && copy.data()[4] == 1 && copy.data()[5] == 2);
    copy.appendSize(2);
    CHECK(copy.size() == 8 && copy.data()[6] == 0 && copy.data()[7] == 0);
    tihmstar::Mem moved(std::move(copy));
    CHECK(copy.size() == 0 && moved.size() == 8);
    moved.resize(2);
    CHECK(moved.size() == 2 && moved.data()[0] == 1);
    CHECK(tihmstar::parseNum("42") == 42);
    CHECK(tihmstar::parseNum("0x2A") == 42);
    unsigned char decoded[2] = {};
    CHECK(tihmstar::hexToBytes("01Af", decoded, 2) == 2);
    CHECK(decoded[0] == 1 && decoded[1] == 0xAF);
    char encoded[5] = {};
    size_t size = sizeof(encoded);
    tihmstar::bytesToHex(decoded, 2, encoded, &size);
    CHECK(size == 2 && std::strcmp(encoded, "01AF") == 0);
    tihmstar::Event event;
    CHECK(event.members() == 0 && event.getNextEvent() == 1);
    event.notifyAll();
    event.waitForEvent(1);
    CHECK(event.members() == 0 && event.getNextEvent() == 2);
    tihmstar::exception fixtureException("90", "81e4636784f1bc3fda6a90911fc15bf529975577", 12, "fixture", "value=%d", 7);
    CHECK(std::strcmp(fixtureException.what(), "value=7") == 0);
    CHECK(fixtureException.build_commit_count() == "90");
    CHECK(fixtureException.build_commit_sha() == "81e4636784f1bc3fda6a90911fc15bf529975577");
    tihmstar::exception errorCopy(fixtureException);
    CHECK(std::strcmp(errorCopy.what(), fixtureException.what()) == 0);
    CHECK(fixtureException.code() == ((12 << 16) | 7));
    tihmstar::writeFile("general-fixture.bin", bytes, sizeof(bytes));
    CHECK(tihmstar::fileExists("general-fixture.bin"));
    tihmstar::Mem file = tihmstar::readFile("general-fixture.bin");
    CHECK(file.size() == sizeof(bytes) && std::memcmp(file.data(), bytes, sizeof(bytes)) == 0);
    std::cout << "PASS downstream-general checks=" << checks << " skips=0\n";
}
CPP

%build
# Retain extras, cleanup, shared/static and assertions.
%configure CC=gcc CXX=g++ CFLAGS="%{optflags} -UNDEBUG" CXXFLAGS="%{optflags} -UNDEBUG"
%make_build

%install
%make_install
find %{buildroot}%{_libdir} -name '*.la' -delete
install -d %{buildroot}%{_datadir}/libgeneral/tests
install -m 0644 verify-general.cpp %{buildroot}%{_datadir}/libgeneral/tests/
sha256sum verify-general.cpp > %{buildroot}%{_datadir}/libgeneral/tests/SHA256SUMS

%check
# Original Automake check target; upstream registers no test cases.
make -j1 check VERBOSE=1
# Separately downstream, not an invented upstream test suite.
PKG_CONFIG_LIBDIR=%{buildroot}%{_libdir}/pkgconfig pkg-config --validate libgeneral
test "$(PKG_CONFIG_LIBDIR=%{buildroot}%{_libdir}/pkgconfig pkg-config --modversion libgeneral)" = 90
g++ %{optflags} -UNDEBUG -std=c++11 -I%{buildroot}%{_includedir} verify-general.cpp \
    -L%{buildroot}%{_libdir} -lgeneral -pthread -o staged-shared
LD_LIBRARY_PATH=%{buildroot}%{_libdir} ./staged-shared
g++ %{optflags} -UNDEBUG -std=c++11 -I%{buildroot}%{_includedir} verify-general.cpp \
    %{buildroot}%{_libdir}/libgeneral.a -pthread -o staged-static
./staged-static

%files
%license LICENSE
%{_libdir}/libgeneral.so.0*

%files devel
%{_includedir}/libgeneral/
%{_libdir}/libgeneral.so
%{_libdir}/libgeneral.a
%{_libdir}/pkgconfig/libgeneral.pc
%{_datadir}/libgeneral/

%changelog
* Thu Oct 15 2026 yinjiayi <yinjiayi@users.noreply.github.com> - 90-1
- Pin official stable archive; preserve full default shared/static build.
