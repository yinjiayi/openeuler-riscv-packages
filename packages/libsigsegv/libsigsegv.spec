# SPDX-License-Identifier: Apache-2.0
Name:           libsigsegv
Version:        2.15
Release:        1%{?dist}
Summary:        Library for handling page faults in user mode
License:        GPL-2.0-or-later
URL:            https://www.gnu.org/software/libsigsegv/
Source0:        libsigsegv-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make

%description
GNU libsigsegv provides portable handlers for page faults and stack overflow.

%package devel
Summary:        Development files for libsigsegv
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Header and unversioned linker name for libsigsegv.

%prep
%autosetup -p1

%build
%configure --disable-silent-rules --disable-static
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/*.la

%check
%make_build check

%files
%license COPYING
%doc AUTHORS ChangeLog NEWS README
%{_libdir}/libsigsegv.so.2*

%files devel
%license COPYING
%{_includedir}/sigsegv.h
%{_libdir}/libsigsegv.so

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.15-1
- Initial openEuler RISC-V package from frozen lineage and official source evidence.
