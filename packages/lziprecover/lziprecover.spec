# SPDX-License-Identifier: Apache-2.0
Name:           lziprecover
Version:        1.26
Release:        1%{?dist}
Summary:        Data recovery tool and decompressor for lzip files
License:        GPL-2.0-or-later
URL:            https://www.nongnu.org/lzip/lziprecover.html
Source0:        lziprecover-%{version}.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  lzip
BuildRequires:  make

%description
Lziprecover repairs and recovers damaged lzip archives, extracts intact data
from damaged members, creates and applies forward-error-correction records,
and provides lzip-compatible decompression and integrity testing.

%prep
%autosetup -p1

%build
./configure \
  --prefix=%{_prefix} \
  --exec-prefix=%{_exec_prefix} \
  --bindir=%{_bindir} \
  --datarootdir=%{_datadir} \
  --infodir=%{_infodir} \
  --mandir=%{_mandir} \
  CXX="%{__cxx}" \
  CXXFLAGS="%{build_cxxflags}" \
  LDFLAGS="%{build_ldflags} -Wl,--no-relax"
%make_build

%install
%make_install
rm -f %{buildroot}%{_infodir}/dir

%check
%make_build check

%files
%license COPYING
%doc AUTHORS ChangeLog NEWS README
%{_bindir}/lziprecover
%{_infodir}/lziprecover.info*
%{_mandir}/man1/lziprecover.1*

%changelog
* Thu Aug 13 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.26-1
- Initial openEuler RISC-V package with the complete upstream recovery suite.
