# SPDX-License-Identifier: Apache-2.0
Name:           activate-linux
Version:        1.1.0
Release:        1%{?dist}
Summary:        The "Activate Windows" watermark ported to Linux with Xlib and cairo in C
License:        GPL-3.0-or-later
URL:            https://github.com/MrGlockenspiel/activate-linux
Source0:        activate-linux-1.1.0.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
The "Activate Windows" watermark ported to Linux with Xlib and cairo in C

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
%license LICENSE.md
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.1.0-1
- Initial openEuler RISC-V package from the full package inventory.
