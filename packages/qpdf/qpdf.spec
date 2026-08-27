# SPDX-License-Identifier: Apache-2.0
Name:           qpdf
Version:        12.3.2
Release:        1%{?dist}
Summary:        QPDF: A Content-Preserving PDF Transformation System
License:        Apache-2.0
URL:            https://github.com/qpdf/qpdf
Source0:        qpdf-12.3.2.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  make
BuildRequires:  openssl-devel
BuildRequires:  zlib-devel

%description
QPDF: A Content-Preserving PDF Transformation System

%prep
%autosetup -p1

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
%license LICENSE.txt
%doc README.md
%doc ChangeLog

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 12.3.2-1
- Initial openEuler RISC-V package from the full package inventory.
