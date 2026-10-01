# SPDX-License-Identifier: Apache-2.0
Name:           s3fs-fuse
Version:        1.97
Release:        1%{?dist}
Summary:        FUSE-based file system backed by Amazon S3
License:        GPL-2.0-or-later
URL:            https://github.com/s3fs-fuse/s3fs-fuse
Source0:        s3fs-fuse-1.97.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libtool
BuildRequires:  make

%description
FUSE-based file system backed by Amazon S3

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
%doc ChangeLog

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.97-1
- Initial openEuler RISC-V package from the full package inventory.
