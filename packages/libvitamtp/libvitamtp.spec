# SPDX-License-Identifier: Apache-2.0
Name:           libvitamtp
Version:        2.5.9
Release:        1%{?dist}
Summary:        Library to interact with Vita's USB MTP protocol
License:        GPL-3.0-or-later
URL:            https://github.com/codestation/vitamtp
Source0:        libvitamtp-2.5.9.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
Library to interact with Vita's USB MTP protocol

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
%doc NEWS
%doc AUTHORS

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.5.9-1
- Initial openEuler RISC-V package from the full package inventory.
