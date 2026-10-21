# SPDX-License-Identifier: Apache-2.0
Name:           pigz
Version:        2.8
Release:        1%{?dist}
Summary:        Parallel implementation of gzip
License:        Zlib
URL:            https://zlib.net/pigz/
Source0:        pigz-%{version}.tar.gz

BuildRequires:  coreutils
BuildRequires:  gcc
BuildRequires:  gzip
BuildRequires:  make
BuildRequires:  which
BuildRequires:  zlib-devel

%description
pigz is a parallel implementation of gzip that uses multiple processor cores
for compression while retaining gzip-compatible output.

%prep
%autosetup -p1

%build
%make_build \
  CC=%{__cc} \
  CFLAGS='%{build_cflags}' \
  LDFLAGS='%{build_ldflags}'

%install
install -Dpm 0755 pigz %{buildroot}%{_bindir}/pigz
ln -s pigz %{buildroot}%{_bindir}/unpigz
install -Dpm 0644 pigz.1 %{buildroot}%{_mandir}/man1/pigz.1
ln -s pigz.1 %{buildroot}%{_mandir}/man1/unpigz.1

%check
%make_build test

%files
%license README
%{_bindir}/pigz
%{_bindir}/unpigz
%{_mandir}/man1/pigz.1*
%{_mandir}/man1/unpigz.1*

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.8-1
- Initial openEuler RISC-V package from frozen cross-distribution and official upstream evidence.
