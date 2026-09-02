# SPDX-License-Identifier: Apache-2.0
Name:           ski-ia64-simulator
Version:        1.5.1
Release:        4%{?dist}
Summary:        Itanium 2 (ia64) instruction set simulator
License:        GPL-2.0-or-later
URL:            https://github.com/trofi/ski
Source0:        ski-ia64-simulator-1.5.1.tar.gz
Patch0:         0001-linux-port-host-syscall-translation.patch
BuildRequires:  autoconf
BuildRequires:  autoconf-archive
BuildRequires:  automake
BuildRequires:  bison
BuildRequires:  elfutils-libelf-devel
BuildRequires:  flex
BuildRequires:  gcc
BuildRequires:  gperf
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  ncurses-devel
BuildRequires:  pkgconf-pkg-config

%description
Itanium 2 (ia64) instruction set simulator

%prep
%autosetup -n ski-1.5.1 -p1

%build
autoreconf -fi
%configure
%make_build

%install
%make_install
find %{buildroot} \( -type f -o -type l \) ! -path '%{buildroot}%{_mandir}/*' -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%make_build check

%files -f %{name}.files
%license COPYING
%doc README
%doc NEWS
%doc AUTHORS
%doc ChangeLog
%{_mandir}/man1/*

%changelog
* Mon Aug 31 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.5.1-4
- Keep brp-compressed manual pages out of the pre-compression generated file manifest.

* Mon Aug 31 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.5.1-3
- Isolate simulated syscall numbers from the RISC-V host ABI and add safe legacy syscall fallbacks.

* Sun Aug 30 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.5.1-2
- Match the official archive root and declare the required generated-code and library dependencies.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.5.1-1
- Initial openEuler RISC-V package from the full package inventory.
