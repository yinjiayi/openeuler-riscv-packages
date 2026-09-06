# SPDX-License-Identifier: Apache-2.0
Name:           qbe
Version:        1.3
Release:        1%{?dist}
Summary:        Small embeddable compiler backend
License:        MIT
URL:            https://c9x.me/compile/
Source0:        qbe-%{version}.tar.xz

BuildRequires:  binutils
BuildRequires:  coreutils
BuildRequires:  diffutils
BuildRequires:  gawk
BuildRequires:  gcc
BuildRequires:  make

%description
QBE is a compact compiler backend that accepts a simple SSA intermediate
language and emits assembly for amd64, arm64, riscv64, and related ABIs.

%prep
%autosetup -p1

%build
%make_build \
  CC=%{__cc} \
  CFLAGS='%{build_cflags} -std=c99 -Wall -Wextra -Wpedantic' \
  LDFLAGS='%{build_ldflags}'

%install
%make_install PREFIX=%{_prefix}

%check
%make_build check-rv64

%files
%license LICENSE
%doc README
%{_bindir}/qbe

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.3-1
- Initial openEuler RISC-V package with the complete upstream riscv64 test route.
