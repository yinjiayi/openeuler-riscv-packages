# SPDX-License-Identifier: Apache-2.0
Name:           rtl-sdr-blog
Version:        1.3.6
Release:        1%{?dist}
Summary:        Modified Osmocom drivers with enhancements for RTL-SDR Blog V3 and V4 units.
License:        GPL-2.0-or-later
URL:            https://github.com/rtlsdrblog/rtl-sdr-blog
Source0:        rtl-sdr-blog-1.3.6.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
Modified Osmocom drivers with enhancements for RTL-SDR Blog V3 and V4 units.

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
%license COPYING
%doc README
%doc AUTHORS

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.3.6-1
- Initial openEuler RISC-V package from the full package inventory.
