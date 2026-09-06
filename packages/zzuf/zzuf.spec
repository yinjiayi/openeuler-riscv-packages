# SPDX-License-Identifier: Apache-2.0
Name:           zzuf
Version:        0.15
Release:        1%{?dist}
Summary:        Transparent application input fuzzer
License:        WTFPL
URL:            https://github.com/samhocevar/zzuf
Source0:        zzuf-0.15.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
Transparent application input fuzzer

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
%license COPYING
%doc README.md
%doc AUTHORS

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.15-1
- Initial openEuler RISC-V package from the full package inventory.
