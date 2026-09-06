# SPDX-License-Identifier: Apache-2.0
Name:           npdfr
Version:        0.3.5
Release:        1%{?dist}
Summary:        A command-line PDF reader prioritizing fast searches
License:        GPL-3.0-or-later
URL:            https://github.com/amini-allight/npdfr
Source0:        npdfr-0.3.5.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
A command-line PDF reader prioritizing fast searches

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
%license license


%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.3.5-1
- Initial openEuler RISC-V package from the full package inventory.
