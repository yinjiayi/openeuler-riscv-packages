# SPDX-License-Identifier: Apache-2.0
Name:           libshine
Version:        3.1.1
Release:        1%{?dist}
Summary:        Fixed-point MP3 encoder library and command-line encoder
License:        LGPL-2.0-only
URL:            https://github.com/toots/shine
Source0:        shine-%{version}.tar.gz
Patch0:         0001-pkgconfig-libdir.patch

BuildRequires:  gcc
BuildRequires:  make

%description
Shine provides a fixed-point MP3 encoder library and the shineenc CLI.

%package devel
Summary:        Development files for libshine
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Public header, linker name, and pkg-config metadata for libshine.

%prep
%autosetup -n shine-%{version} -p1

%build
%configure --disable-static
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/libshine.la

%check
%make_build check
check_dir=$(mktemp -d)
trap 'rm -rf -- "$check_dir"' EXIT
./shineenc -q js/test/lib/encode.wav "$check_dir/encoded.mp3"
test -s "$check_dir/encoded.mp3"
magic=$(od -An -tx1 -N2 "$check_dir/encoded.mp3" | tr -d '[:space:]')
case "$magic" in
  ffe?|fff?) ;;
  *) echo "invalid MP3 frame sync: $magic" >&2; exit 1 ;;
esac

%files
%license COPYING
%doc ChangeLog README.md
%{_bindir}/shineenc
%{_libdir}/libshine.so.3*

%files devel
%license COPYING
%{_includedir}/shine/layer3.h
%{_libdir}/libshine.so
%{_libdir}/pkgconfig/shine.pc

%changelog
* Tue Sep 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.1.1-1
- Package official Shine 3.1.1 and native functional encode checks.
