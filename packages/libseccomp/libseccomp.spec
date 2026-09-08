# SPDX-License-Identifier: Apache-2.0
Name:           libseccomp
Version:        2.6.1
Release:        1%{?dist}
Summary:        System call filtering library
License:        LGPL-2.1-only
URL:            https://github.com/seccomp/libseccomp
Source0:        libseccomp-2.6.1.tar.gz

BuildRequires:  gcc
BuildRequires:  gperf
BuildRequires:  make
BuildRequires:  python3-Cython
BuildRequires:  python3-devel
BuildRequires:  python3-unversioned-command

%description
libseccomp provides a platform-independent API for configuring Linux seccomp
system-call filters and includes a syscall name resolver.

%package devel
Summary:        Development files for libseccomp
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, pkg-config metadata, manual pages, and the unversioned library link
for developing applications with libseccomp.

%package -n python3-libseccomp
Summary:        Python 3 bindings for libseccomp
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description -n python3-libseccomp
Python 3 bindings for creating and inspecting Linux seccomp filters.

%prep
%autosetup -p1

%build
%configure --enable-python
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/libseccomp.a
rm -f %{buildroot}%{_libdir}/libseccomp.la
rm -f %{buildroot}%{python3_sitearch}/install_files.txt

%check
%make_build check

%files
%license LICENSE
%doc CHANGELOG CREDITS README.md SECURITY.md
%{_bindir}/scmp_sys_resolver
%{_libdir}/libseccomp.so.2*
%{_mandir}/man1/scmp_sys_resolver.1*

%files devel
%license LICENSE
%{_includedir}/seccomp.h
%{_includedir}/seccomp-syscalls.h
%{_libdir}/libseccomp.so
%{_libdir}/pkgconfig/libseccomp.pc
%{_mandir}/man3/seccomp_*.3*

%files -n python3-libseccomp
%license LICENSE
%{python3_sitearch}/seccomp*.so
%{python3_sitearch}/seccomp-*.egg-info/

%changelog
* Tue Aug 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.6.1-1
- Initial openEuler RISC-V package with complete upstream checks.
