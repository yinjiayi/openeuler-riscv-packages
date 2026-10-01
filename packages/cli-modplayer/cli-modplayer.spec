# SPDX-License-Identifier: Apache-2.0
Name:           cli-modplayer
Version:        1.3.0
Release:        1%{?dist}
Summary:        A terminal-based Module player (.mod, .xm, .it, .s3m) with real-time visualization
License:        MIT
URL:            https://github.com/Master290/cli-tracker
Source0:        cli-modplayer-1.3.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
A terminal-based Module player (.mod, .xm, .it, .s3m) with real-time visualization

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.3.0-1
- Initial openEuler RISC-V package from the full package inventory.
