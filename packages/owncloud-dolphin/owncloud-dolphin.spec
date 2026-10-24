# SPDX-License-Identifier: Apache-2.0
Name:           owncloud-dolphin
Version:        6.0.0
Release:        1%{?dist}
Summary:        Dolphin Integrations for the ownCloud desktop syncing client
License:        GPL-2.0-or-later
URL:            https://github.com/owncloud/client-desktop-shell-integration-dolphin
Source0:        owncloud-dolphin-6.0.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Dolphin Integrations for the ownCloud desktop syncing client

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
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 6.0.0-1
- Initial openEuler RISC-V package from the full package inventory.
