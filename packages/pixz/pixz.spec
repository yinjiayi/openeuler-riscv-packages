# SPDX-License-Identifier: Apache-2.0
Name:           pixz
Version:        1.0.7
Release:        1%{?dist}
Summary:        Parallel, indexed xz compressor
License:        BSD-2-Clause
URL:            https://github.com/vasi/pixz
Source0:        pixz-1.0.7.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
Parallel, indexed xz compressor

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
%doc NEWS

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.7-1
- Initial openEuler RISC-V package from the full package inventory.
