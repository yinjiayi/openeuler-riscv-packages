# SPDX-License-Identifier: Apache-2.0
Name:           xss-lock
Version:        0.4.0
Release:        1%{?dist}
Summary:        Use external locker as X screen saver
License:        MIT
URL:            https://github.com/wavexx/xss-lock
Source0:        xss-lock-0.4.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
Use external locker as X screen saver

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
%doc README.rst
%doc NEWS

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.4.0-1
- Initial openEuler RISC-V package from the full package inventory.
