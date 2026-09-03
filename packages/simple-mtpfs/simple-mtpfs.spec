# SPDX-License-Identifier: Apache-2.0
Name:           simple-mtpfs
Version:        0.4.0
Release:        3%{?dist}
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
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%make_build check

%files -f %{name}.files
%license COPYING
%doc README.md
%doc NEWS
%doc AUTHORS
%doc ChangeLog

%changelog
* Thu Sep 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.4.0-3
- Raise the package timeout to 180 minutes after exact-head CI exhausted the
  former 60-minute budget while downloading the complete build dependencies.
- Preserve the full Autotools build, test suite, and FUSE functionality.

* Mon Aug 31 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.4.0-2
- Add the Autoconf macro, pkg-config, FUSE, MTP, and USB build dependencies.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.4.0-1
- Initial openEuler RISC-V package from the full package inventory.
