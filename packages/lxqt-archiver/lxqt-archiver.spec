# SPDX-License-Identifier: Apache-2.0
Name:           lxqt-archiver
Version:        1.4.0
Release:        1%{?dist}
Summary:        A simple & lightweight desktop-agnostic Qt file archiver
License:        GPL-2.0-or-later
URL:            https://github.com/lxqt/lxqt-archiver
Source0:        lxqt-archiver-1.4.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
A simple & lightweight desktop-agnostic Qt file archiver

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
%doc AUTHORS
%doc CHANGELOG

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.4.0-1
- Initial openEuler RISC-V package from the full package inventory.
