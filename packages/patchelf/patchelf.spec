# SPDX-License-Identifier: Apache-2.0
Name:           patchelf
Version:        0.19.1
Release:        1%{?dist}
Summary:        Utility for modifying ELF executables and libraries
License:        GPL-3.0-or-later
URL:            https://github.com/NixOS/patchelf
Source0:        patchelf-%{version}.tar.bz2

BuildRequires:  binutils
BuildRequires:  coreutils
BuildRequires:  diffutils
BuildRequires:  file
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libacl-devel
BuildRequires:  libattr-devel
BuildRequires:  make

%description
PatchELF is a utility for changing the interpreter, RPATH, needed libraries,
and other dynamic-linking metadata of ELF executables and shared libraries.

%prep
%autosetup -p1

%build
%configure --disable-silent-rules
%make_build

%install
%make_install
rm -f %{buildroot}%{_datadir}/doc/patchelf/README.md

%check
%make_build check

%files
%license COPYING
%doc README.md
%{_bindir}/patchelf
%{_mandir}/man1/patchelf.1*
%dir %{_datadir}/zsh
%dir %{_datadir}/zsh/site-functions
%{_datadir}/zsh/site-functions/_patchelf

%changelog
* Tue Aug 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.19.1-1
- Initial openEuler RISC-V package from frozen cross-distribution and upstream evidence.
