# SPDX-License-Identifier: Apache-2.0
Name:           libx86emu
Version:        3.7
Release:        1%{?dist}
Summary:        Library for emulating x86 instructions
License:        HPND
URL:            https://github.com/wfeldt/libx86emu
Source0:        libx86emu-%{version}.tar.gz
Patch0:         0001-test-remove-unused-x86-io-header.patch

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  nasm
BuildRequires:  perl

%description
libx86emu provides a portable library for emulating x86 instructions,
including real-mode and basic protected-mode execution.

%package devel
Summary:        Development files for libx86emu
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
The public x86 emulation header and shared-library linker name.

%prep
%autosetup -n libx86emu-ce81129c57fdfbf690bebc210a8db97d926cc5e7 -p1
# The official GitHub tag archive does not include the generated VERSION file.
printf '%s\n' '%{version}' > VERSION

%build
# git2log requires a .git directory absent from the immutable source archive.
%make_build GIT2LOG=true CC=%{__cc} CFLAGS='%{optflags} -fPIC -fvisibility=hidden -fomit-frame-pointer -Wall' LDFLAGS='%{?build_ldflags}'

%install
%make_install GIT2LOG=true LIBDIR=%{_libdir}

%check
# Upstream test target runs all 60 fixtures and compares the 42 with .done
# reference outputs; the remaining 18 fixtures are intentionally run-only.
%make_build GIT2LOG=true test

%files
%license LICENSE LICENSE_INFO
%doc README.md
%{_libdir}/libx86emu.so.3*

%files devel
%license LICENSE LICENSE_INFO
%{_includedir}/x86emu.h
%{_libdir}/libx86emu.so

%changelog
* Tue Sep 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.7-1
- Package the official upstream 3.7 release for openEuler RISC-V.
