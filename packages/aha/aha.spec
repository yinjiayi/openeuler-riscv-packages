# SPDX-License-Identifier: Apache-2.0
Name:           aha
Version:        0.5.1
Release:        1%{?dist}
Summary:        Convert ANSI terminal colors to HTML
License:        LGPL-2.0-or-later OR MPL-1.1
URL:            https://github.com/theZiz/aha
Source0:        aha-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make

%description
aha reads text containing ANSI terminal escape sequences and writes HTML that
preserves the terminal colors and text attributes.

%prep
%autosetup -p1

%build
%make_build \
  CC=%{__cc} \
  CFLAGS='%{optflags}' \
  LDFLAGS='%{build_ldflags}'

%install
%make_install PREFIX=%{_prefix} MANDIR=%{_mandir}

%check
./aha --version | grep -F '%{version}'
printf '\033[31mred\033[0m\n' | ./aha --no-header > converted.html
grep -F 'color:red' converted.html
grep -F '>red<' converted.html

%files
%license LICENSE.LGPLv2+ LICENSE.MPL1.1
%doc CHANGELOG README.md
%{_bindir}/aha
%{_mandir}/man1/aha.1*

%changelog
* Thu Aug 13 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.5.1-1
- Initial openEuler RISC-V package.
