# SPDX-License-Identifier: Apache-2.0
Name:           sysbench
Version:        1.0.20
Release:        2%{?dist}
Summary:        Scriptable multi-threaded benchmark tool for databases and systems
License:        GPL-2.0-or-later
URL:            https://github.com/akopytov/sysbench
Source0:        sysbench-1.0.20.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  ck-devel
BuildRequires:  gcc
BuildRequires:  libaio-devel
BuildRequires:  libtool
BuildRequires:  luajit-devel
BuildRequires:  make
BuildRequires:  mariadb-devel
BuildRequires:  openssl-devel
BuildRequires:  pkgconf-pkg-config
BuildRequires:  python3-unversioned-command

%description
Scriptable multi-threaded benchmark tool for databases and systems

%prep
%autosetup -p1

%build
autoreconf -fi
%configure \
    --with-mysql \
    --with-system-ck \
    --with-system-luajit \
    --without-gcc-arch
%make_build

%install
%make_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%make_build check

%files -f %{name}.files
%license COPYING
%doc README.md
%doc ChangeLog

%changelog
* Mon Aug 31 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.20-2
- Add the dependencies required by the default MySQL, AIO, and test paths.
- Use the target-native system LuaJIT and Concurrency Kit libraries.
- Preserve distribution RVA23 flags instead of guessing a host architecture.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.20-1
- Initial openEuler RISC-V package from the full package inventory.
