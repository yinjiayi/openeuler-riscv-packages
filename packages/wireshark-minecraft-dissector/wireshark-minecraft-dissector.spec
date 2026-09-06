# SPDX-License-Identifier: Apache-2.0
Name:           wireshark-minecraft-dissector
Version:        1.4.4
Release:        1%{?dist}
Summary:        Wireshark dissector for Minecraft protocols.
License:        GPL-2.0-or-later
URL:            https://github.com/Nickid2018/MC_Dissector
Source0:        wireshark-minecraft-dissector-1.4.4.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
Wireshark dissector for Minecraft protocols.

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
%license LICENSE.GPL-3.0


%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.4.4-1
- Initial openEuler RISC-V package from the full package inventory.
