# SPDX-License-Identifier: Apache-2.0
Name:           stream-alert
Version:        1.0.2
Release:        1%{?dist}
Summary:        Get a Telegram notification when your webcam or screen changes
License:        MIT
URL:            https://github.com/akoidan/stream-alert
Source0:        stream-alert-1.0.2.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Get a Telegram notification when your webcam or screen changes

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.2-1
- Initial openEuler RISC-V package from the full package inventory.
