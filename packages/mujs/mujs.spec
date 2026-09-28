# SPDX-License-Identifier: Apache-2.0
Name:           mujs
Version:        1.3.10
Release:        1%{?dist}
Summary:        Lightweight embeddable JavaScript interpreter
License:        ISC
URL:            https://mujs.com/
Source0:        mujs-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconf-pkg-config
BuildRequires:  readline-devel

%description
MuJS provides a small JavaScript interpreter, a script pretty-printer, and a
shared C library for embedding JavaScript in applications.

%package devel
Summary:        Development files for MuJS
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconf-pkg-config

%description devel
The MuJS public C header and pkg-config metadata for embedding its shared
library in other applications.

%prep
%autosetup -p1

%build
%make_build release \
  CC=%{__cc} \
  CFLAGS='%{optflags} -std=c99 -pedantic -Wall -Wextra -Wno-unused-parameter' \
  OPTIM=

%install
%make_install install-shared \
  prefix=%{_prefix} \
  bindir=%{_bindir} \
  incdir=%{_includedir} \
  libdir=%{_libdir}

%check
cat > smoke.js <<'EOF'
var value = JSON.parse('{"arch":"riscv64","numbers":[6,7]}');
if (value.arch !== 'riscv64' || value.numbers[0] * value.numbers[1] !== 42)
    throw new Error('MuJS interpreter result mismatch');
print('mujs-runtime-ok');
EOF
./build/release/mujs smoke.js | grep -Fx 'mujs-runtime-ok'
./build/release/mujs-pp smoke.js > smoke.pretty.js
./build/release/mujs smoke.pretty.js | grep -Fx 'mujs-runtime-ok'

%files
%license COPYING
%doc AUTHORS README
%{_bindir}/mujs
%{_bindir}/mujs-pp
%{_libdir}/libmujs.so

%files devel
%license COPYING
%{_includedir}/mujs.h
%{_libdir}/pkgconfig/mujs.pc

%changelog
* Mon Sep 28 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.3.10-1
- Initial openEuler RISC-V package from the official ISC-licensed archive.
