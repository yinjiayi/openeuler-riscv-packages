# SPDX-License-Identifier: Apache-2.0
Name:           simple-mtpfs
Version:        0.4.0
Release:        4%{?dist}
Summary:        A FUSE filesystem that supports reading/writing from MTP devices
License:        GPL-2.0-or-later
URL:            https://github.com/phatina/simple-mtpfs
Source0:        simple-mtpfs-0.4.0.tar.gz
BuildRequires:  autoconf
BuildRequires:  autoconf-archive
BuildRequires:  automake
BuildRequires:  fuse-devel
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libmtp-devel
BuildRequires:  libtool
BuildRequires:  libusbx-devel
BuildRequires:  make
BuildRequires:  pkgconf

%description
A FUSE filesystem that supports reading/writing from MTP devices

%prep
%autosetup -p1

%build
autoreconf -fi
%configure
%make_build

%install
%make_install
test -x %{buildroot}%{_bindir}/simple-mtpfs
test -f %{buildroot}%{_mandir}/man1/simple-mtpfs.1

%check
%make_build check
./src/simple-mtpfs --version > version.out
grep -F "simple-mtpfs version %{version}" version.out
./src/simple-mtpfs --help > help.out 2>&1
grep -F "usage: simple-mtpfs" help.out
grep -F "Report bugs to" help.out

%files
%{_bindir}/simple-mtpfs
%{_mandir}/man1/simple-mtpfs.1*
%license COPYING
%doc README.md
%doc NEWS
%doc AUTHORS
%doc ChangeLog

%changelog
* Thu Sep 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.4.0-4
- Use compression-safe explicit paths for the executable and manual page.
- Exercise upstream's version and help behavior because upstream registers no
  automated test targets, while retaining the no-op upstream check target.

* Thu Sep 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.4.0-3
- Raise the package timeout to 180 minutes after exact-head CI exhausted the
  former 60-minute budget while downloading the complete build dependencies.
- Preserve the full Autotools build, test suite, and FUSE functionality.

* Mon Aug 31 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.4.0-2
- Add the Autoconf macro, pkg-config, FUSE, MTP, and USB build dependencies.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.4.0-1
- Initial openEuler RISC-V package from the full package inventory.
