# SPDX-License-Identifier: Apache-2.0
Name:           gperf
Version:        3.3
Release:        1%{?dist}
Summary:        Perfect hash function generator
License:        GPL-3.0-or-later
URL:            https://www.gnu.org/software/gperf/
Source0:        gperf-%{version}.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  make

%description
GNU gperf generates perfect hash functions and associated lookup tables from
a set of keywords.

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install
rm -rf %{buildroot}%{_docdir}/gperf
rm -f %{buildroot}%{_infodir}/dir

%check
%make_build check

%files
%license COPYING
%doc AUTHORS ChangeLog NEWS README doc/gperf.html doc/gperf.pdf
%{_bindir}/gperf
%{_mandir}/man1/gperf.1*
%{_infodir}/gperf.info*

%changelog
* Tue Aug 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.3-1
- Initial openEuler RISC-V package from reviewed Fedora 44 and upstream evidence.
