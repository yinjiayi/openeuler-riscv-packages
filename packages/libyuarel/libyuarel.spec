# SPDX-License-Identifier: MIT
Name:           libyuarel
Version:        1.0
Release:        1%{?dist}
Summary:        In-place C URL parser
License:        MIT
URL:            https://github.com/jacketizer/libyuarel
Source0:        https://codeload.github.com/jacketizer/libyuarel/tar.gz/a1c9a19c03360909e7d3b9acbb7e0b986efbfb30#/libyuarel-1.0.tar.gz
Source1:        tests/run-tests.sh
Source2:        tests/consumer.c
Patch0:         patches/0001-support-staged-libdir-installation.patch
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  glibc-devel
BuildRequires:  bash
BuildRequires:  coreutils
BuildRequires:  binutils
BuildRequires:  grep
BuildRequires:  patch

%description
A small C library that parses URL components, path parts and query parameters
in place, using pointers into a mutable caller-owned buffer. It is not a URL
syntax validator and does not perform percent-decoding.

%package devel
Summary:        Headers and installed-interface checks for libyuarel
Requires:       %{name} = %{version}-%{release}
Requires:       gcc
Requires:       glibc-devel
Requires:       bash
Requires:       coreutils
Requires:       binutils
Requires:       grep

%description devel
The original public header and linker symlink, plus unchanged upstream tests
and example and a separate downstream installed-interface consumer.

%prep
%setup -q -n libyuarel-a1c9a19c03360909e7d3b9acbb7e0b986efbfb30
%patch0 -p1

%build
# Preserve upstream shared-library/SONAME flags, without upstream's -s stripping.
%make_build CC=gcc CFLAGS="%{optflags} -c -fPIC -Wall" LDFLAGS="%{build_ldflags} -shared -fvisibility=hidden -Wl,--exclude-libs=ALL,--no-as-needed,-soname,libyuarel.so.1"

%install
%make_install CC=gcc CFLAGS="%{optflags} -c -fPIC -Wall" LDFLAGS="%{build_ldflags} -shared -fvisibility=hidden -Wl,--exclude-libs=ALL,--no-as-needed,-soname,libyuarel.so.1" PREFIX=%{_prefix} LIBDIR=lib64
install -d %{buildroot}%{_datadir}/libyuarel/tests %{buildroot}%{_datadir}/libyuarel/examples
install -m 0644 tests/test_lib.c tests/minunit.h %{buildroot}%{_datadir}/libyuarel/tests/
install -m 0644 examples/simple.c %{buildroot}%{_datadir}/libyuarel/examples/
install -m 0644 %{SOURCE2} %{buildroot}%{_datadir}/libyuarel/consumer.c
install -m 0755 %{SOURCE1} %{buildroot}%{_datadir}/libyuarel/run-tests.sh
(
    cd %{buildroot}%{_datadir}/libyuarel
    sha256sum tests/test_lib.c tests/minunit.h examples/simple.c consumer.c run-tests.sh > SHA256SUMS
)

%check
# Exact original CI test target, retaining the default private build/lib prefix.
make check CC=gcc CFLAGS="%{optflags} -c -fPIC -Wall" LDFLAGS="%{build_ldflags} -shared -fvisibility=hidden -Wl,--exclude-libs=ALL,--no-as-needed,-soname,libyuarel.so.1"
bash %{buildroot}%{_datadir}/libyuarel/run-tests.sh %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license LICENSE
%doc README.md
%{_libdir}/libyuarel.so.1

%files devel
%{_includedir}/yuarel.h
%{_libdir}/libyuarel.so
%{_datadir}/libyuarel/

%changelog
* Sat Oct 17 2026 yinjiayi <yinjiayi@users.noreply.github.com> - 1.0-1
- Package fixed official 1.0 release; retain original check target and example.
