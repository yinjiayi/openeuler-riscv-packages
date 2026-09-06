# SPDX-License-Identifier: Apache-2.0
Name:           xmrig-proxy
Version:        6.24.0
Release:        1%{?dist}
Summary:        Stratum protocol proxy for Monero; HTTP API disabled, donation percentage is 0.
License:        GPL-3.0-or-later
URL:            https://github.com/xmrig/xmrig-proxy
Source0:        xmrig-proxy-6.24.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Stratum protocol proxy for Monero; HTTP API disabled, donation percentage is 0.

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 6.24.0-1
- Initial openEuler RISC-V package from the full package inventory.
