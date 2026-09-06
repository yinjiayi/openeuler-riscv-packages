# SPDX-License-Identifier: Apache-2.0
Name:           ksmbd-tools
Version:        3.5.6
Release:        1%{?dist}
Summary:        Userspace tools for the ksmbd kernel SMB server
License:        GPL-2.0-or-later
URL:            https://github.com/cifsd-team/ksmbd-tools
Source0:        ksmbd-tools-3.5.6.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
Userspace tools for the ksmbd kernel SMB server

%prep
%autosetup -p1

%build
%meson
%meson_build

%install
%meson_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%meson_test

%files -f %{name}.files
%license COPYING
%doc README.md
%doc AUTHORS

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.5.6-1
- Initial openEuler RISC-V package from the full package inventory.
