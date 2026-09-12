# SPDX-License-Identifier: Apache-2.0
Name:           clzip
Version:        1.16
Release:        1%{?dist}
Summary:        C implementation of the lzip lossless data compressor
License:        GPL-2.0-or-later
URL:            https://www.nongnu.org/lzip/clzip.html
Source0:        clzip-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make

%description
Clzip is a C implementation of the lzip lossless data compressor. It provides
a gzip-like command-line interface and interoperates with other lzip format
implementations while requiring no C++ compiler.

%prep
%autosetup -p1

%build
%set_build_flags
./configure \
  --prefix=%{_prefix} \
  --exec-prefix=%{_exec_prefix} \
  --bindir=%{_bindir} \
  --datarootdir=%{_datadir} \
  --infodir=%{_infodir} \
  --mandir=%{_mandir} \
  CC="%{__cc}" \
  CPPFLAGS="${CPPFLAGS}" \
  CFLAGS="${CFLAGS}" \
  LDFLAGS="${LDFLAGS}"
%make_build

%install
%make_install
rm -f %{buildroot}%{_infodir}/dir

%check
# Run the complete maintained compression, decompression, listing, stream,
# malformed-input, truncation, and corruption test script.
%make_build check

%files
%license COPYING
%doc AUTHORS ChangeLog NEWS README
%{_bindir}/clzip
%{_infodir}/clzip.info*
%{_mandir}/man1/clzip.1*

%changelog
* Fri Aug 14 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.16-1
- Initial openEuler RISC-V package from reviewed upstream evidence.
