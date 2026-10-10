# SPDX-License-Identifier: Apache-2.0
Name:           deepin-polkit-agent-ext-gnomekeyring
Version:        6.0.1
Release:        1%{?dist}
Summary:        GNOME keyring extension for dde-polkit-agent
License:        GPL-3.0-or-later
URL:            https://github.com/linuxdeepin/dpa-ext-gnomekeyring
Source0:        deepin-polkit-agent-ext-gnomekeyring-6.0.1.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
GNOME keyring extension for dde-polkit-agent

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 6.0.1-1
- Initial openEuler RISC-V package from the full package inventory.
