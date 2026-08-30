# SPDX-License-Identifier: Apache-2.0
Name:           sipgrep
Version:        2.2.0
Release:        2%{?dist}
Summary:        A powerful pcap-aware tool command line tool to sniff, capture, display and troubleshoot SIP signaling over IP networks
License:        GPL-3.0-or-later
URL:            https://github.com/sipcapture/sipgrep
Source0:        sipgrep-2.2.0.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libpcap-devel
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  pcre2-devel

%description
A powerful pcap-aware tool command line tool to sniff, capture, display and troubleshoot SIP signaling over IP networks

%prep
%autosetup -p1
autoreconf -fi

%build
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

%changelog
* Mon Aug 31 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.2.0-2
- Regenerate configure and add the required libpcap and PCRE2 development dependencies.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.2.0-1
- Initial openEuler RISC-V package from the full package inventory.
