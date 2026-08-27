# SPDX-License-Identifier: Apache-2.0
Name:           darknet-hankai
Version:        6.0
Release:        1%{?dist}
Summary:        An open source neural network framework written in C, C++, and CUDA
License:        Apache-2.0
URL:            https://github.com/hank-ai/darknet
Source0:        darknet-hankai-6.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
An open source neural network framework written in C, C++, and CUDA

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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 6.0-1
- Initial openEuler RISC-V package from the full package inventory.
