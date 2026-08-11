# SPDX-License-Identifier: Apache-2.0
Name:           bzip2
Version:        1.0.8
Release:        1%{?dist}
Summary:        High-quality data compression utilities
License:        bzip2-1.0.6
URL:            https://sourceware.org/bzip2
Source0:        bzip2-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make

%description
bzip2 is a lossless, block-sorting data compressor. This package provides
the command-line compression and recovery tools.

%package libs
Summary:        Runtime library for bzip2

%description libs
The shared libbz2 runtime library used by applications that read and write
bzip2-compressed data.

%package devel
Summary:        Development files for bzip2
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description devel
The header and unversioned shared-library link required to develop software
using libbz2.

%prep
%autosetup -p1

%build
%make_build -f Makefile-libbz2_so \
  CC=%{__cc} \
  CFLAGS="%{optflags} -fPIC -D_FILE_OFFSET_BITS=64" \
  LDFLAGS="%{build_ldflags}"
%make_build \
  CC=%{__cc} \
  CFLAGS="%{optflags} -fPIC -D_FILE_OFFSET_BITS=64" \
  LDFLAGS="%{build_ldflags}"

%install
install -d \
  %{buildroot}%{_bindir} \
  %{buildroot}%{_includedir} \
  %{buildroot}%{_libdir} \
  %{buildroot}%{_mandir}/man1

install -pm0755 bzip2-shared %{buildroot}%{_bindir}/bzip2
install -pm0755 bzip2recover %{buildroot}%{_bindir}/bzip2recover
ln -s bzip2 %{buildroot}%{_bindir}/bunzip2
ln -s bzip2 %{buildroot}%{_bindir}/bzcat

install -pm0755 bzgrep bzmore bzdiff %{buildroot}%{_bindir}/
ln -s bzgrep %{buildroot}%{_bindir}/bzegrep
ln -s bzgrep %{buildroot}%{_bindir}/bzfgrep
ln -s bzmore %{buildroot}%{_bindir}/bzless
ln -s bzdiff %{buildroot}%{_bindir}/bzcmp

install -pm0644 bzlib.h %{buildroot}%{_includedir}/bzlib.h
install -pm0755 libbz2.so.1.0.8 %{buildroot}%{_libdir}/libbz2.so.1.0.8
ln -s libbz2.so.1.0.8 %{buildroot}%{_libdir}/libbz2.so.1.0
ln -s libbz2.so.1.0 %{buildroot}%{_libdir}/libbz2.so

install -pm0644 bzip2.1 bzgrep.1 bzmore.1 bzdiff.1 \
  %{buildroot}%{_mandir}/man1/
printf '.so man1/bzgrep.1\n' >%{buildroot}%{_mandir}/man1/bzegrep.1
printf '.so man1/bzgrep.1\n' >%{buildroot}%{_mandir}/man1/bzfgrep.1
printf '.so man1/bzmore.1\n' >%{buildroot}%{_mandir}/man1/bzless.1
printf '.so man1/bzdiff.1\n' >%{buildroot}%{_mandir}/man1/bzcmp.1

%check
%make_build test

%files
%license LICENSE
%doc CHANGES README README.COMPILATION.PROBLEMS
%{_bindir}/bunzip2
%{_bindir}/bzcat
%{_bindir}/bzcmp
%{_bindir}/bzdiff
%{_bindir}/bzegrep
%{_bindir}/bzfgrep
%{_bindir}/bzgrep
%{_bindir}/bzip2
%{_bindir}/bzip2recover
%{_bindir}/bzless
%{_bindir}/bzmore
%{_mandir}/man1/*.1*

%files libs
%license LICENSE
%{_libdir}/libbz2.so.1.0*

%files devel
%license LICENSE
%{_includedir}/bzlib.h
%{_libdir}/libbz2.so

%changelog
* Tue Aug 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.8-1
- Initial openEuler RISC-V package based on cross-distribution release evidence.
