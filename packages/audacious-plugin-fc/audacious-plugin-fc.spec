# SPDX-License-Identifier: Apache-2.0
Name:           audacious-plugin-fc
Version:        0.9.4
Release:        1%{?dist}
Summary:        TFMX & Future Composer input plugin for Audacious
License:        GPL-2.0-or-later
URL:            https://github.com/mschwendt/audacious-plugins-fc
Source0:        audacious-plugin-fc-0.9.4.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libtool
BuildRequires:  make

%description
TFMX & Future Composer input plugin for Audacious

%prep
%autosetup -p1

%build
autoreconf -fi
%configure
%make_build

%install
%make_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%make_build check

%files -f %{name}.files
%license COPYING
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.9.4-1
- Initial openEuler RISC-V package from the full package inventory.
