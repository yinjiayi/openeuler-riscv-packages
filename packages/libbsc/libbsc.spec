# SPDX-License-Identifier: Apache-2.0
Name:           libbsc
Version:        3.3.12
Release:        1%{?dist}
Summary:        High-performance block-sorting data compressor
License:        Apache-2.0
URL:            https://github.com/IlyaGrebnov/libbsc
Source0:        libbsc-3.3.12.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
High-performance block-sorting data compressor

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
%doc AUTHORS

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.3.12-1
- Initial openEuler RISC-V package from the full package inventory.
