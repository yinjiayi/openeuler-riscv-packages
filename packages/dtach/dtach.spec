# SPDX-License-Identifier: Apache-2.0
Name:           dtach
Version:        0.9
Release:        1%{?dist}
Summary:        Small terminal session detach and attach utility
License:        GPL-2.0-or-later
URL:            https://github.com/crigler/dtach
Source0:        dtach-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make

%description
dtach is a small utility that emulates the detach feature of screen without
adding a terminal emulation layer. It keeps a program running independently
of its controlling terminal and can later attach another terminal to it.

%prep
%autosetup -p1

%build
%configure
%make_build

%install
install -Dpm0755 dtach %{buildroot}%{_bindir}/dtach
install -Dpm0644 dtach.1 %{buildroot}%{_mandir}/man1/dtach.1

%check
./dtach --version | grep -F "dtach - version %{version}"
./dtach --help >/dev/null

%files
%license COPYING
%doc README
%{_bindir}/dtach
%{_mandir}/man1/dtach.1*

%changelog
* Fri Aug 14 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.9-1
- Initial openEuler RISC-V package from the independently verified upstream archive.
