# SPDX-License-Identifier: Apache-2.0
Name:           movgrab
Version:        3.1.2
Release:        1%{?dist}
Summary:        command-line movie downloader
License:        GPL-3.0-or-later
URL:            https://github.com/ColumPaget/Movgrab
Source0:        movgrab-3.1.2.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
command-line movie downloader

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%make_build check

%files -f %{name}.files
%license LICENCE
%doc README

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.1.2-1
- Initial openEuler RISC-V package from the full package inventory.
