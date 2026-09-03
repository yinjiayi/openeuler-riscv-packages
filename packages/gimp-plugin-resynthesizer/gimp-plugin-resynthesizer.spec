# SPDX-License-Identifier: Apache-2.0
Name:           gimp-plugin-resynthesizer
Version:        3.0.1
Release:        4%{?dist}
Summary:        Suite of gimp plugins for texture synthesis
License:        GPL-3.0-or-later
URL:            https://github.com/bootchk/resynthesizer
Source0:        gimp-plugin-resynthesizer-3.0.1.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  pkgconfig(gimp-3.0)
BuildRequires:  pkgconfig(glib-2.0)

%description
Suite of gimp plugins for texture synthesis

%prep
%autosetup -n resynthesizer-%{version} -p1

%build
%meson -Dbuild-libheal=true
%meson_build

%install
%meson_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
test -x %{_vpath_builddir}/test/testHealLib
%{_vpath_builddir}/test/testHealLib | tee testHealLib.log
test "$(grep -c '^Expect:$' testHealLib.log)" -eq 8
test "$(grep -c '^Result:$' testHealLib.log)" -eq 8

%files -f %{name}.files
%license COPYING
%doc README.md
%doc NEWS
%doc AUTHORS
%doc ChangeLog

%changelog
* Thu Sep 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.0.1-4
- Select the actual resynthesizer-3.0.1 directory emitted by the upstream tag
  archive instead of deriving the directory from the downstream package name.
- Build and execute the upstream testHealLib functional harness and assert that
  all eight exercised scenarios ran, avoiding an empty Meson test invocation.

* Thu Sep 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.0.1-3
- Raise the package timeout to 180 minutes after the complete 328-package GIMP
  dependency transaction exhausted the former 60-minute budget during downloads.
- Preserve the full upstream Meson test suite and plugin functionality.

* Mon Aug 31 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.0.1-2
- Require the exact GIMP 3 and GLib pkg-config interfaces used by Meson.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.0.1-1
- Initial openEuler RISC-V package from the full package inventory.
