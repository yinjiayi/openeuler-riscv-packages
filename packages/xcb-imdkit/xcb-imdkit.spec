# SPDX-License-Identifier: Apache-2.0
Name:           xcb-imdkit
Version:        1.0.9
Release:        1%{?dist}
Summary:        XIM protocol implementation for XCB
License:        LGPL-2.1-only AND MIT
URL:            https://github.com/fcitx/xcb-imdkit
Source0:        xcb-imdkit-1.0.9.tar.gz

BuildRequires:  cmake
BuildRequires:  extra-cmake-modules
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconf
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xcb-keysyms)
BuildRequires:  pkgconfig(xcb-util)
BuildRequires:  uthash-devel

%description
xcb-imdkit implements the X Input Method protocol using XCB. It provides
asynchronous client and server APIs with safer handling of malformed protocol
messages than the historical Xlib IMdkit implementation.

%package devel
Summary:        Development files for xcb-imdkit
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       libxcb-devel%{?_isa}
Requires:       xcb-util-devel%{?_isa}

%description devel
Headers, pkg-config and CMake metadata, and the unversioned shared-library link
for developing XIM clients and servers with xcb-imdkit.

%prep
%autosetup -p1

%build
%cmake_conf \
  -DUSE_SYSTEM_UTHASH=ON
%cmake_build

%install
%cmake_install

%check
# Upstream registers its display-independent UTF-8/compound-text round-trip
# test with CTest. The interactive client/server demos need an X server and are
# compiled but intentionally are not registered as automated tests upstream.
%ctest --output-on-failure --parallel 1

%files
%license LICENSES/LGPL-2.1-only.txt
%doc README.md
%{_libdir}/libxcb-imdkit.so.1*

%files devel
%license LICENSES/LGPL-2.1-only.txt
%{_includedir}/xcb-imdkit/
%{_libdir}/cmake/XCBImdkit/
%{_libdir}/libxcb-imdkit.so
%{_libdir}/pkgconfig/xcb-imdkit.pc

%changelog
* Sun Sep 06 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.9-1
- Initial openEuler RISC-V package with system dependencies and upstream test.
