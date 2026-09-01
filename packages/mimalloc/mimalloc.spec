# SPDX-License-Identifier: Apache-2.0
Name:           mimalloc
Version:        3.5.1
Release:        1%{?dist}
Summary:        Compact general-purpose memory allocator
License:        MIT
URL:            https://github.com/microsoft/mimalloc
Source0:        v3.5.1.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
mimalloc is a compact general-purpose allocator designed for consistent
performance, low fragmentation, and efficient concurrent allocation.

%package devel
Summary:        Development files for mimalloc
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, CMake package metadata, pkg-config metadata, and the unversioned
shared-library link for developing software with mimalloc.

%package static
Summary:        Static library for mimalloc
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}

%description static
The static library for applications that explicitly require static linking
with mimalloc.

%prep
%autosetup -p1

%build
%cmake \
  -DMI_BUILD_SHARED=ON \
  -DMI_BUILD_STATIC=ON \
  -DMI_BUILD_OBJECT=OFF \
  -DMI_BUILD_TESTS=ON \
  -DMI_INSTALL_TOPLEVEL=ON \
  -DMI_OPT_ARCH=OFF
%make_build

%install
DESTDIR=%{buildroot} %{__cmake} --install .

%check
%{__ctest} --output-on-failure

%files
%license LICENSE
%doc readme.md SECURITY.md
%{_libdir}/libmimalloc.so.3*

%files devel
%license LICENSE
%{_includedir}/mimalloc*.h
%{_libdir}/libmimalloc.so
%{_libdir}/pkgconfig/mimalloc.pc
%{_libdir}/cmake/mimalloc/

%files static
%license LICENSE
%{_libdir}/libmimalloc.a

%changelog
* Thu Aug 13 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.4.5-1
- Initial openEuler RISC-V package.
