# SPDX-License-Identifier: Apache-2.0
Name:           sekirofpsunlock
Version:        0.2.3
Release:        2%{?dist}
Summary:        Patcher to set custom fps limit and resolution for Sekiro: Shadows Die Twice
License:        MIT
URL:            https://github.com/Lahvuun/sekirofpsunlock
Source0:        sekirofpsunlock-0.2.3.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
Patcher to set custom fps limit and resolution for Sekiro: Shadows Die Twice

%prep
%autosetup -p1

%build
%meson
%meson_build

%install
install -Dpm0755 %{_vpath_builddir}/sekirofpsunlock \
  %{buildroot}%{_bindir}/sekirofpsunlock
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%meson_test

%files -f %{name}.files
%license LICENSE
%doc README.md

%changelog
* Mon Aug 31 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.2.3-2
- Install the executable explicitly because upstream defines no Meson install rule.
- Preserve Meson test discovery without synthesizing unavailable integration tests.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.2.3-1
- Initial openEuler RISC-V package from the full package inventory.
