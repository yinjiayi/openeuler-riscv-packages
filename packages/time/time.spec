# SPDX-License-Identifier: Apache-2.0
Name:           time
Version:        1.10
Release:        1%{?dist}
Summary:        GNU resource usage measurement utility
License:        GPL-3.0-or-later AND GFDL-1.3-no-invariants-or-later
URL:            https://www.gnu.org/software/time/
Source0:        time-%{version}.tar.xz

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  texinfo

%description
GNU time runs another program and reports elapsed time, CPU time, memory,
page-fault, context-switch, and other resource usage statistics.

%prep
%autosetup -p1

%build
%configure --disable-silent-rules
%make_build

%install
%make_install
rm -f %{buildroot}%{_infodir}/dir

%check
%make_build check

%files
%license COPYING
%doc AUTHORS ChangeLog NEWS README
%{_bindir}/time
%{_infodir}/time.info*

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.10-1
- Initial openEuler RISC-V package from frozen cross-distribution and upstream evidence.
