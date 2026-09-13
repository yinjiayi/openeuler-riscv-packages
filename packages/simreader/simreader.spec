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
%make_build CFLAGS="%{build_cflags} -Wall -Wextra -std=c99" LDFLAGS="%{build_ldflags} -lpcsclite"

%install
%make_install PREFIX=%{_prefix}
rm -rf %{buildroot}%{_docdir}/%{name}
find %{buildroot} \( -type f -o -type l \) ! -path '%{buildroot}%{_mandir}/*' ! -path '%{buildroot}%{_docdir}/%{name}/*' -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%make_build test

%files -f %{name}.files
%license LICENSE
%doc README.md
%{_mandir}/man1/simreader.1*

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.1-1
- Initial openEuler RISC-V package from the full package inventory.
- Add the PC/SC headers and library required by the build.
- Keep compressed manual pages out of the pre-compression file manifest.
- Preserve distribution debug and linker flags and avoid duplicate doc entries.
