# SPDX-License-Identifier: Apache-2.0
Name:           bitwise
Version:        0.60
Release:        1%{?dist}
Summary:        Interactive ncurses bitwise calculator
License:        GPL-3.0-or-later AND BSD-2-Clause
URL:            https://github.com/mellowcandle/bitwise
Source0:        bitwise-v0.60.tar.gz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  CUnit-devel
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  ncurses-devel
BuildRequires:  pkgconfig
BuildRequires:  readline-devel

%description
bitwise is an interactive terminal calculator for base conversion and bitwise
arithmetic.

%prep
%autosetup -n bitwise-v%{version} -p1

%build
autoreconf -fi
%configure
%make_build

%install
%make_install

%check
%make_build check
./bitwise --version | grep -F '%{version}'

%files
%license COPYING
%doc AUTHORS ChangeLog NEWS README
%{_bindir}/bitwise
%{_mandir}/man1/bitwise.1*

%changelog
* Mon Aug 24 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.60-1
- Update to 0.60 and use the upstream release asset.

* Sat Aug 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.50-1
- Initial openEuler RISC-V package.
