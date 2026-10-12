# SPDX-License-Identifier: Apache-2.0
Name:           mysql-xml-to-csv
Version:        1.0.3
Release:        1%{?dist}
Summary:        Convert MySQL XML output to CSV
License:        Apache-2.0
URL:            https://github.com/archiecobbs/mysql-xml-to-csv
Source0:        mysql-xml-to-csv-1.0.3.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
Convert MySQL XML output to CSV

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
%doc README.md
%doc AUTHORS

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.3-1
- Initial openEuler RISC-V package from the full package inventory.
