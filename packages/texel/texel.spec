# SPDX-License-Identifier: Apache-2.0
Name:           texel
Version:        1.12
Release:        2%{?dist}
Summary:        Free UCI compliant open source chess engine developed by Peter Österlund
License:        GPL-3.0-or-later
URL:            https://github.com/peterosterlund2/texel
Source0:        texel-1.12.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Free UCI compliant open source chess engine developed by Peter Österlund

%prep
%autosetup -p1

%build
%cmake -S . -B %{_vpath_builddir} -DBUILD_TESTING=ON
%cmake_build

%install
%cmake_install
install -Dpm0755 %{_vpath_builddir}/texel %{buildroot}%{_bindir}/texel
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
ctest --test-dir %{_vpath_builddir} --output-on-failure

%files -f %{name}.files
%license COPYING


%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.12-2
- Install the primary Texel engine executable when upstream provides no install target.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.12-1
- Initial openEuler RISC-V package from the full package inventory.
