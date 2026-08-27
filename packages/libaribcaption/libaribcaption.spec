# SPDX-License-Identifier: Apache-2.0
Name:           libaribcaption
Version:        1.1.2
Release:        1%{?dist}
Summary:        Caption decoder/renderer library for handling ARIB STD-B24 based TV broadcast captions
License:        MIT
URL:            https://github.com/xqq/libaribcaption
Source0:        libaribcaption-1.1.2.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Caption decoder/renderer library for handling ARIB STD-B24 based TV broadcast captions

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.1.2-1
- Initial openEuler RISC-V package from the full package inventory.
