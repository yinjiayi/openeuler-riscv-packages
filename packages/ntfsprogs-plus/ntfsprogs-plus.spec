# SPDX-License-Identifier: Apache-2.0
Name:           ntfsprogs-plus
Version:        1.0.0
Release:        1%{?dist}
Summary:        NTFS filesystem utilities.
License:        GPL-2.0-or-later
URL:            https://github.com/ntfsprogs-plus/ntfsprogs-plus
Source0:        ntfsprogs-plus-1.0.0.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
NTFS filesystem utilities.

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
%license COPYING.LIB
%doc README.md
%doc NEWS
%doc AUTHORS
%doc ChangeLog

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.0-1
- Initial openEuler RISC-V package from the full package inventory.
