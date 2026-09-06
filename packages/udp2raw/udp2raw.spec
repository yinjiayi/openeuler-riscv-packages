# SPDX-License-Identifier: Apache-2.0
Name:           udp2raw
Version:        20230206.0
Release:        2%{?dist}
Summary:        A tunnel that turns UDP traffic into encrypted UDP/FakeTCP/ICMP traffic using raw sockets
License:        MIT
URL:            https://github.com/wangyu-/udp2raw
Source0:        udp2raw-20230206.0.tar.gz
BuildRequires:  gcc-c++
BuildRequires:  make

%description
A tunnel that turns UDP traffic into encrypted UDP/FakeTCP/ICMP traffic using raw sockets

%prep
%autosetup -p1

%build
printf 'const char *gitversion = "%{version}";\n' > git_version.h
%make_build -o git_version dynamic cc_local=%{__cxx} OPT="%{optflags} %{?build_ldflags}"

%install
install -Dpm0755 udp2raw_dynamic %{buildroot}%{_bindir}/udp2raw

%check
./udp2raw_dynamic --help >/dev/null

%files
%{_bindir}/udp2raw
%license LICENSE.md
%doc README.md

%changelog
* Sun Sep 06 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 20230206.0-2
- Use the supported upstream dynamic Makefile target and install the executable.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 20230206.0-1
- Initial openEuler RISC-V package from the full package inventory.
