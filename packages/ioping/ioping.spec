# SPDX-License-Identifier: Apache-2.0

Name:           ioping
Version:        1.3
Release:        1%{?dist}
Summary:        Disk I/O latency measurement utility
License:        GPL-3.0-only
URL:            https://github.com/koct9i/ioping
Source0:        ioping-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make

%description
ioping measures storage latency and throughput using request patterns similar
to the network ping utility.

%prep
%autosetup -p1

%build
%make_build CFLAGS="%{optflags}" LDFLAGS="%{build_ldflags}"

%install
%make_install PREFIX=%{_prefix} \
  CFLAGS="%{optflags}" LDFLAGS="%{build_ldflags}"

%check
%make_build test CFLAGS="%{optflags}" LDFLAGS="%{build_ldflags}"

%files
%license LICENSE
%doc README.md changelog
%{_bindir}/ioping
%{_mandir}/man1/ioping.1*

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.3-1
- Initial openEuler RISC-V package with the complete maintained upstream I/O test target.
