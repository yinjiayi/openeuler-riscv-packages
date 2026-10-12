# SPDX-License-Identifier: Apache-2.0
Name:           undbx
Version:        0.21
Release:        1%{?dist}
Summary:        Outlook Express .dbx files extractor
License:        GPL-3.0-or-later
URL:            https://github.com/ZungBang/undbx
Source0:        undbx-0.21.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
Outlook Express .dbx files extractor

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
%doc README.rst

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.21-1
- Initial openEuler RISC-V package from the full package inventory.
