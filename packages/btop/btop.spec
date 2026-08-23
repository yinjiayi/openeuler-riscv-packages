# SPDX-License-Identifier: Apache-2.0

Name:           btop
Version:        1.4.7
Release:        1%{?dist}
Summary:        A monitor of system resources, bpytop ported to C++
License:        Apache-2.0
URL:            https://github.com/aristocratos/btop
Source0:        btop-1.4.7.tar.gz
BuildRequires:  gcc-c++
BuildRequires:  make

%description
btop is a resource monitor for Linux that displays CPU, memory, disks,
network, and process activity in an interactive terminal interface.

%prep
%autosetup -p1 -n btop-%{version}

%build
%make_build \
  CXX="%{__cxx}" \
  CXXFLAGS="%{build_cxxflags}" \
  LDFLAGS="%{build_ldflags}" \
  PLATFORM=linux \
  ARCH=riscv64 \
  GPU_SUPPORT=false

%install
%make_build install \
  DESTDIR="%{buildroot}" \
  PREFIX="%{_prefix}" \
  PLATFORM=linux \
  ARCH=riscv64 \
  GPU_SUPPORT=false

%check
bin/btop --version | grep -F '1.4.7'
bin/btop --help >/dev/null
bin/btop --default-config >/dev/null

%files
%license LICENSE
%doc CHANGELOG.md
%{_bindir}/btop
%{_docdir}/btop/README.md
%{_datadir}/btop/themes/
%{_datadir}/applications/btop.desktop
%{_datadir}/icons/hicolor/48x48/apps/btop.png
%{_datadir}/icons/hicolor/scalable/apps/btop.svg

%changelog
* Fri Aug 21 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.4.7-1
- Initial openEuler RISC-V package using the upstream Linux Makefile.
