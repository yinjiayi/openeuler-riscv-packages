# SPDX-License-Identifier: Apache-2.0
Name:           colorized-logs
Version:        2.7
Release:        1%{?dist}
Summary:        Tools for logs with ANSI color
License:        MIT
URL:            https://github.com/kilobyte/colorized-logs
Source0:        colorized-logs-2.7.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
Tools for logs with ANSI color

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
%doc README
%doc ChangeLog

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.7-1
- Initial openEuler RISC-V package from the full package inventory.
