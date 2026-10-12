# SPDX-License-Identifier: Apache-2.0
Name:           nsproxy
Version:        0.5.2
Release:        1%{?dist}
Summary:        A command-line tool that force applications to use a specific SOCKS5 or HTTP proxy.
License:        GPL-2.0-or-later
URL:            https://github.com/nlzy/nsproxy
Source0:        nsproxy-0.5.2.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
A command-line tool that force applications to use a specific SOCKS5 or HTTP proxy.

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

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.5.2-1
- Initial openEuler RISC-V package from the full package inventory.
