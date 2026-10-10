# SPDX-License-Identifier: Apache-2.0
Name:           stressapptest
Version:        1.0.11
Release:        1%{?dist}
Summary:        Memory and I/O stress testing utility
License:        Apache-2.0
URL:            https://github.com/stressapptest/stressapptest
Source0:        stressapptest-1.0.11.tar.gz

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libaio-devel
BuildRequires:  make

%description
stressapptest exercises memory, processors, and I/O devices under sustained
load. Meaningful validation requires native RISC-V hardware.

%prep
%autosetup -p1

%build
%configure --disable-default-optimizations
%make_build

%install
%make_install

%check
# This short run is intentionally reserved for the native-riscv64 route.
./src/stressapptest -M 16 -s 1

%files
%license COPYING NOTICE
%doc README.md
%{_bindir}/stressapptest
%{_mandir}/man1/stressapptest.1*

%changelog
* Tue Aug 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.11-1
- Initial openEuler RISC-V package; require native hardware validation.
