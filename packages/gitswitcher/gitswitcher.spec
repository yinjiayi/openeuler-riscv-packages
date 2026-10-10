# SPDX-License-Identifier: Apache-2.0
Name:           gitswitcher
Version:        1.9.0
Release:        1%{?dist}
Summary:        Secure Git identity and SSH/GPG key management tool for seamless account switching
License:        GPL-3.0-or-later
URL:            https://github.com/tenseleyFlow/gitswitchC
Source0:        gitswitcher-1.9.0.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
Secure Git identity and SSH/GPG key management tool for seamless account switching

%prep
%autosetup -p1

%build
%make_build

%install
%make_install PREFIX=%{_prefix}
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%make_build test

%files -f %{name}.files
%license LICENSE
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.9.0-1
- Initial openEuler RISC-V package from the full package inventory.
