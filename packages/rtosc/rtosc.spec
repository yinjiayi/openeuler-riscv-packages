# SPDX-License-Identifier: Apache-2.0
Name:           rtosc
Version:        0.3.1
Release:        1%{?dist}
Summary:        Realtime safe OSC Messaging
License:        MIT
URL:            https://github.com/fundamental/rtosc
Source0:        rtosc-0.3.1.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Realtime safe OSC Messaging

%prep
%autosetup -p1

%build
%cmake -DBUILD_TESTING=ON
%cmake_build

%install
%cmake_install
find %{buildroot} \( -type f -o -type l \) -printf '/%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
ctest --test-dir %{_vpath_builddir} --output-on-failure

%files -f %{name}.files
%license LICENSE


%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.3.1-1
- Initial openEuler RISC-V package from the full package inventory.
