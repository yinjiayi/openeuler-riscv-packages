# SPDX-License-Identifier: Apache-2.0
Name:           abracadabra
Version:        4.1.1
Release:        1%{?dist}
Summary:        Abraca DAB radio: DAB/DAB+ Software Defined Radio (SDR)
License:        MIT
URL:            https://github.com/KejPi/AbracaDABra
Source0:        abracadabra-4.1.1.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Abraca DAB radio: DAB/DAB+ Software Defined Radio (SDR)

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
%license LICENSE
%doc README.md

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.1.1-1
- Initial openEuler RISC-V package from the full package inventory.
