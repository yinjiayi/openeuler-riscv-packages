# SPDX-License-Identifier: Apache-2.0
Name:           bcal
Version:        2.5
Release:        1%{?dist}
Summary:        Storage conversion and expression calculator
License:        GPL-3.0-only
URL:            https://github.com/jarun/bcal
Source0:        bcal-v2.5.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  python3-pytest
BuildRequires:  readline-devel


%description
Storage conversion and expression calculator

%prep
%autosetup -p1 -n bcal-%{version}

%build
%make_build \
  CFLAGS="%{optflags}" \
  CFLAGS_OPTIMIZATION= \
  CFLAGS_WARNINGS= \
  LDFLAGS="%{build_ldflags}"

%install
%make_install \
  CFLAGS="%{optflags}" \
  CFLAGS_OPTIMIZATION= \
  CFLAGS_WARNINGS= \
  LDFLAGS="%{build_ldflags}" \
  PREFIX=%{_prefix}

%check
%{__python3} -m pytest -q test.py

%files
%license LICENSE
%doc README.md CHANGELOG
%{_bindir}/bcal
%{_mandir}/man1/bcal.1*

%changelog
* Sat Aug 22 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.5-1
- Package upstream bcal with the complete pytest suite.
