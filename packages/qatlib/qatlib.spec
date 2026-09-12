# SPDX-License-Identifier: Apache-2.0
Name:           qatlib
Version:        26.02.0
Release:        1%{?dist}
Summary:        User space library for Intel(R) QuickAssist Technology
License:        BSD-3-Clause
URL:            https://github.com/intel/qatlib
Source0:        qatlib-26.02.0.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
User space library for Intel(R) QuickAssist Technology

%prep
%autosetup -p1

%build
autoreconf -fi
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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 26.02.0-1
- Initial openEuler RISC-V package from the full package inventory.
