# SPDX-License-Identifier: Apache-2.0
Name:           pcalc-lts
Version:        0.8.1
Release:        1%{?dist}
Summary:        A command-line programmer's calculator handling HEX/DEC/OCT/BIN
License:        GPL-2.0-or-later
URL:            https://github.com/jurassiclizard/pcalc-lts
Source0:        pcalc-lts-0.8.1.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
A command-line programmer's calculator handling HEX/DEC/OCT/BIN

%prep
%autosetup -p1

%build
%cmake -DBUILD_TESTING=ON
%cmake_build

%install
%cmake_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
ctest --test-dir %{_vpath_builddir} --output-on-failure

%files -f %{name}.files
%license COPYING
%doc README.md
%doc AUTHORS

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.8.1-1
- Initial openEuler RISC-V package from the full package inventory.
