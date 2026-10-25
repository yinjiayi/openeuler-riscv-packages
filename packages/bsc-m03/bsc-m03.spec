# SPDX-License-Identifier: Apache-2.0
Name:           bsc-m03
Version:        0.5.5
Release:        1%{?dist}
Summary:        High-performance block-sorting data compressor
License:        GPL-3.0-or-later
URL:            https://github.com/IlyaGrebnov/bsc-m03
Source0:        bsc-m03-0.5.5.tar.gz
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
%doc README.md
%doc AUTHORS

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.5.5-1
- Initial openEuler RISC-V package from the full package inventory.
