# SPDX-License-Identifier: Apache-2.0
Name:           acl
Version:        2.4.0
Release:        1%{?dist}
Summary:        POSIX access control list utilities
License:        GPL-2.0-or-later AND LGPL-2.1-or-later
URL:            https://savannah.nongnu.org/projects/acl
Source0:        acl-%{version}.tar.xz
Patch0:         0001-tests-recognize-post-acl-device-cgroup-denial.patch

BuildRequires:  gawk
BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  libattr-devel
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  util-linux
Requires:       libacl%{?_isa} = %{version}-%{release}

%description
The acl package provides getfacl, setfacl, and chacl for inspecting and
changing POSIX access control lists on filesystem objects.

%package -n libacl
Summary:        Runtime library for POSIX access control lists
License:        LGPL-2.1-or-later

%description -n libacl
libacl implements the POSIX 1003.1e draft access control list interface.

%package -n libacl-devel
Summary:        Development files for libacl
License:        LGPL-2.1-or-later
Requires:       libacl%{?_isa} = %{version}-%{release}
Requires:       libattr-devel%{?_isa}

%description -n libacl-devel
Headers, pkg-config metadata, manual pages, and the unversioned library link
for developing applications with libacl.

%prep
%autosetup -p1

%build
%configure --disable-rpath --disable-static
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/libacl.a
rm -f %{buildroot}%{_libdir}/libacl.la
rm -rf %{buildroot}%{_docdir}/%{name}*
%find_lang %{name}

%check
export LD_LIBRARY_PATH="$PWD/.libs${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
# Pre-create libtool's fast-install executables with a world-executable mode.
# Otherwise a parallel root test with umask 027 can create lt-getfacl as 0750,
# preventing the test harness's unprivileged bin identity from executing it.
umask 022
./getfacl --version >/dev/null
./setfacl --version >/dev/null
# Runner workspaces can carry inherited named-user ACLs that override the
# ordinary other-mode bits for the bin identity.  Normalize only this writable
# package build tree and its test programs before exercising identity changes.
./setfacl --remove-all "%{_topdir}" "%{_builddir}" "$PWD" "$PWD/.libs" \
  "$PWD/getfacl" "$PWD/setfacl" \
  "$PWD/.libs/lt-getfacl" "$PWD/.libs/lt-setfacl"
./setfacl --remove-default "%{_topdir}" "%{_builddir}" "$PWD" "$PWD/.libs"
chmod a+rx "%{_topdir}" "%{_builddir}" "$PWD" "$PWD/.libs" \
  "$PWD/getfacl" "$PWD/setfacl" \
  "$PWD/.libs/lt-getfacl" "$PWD/.libs/lt-setfacl"
runuser -u bin -- "$PWD/getfacl" --version >/dev/null
runuser -u bin -- "$PWD/setfacl" --version >/dev/null
%make_build check

%files -f %{name}.lang
%license doc/COPYING doc/COPYING.LGPL
%doc README doc/CHANGES
%{_bindir}/chacl
%{_bindir}/getfacl
%{_bindir}/setfacl
%{_mandir}/man1/chacl.1*
%{_mandir}/man1/getfacl.1*
%{_mandir}/man1/setfacl.1*
%{_mandir}/man5/acl.5*

%files -n libacl
%license doc/COPYING.LGPL
%{_libdir}/libacl.so.1*

%files -n libacl-devel
%license doc/COPYING.LGPL
%{_includedir}/acl/
%{_includedir}/sys/acl.h
%{_libdir}/libacl.so
%{_libdir}/pkgconfig/libacl.pc
%{_mandir}/man3/acl_*.3*

%changelog
* Tue Aug 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.4.0-1
- Initial openEuler RISC-V package with the complete upstream test suite.
- Preserve root tests under parallel libtool execution, hardened device cgroups, and the protected runner's fixed workspace mount.
