# SPDX-License-Identifier: Apache-2.0
Name:           lzip
Version:        1.26
Release:        1%{?dist}
Summary:        Lossless data compressor based on the LZMA algorithm
License:        GPL-2.0-or-later
URL:            https://www.nongnu.org/lzip/lzip.html
Source0:        lzip-%{version}.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  make

%description
Lzip is a lossless data compressor with a user interface similar to gzip or
bzip2. It uses a simplified LZMA stream format with integrity checking.

%prep
%autosetup -p1

%build
./configure \
  --prefix=%{_prefix} \
  --exec-prefix=%{_exec_prefix} \
  --bindir=%{_bindir} \
  --datarootdir=%{_datadir} \
  --infodir=%{_infodir} \
  --mandir=%{_mandir} \
  CXX="%{__cxx}" \
  CXXFLAGS="%{build_cxxflags}" \
  LDFLAGS="%{build_ldflags}"
%make_build

%install
%make_install

%check
# Run the complete maintained compression, decompression, listing, and
# malformed-input test script shipped in the publisher archive.
%make_build check

%files
%license COPYING
%doc AUTHORS ChangeLog NEWS README
%{_bindir}/lzip
%{_infodir}/lzip.info*
%{_mandir}/man1/lzip.1*

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.26-1
- Update the openEuler RISC-V package to upstream 1.26 with full tests.
