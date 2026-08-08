# SPDX-License-Identifier: Apache-2.0
%global debug_package %{nil}

Name:           sparsehash
Version:        2.0.4
Release:        1%{?dist}
Summary:        Memory-efficient C++ hash table headers
License:        BSD-3-Clause
URL:            https://github.com/sparsehash/sparsehash
Source0:        sparsehash-%{version}.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  make

%description
sparsehash provides memory-efficient sparse and dense C++ hash maps and sets.
The installed internal configuration header is generated for the target
toolchain, so this package is architecture-specific despite being header-only.

%prep
%autosetup -p1 -n sparsehash-sparsehash-%{version}

%build
%configure --disable-dependency-tracking
%make_build

%install
%make_install
rm -rf %{buildroot}%{_docdir}/%{name}-%{version}

%check
%make_build check

%files
%license COPYING
%doc AUTHORS ChangeLog NEWS README TODO doc/*.html doc/designstyle.css
%{_includedir}/google/
%{_includedir}/sparsehash/
%{_libdir}/pkgconfig/libsparsehash.pc

%changelog
* Sat Aug 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.0.4-1
- Initial openEuler RISC-V package.
