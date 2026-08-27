# SPDX-License-Identifier: Apache-2.0
Name:           openarc
Version:        1.3.0
Release:        1%{?dist}
Summary:        Open source implementation of the ARC email authentication system
License:        BSD-2-Clause
URL:            https://github.com/flowerysong/OpenARC
Source0:        openarc-1.3.0.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
Open source implementation of the ARC email authentication system

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
%license LICENSE
%license LICENSE.Sendmail
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.3.0-1
- Initial openEuler RISC-V package from the full package inventory.
