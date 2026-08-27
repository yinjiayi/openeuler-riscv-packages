# SPDX-License-Identifier: Apache-2.0
Name:           flow-pomodoro
Version:        1.2.0
Release:        1%{?dist}
Summary:        A pomodoro app that blocks distractions while you work.
License:        GPL-2.0-or-later
URL:            https://github.com/iamsergio/flow-pomodoro
Source0:        flow-pomodoro-1.2.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
A pomodoro app that blocks distractions while you work.

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
%license License.txt
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.2.0-1
- Initial openEuler RISC-V package from the full package inventory.
