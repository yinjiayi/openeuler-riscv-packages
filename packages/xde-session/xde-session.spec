# SPDX-License-Identifier: Apache-2.0
Name:           xde-session
Version:        1.14
Release:        8%{?dist}
Summary:        X Desktop Environment Display and Session Management
License:        GPL-3.0-or-later
URL:            https://github.com/bbidulock/xde-session
Source0:        xde-session-1.14.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libICE-devel
BuildRequires:  libSM-devel
BuildRequires:  libX11-devel
BuildRequires:  libXdmcp-devel
BuildRequires:  libXext-devel
BuildRequires:  libXft-devel
BuildRequires:  libXScrnSaver-devel
BuildRequires:  libtool
BuildRequires:  make

%description
X Desktop Environment Display and Session Management

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
* Thu Sep 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.14-8
- Add libXft-devel so pkg-config can resolve xft during configure.

* Thu Sep 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.14-7
- Add libSM-devel so pkg-config can resolve sm during configure.

* Thu Sep 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.14-6
- Add libICE-devel so pkg-config can resolve ice during configure.

* Thu Sep 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.14-5
- Add libXdmcp-devel so pkg-config can resolve xdmcp during configure.

* Thu Sep 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.14-4
- Add libXScrnSaver-devel so pkg-config can resolve xscrnsaver during configure.

* Thu Sep 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.14-3
- Add libXext-devel so pkg-config can resolve xext during configure.

* Thu Sep 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.14-2
- Add libX11-devel so pkg-config can resolve x11 during configure.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.14-1
- Initial openEuler RISC-V package from the full package inventory.
