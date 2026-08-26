# SPDX-License-Identifier: Apache-2.0
Name:           selint
Version:        1.5.1
Release:        1%{?dist}
Summary:        Static code analysis tool for SELinux policy source files
License:        Apache-2.0
URL:            https://github.com/SELinuxProject/selint
Source0:        selint-1.5.1.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
Static code analysis tool for SELinux policy source files

%prep
%autosetup -p1

%build
autoreconf -fi
%configure
%make_build

%install
%make_install
find %{buildroot} \( -type f -o -type l \) -printf '/%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%make_build check

%files -f %{name}.files
%license LICENSE
%doc README.md
%doc CHANGELOG

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.5.1-1
- Initial openEuler RISC-V package from the full package inventory.
