# SPDX-License-Identifier: Apache-2.0
Name:           authselect
Version:        1.7.1
Release:        1%{?dist}
Summary:        Tool to select system authentication and identity sources from a list of supported profiles.
License:        GPL-3.0-or-later
URL:            https://github.com/authselect/authselect
Source0:        authselect-1.7.1.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
Tool to select system authentication and identity sources from a list of supported profiles.

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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.7.1-1
- Initial openEuler RISC-V package from the full package inventory.
