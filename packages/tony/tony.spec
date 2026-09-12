# SPDX-License-Identifier: Apache-2.0
Name:           tony
Version:        2.1.1
Release:        1%{?dist}
Summary:        High quality pitch and note transcription for scientific applications
License:        GPL-2.0-or-later
URL:            https://github.com/sonic-visualiser/tony
Source0:        tony-2.1.1.tar.gz
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
High quality pitch and note transcription for scientific applications

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
%license COPYING
%doc README.md
%doc CHANGELOG

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.1.1-1
- Initial openEuler RISC-V package from the full package inventory.
