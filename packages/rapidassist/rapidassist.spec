# SPDX-License-Identifier: Apache-2.0
Name:           rapidassist
Version:        0.11.0
Release:        1%{?dist}
Summary:        RapidAssist is a lite cross-platform library that assist you with the most c++ repetitive tasks.
License:        MIT
URL:            https://github.com/end2endzone/RapidAssist
Source0:        rapidassist-0.11.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
RapidAssist is a lite cross-platform library that assist you with the most c++ repetitive tasks.

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
%license LICENSE.h
%doc README.md
%doc AUTHORS

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.11.0-1
- Initial openEuler RISC-V package from the full package inventory.
