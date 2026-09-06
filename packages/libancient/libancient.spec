# SPDX-License-Identifier: Apache-2.0
Name:           libancient
Version:        2.3.0
Release:        1%{?dist}
Summary:        Decompression routines for ancient formats
License:        BSD-2-Clause
URL:            https://github.com/temisu/ancient
Source0:        libancient-2.3.0.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libtool
BuildRequires:  make

%description
Decompression routines for ancient formats

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
%license LICENSE.bzip2
%doc README.md

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.3.0-1
- Initial openEuler RISC-V package from the full package inventory.
