# SPDX-License-Identifier: Apache-2.0
Name:           dsp
Version:        2.0
Release:        1%{?dist}
Summary:        An audio processing program with an interactive mode
License:        ISC
URL:            https://github.com/bmc0/dsp
Source0:        dsp-2.0.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
An audio processing program with an interactive mode

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
%license LICENSE
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.0-1
- Initial openEuler RISC-V package from the full package inventory.
