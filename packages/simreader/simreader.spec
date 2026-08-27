# SPDX-License-Identifier: Apache-2.0
Name:           simreader
Version:        1.0.1
Release:        1%{?dist}
Summary:        Unified SIM/USIM card reader tool with complete analysis capabilities
License:        MIT
URL:            https://github.com/TheOnlyMango/simreader
Source0:        simreader-1.0.1.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pcsc-lite-devel

%description
Unified SIM/USIM card reader tool with complete analysis capabilities

%prep
%autosetup -p1

%build
%make_build

%install
%make_install PREFIX=%{_prefix}
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%make_build test

%files -f %{name}.files
%license LICENSE
%doc README.md

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.1-1
- Initial openEuler RISC-V package from the full package inventory.
- Add the PC/SC headers and library required by the build.
