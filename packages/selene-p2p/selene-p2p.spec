# SPDX-License-Identifier: Apache-2.0
Name:           selene-p2p
Version:        1.0.7
Release:        1%{?dist}
Summary:        Selene is a Tor-based P2P chat and encrypted file sharing
License:        GPL-3.0-or-later
URL:            https://github.com/alamahant/Selene
Source0:        selene-p2p-1.0.7.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  openssl-devel
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qtmultimedia-devel

%description
Selene is a Tor-based P2P chat and encrypted file sharing

%prep
%autosetup -n Selene-%{version} -p1

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
%license LICENSE
%doc README.md

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.7-1
- Initial openEuler RISC-V package from the full package inventory.
- Use the upstream archive's actual top-level directory.
- Add the Qt 6 multimedia and OpenSSL development files required by CMake.
