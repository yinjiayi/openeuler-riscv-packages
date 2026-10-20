# SPDX-License-Identifier: Apache-2.0
Name:           nmail
Version:        5.14.12
Release:        6%{?dist}
Summary:        Terminal-based email client
License:        MIT
URL:            https://github.com/d99kris/nmail
Source0:        nmail-5.14.12.tar.gz
BuildRequires:  cmake
BuildRequires:  cyrus-sasl-devel
BuildRequires:  expat-devel
BuildRequires:  file-devel
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libcurl-devel
BuildRequires:  make
BuildRequires:  ncurses-devel
BuildRequires:  openssl-devel
BuildRequires:  sqlite-devel
BuildRequires:  util-linux-devel
BuildRequires:  xapian-core-devel
BuildRequires:  zlib-devel

%description
Terminal-based email client

%prep
%autosetup -p1

%build
%cmake -S . -B %{_vpath_builddir} -DBUILD_TESTING=ON
%cmake_build

%install
%cmake_install

%check
%{_vpath_builddir}/nmail --version | grep -F -- 'nmail %{version}'
%{_vpath_builddir}/nmail --help >/dev/null

%files
%license LICENSE
%doc README.md
%{_bindir}/nmail
%{_mandir}/man1/nmail.1*

%changelog
* Wed Sep 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 5.14.12-6
- Own the installed binary and compression-tolerant manual path explicitly.
- Exercise the upstream release version and help probes during the build check.

* Wed Sep 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 5.14.12-5
- Configure CMake explicitly in the build directory consumed by the build and test macros.

* Wed Sep 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 5.14.12-4
- Declare the complete required nmail and bundled libetpan build dependency closure.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 5.14.12-3
- Add the OpenSSL development files required by CMake.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 5.14.12-2
- Add the ncurses development dependency required by CMake.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 5.14.12-1
- Initial openEuler RISC-V package from the full package inventory.
