# SPDX-License-Identifier: Apache-2.0
Name:           luau
Version:        0.733
Release:        4%{?dist}
Summary:        A fast, small, safe, gradually typed embeddable scripting language derived from Lua
License:        MIT
URL:            https://github.com/luau-lang/luau
Source0:        luau-0.733.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
A fast, small, safe, gradually typed embeddable scripting language derived from Lua

%prep
%autosetup -p1

%build
%cmake_conf \
  -DLUAU_BUILD_CLI=ON \
  -DLUAU_BUILD_TESTS=ON \
  -DLUAU_BUILD_WEB=OFF
%cmake_build

%install
for executable in \
  luau \
  luau-analyze \
  luau-ast \
  luau-bytecode \
  luau-compile \
  luau-reduce
do
  install -Dpm0755 "%{_vpath_builddir}/${executable}" \
    "%{buildroot}%{_bindir}/${executable}"
done
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%{_vpath_builddir}/Luau.UnitTest
%{_vpath_builddir}/Luau.Conformance
%{_vpath_builddir}/Luau.CLI.Test

%files -f %{name}.files
%license LICENSE.txt
%doc README.md

%changelog
* Sat Sep 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.733-4
- Extend the QEMU budget after compilation reached 76% at the prior deadline.

* Wed Sep 09 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.733-3
- Allow the complete CLI, library, and test build to finish under QEMU.

* Tue Sep 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.733-2
- Configure in the RPM out-of-source build directory, install the CLI tools,
  and execute the upstream test binaries directly.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.733-1
- Initial openEuler RISC-V package from the full package inventory.
