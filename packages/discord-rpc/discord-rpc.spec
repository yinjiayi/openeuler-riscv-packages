# SPDX-License-Identifier: Apache-2.0
Name:           discord-rpc
Version:        3.4.0
Release:        1%{?dist}
Summary:        Library for integrating Discord features This is a library for interfacing your game with a locally running Discord desktop client. It allows applications t
License:        MIT
URL:            https://github.com/discord/discord-rpc
Source0:        discord-rpc-3.4.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Library for integrating Discord features This is a library for interfacing your game with a locally running Discord desktop client. It allows applications t

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.4.0-1
- Initial openEuler RISC-V package from the full package inventory.
