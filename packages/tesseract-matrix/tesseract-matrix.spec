# SPDX-License-Identifier: Apache-2.0
Name:           tesseract-matrix
Version:        0.8.16
Release:        1%{?dist}
Summary:        Cross-platform Matrix chat client
License:        GPL-3.0-or-later
URL:            https://github.com/surakin/tesseract
Source0:        tesseract-matrix-0.8.16.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Cross-platform Matrix chat client

%prep
%autosetup -p1 -n tesseract-%{version}

%build
%cmake -S . -B %{_vpath_builddir} -DBUILD_TESTING=ON
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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.8.16-1
- Initial openEuler RISC-V package from the full package inventory.
