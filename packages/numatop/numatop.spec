# SPDX-License-Identifier: Apache-2.0
Name:           numatop
Version:        2.5.1
Release:        1%{?dist}
Summary:        Observation tool for NUMA systems
License:        BSD-3-Clause
URL:            https://github.com/intel/numatop
Source0:        numatop-2.5.1.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
Observation tool for NUMA systems

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
%doc AUTHORS

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.5.1-1
- Initial openEuler RISC-V package from the full package inventory.
