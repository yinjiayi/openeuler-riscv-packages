# SPDX-License-Identifier: Apache-2.0
Name:           sipgrep
Version:        2.2.0
Release:        1%{?dist}
Summary:        A powerful pcap-aware tool command line tool to sniff, capture, display and troubleshoot SIP signaling over IP networks
License:        GPL-3.0-or-later
URL:            https://github.com/sipcapture/sipgrep
Source0:        sipgrep-2.2.0.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
A powerful pcap-aware tool command line tool to sniff, capture, display and troubleshoot SIP signaling over IP networks

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install
find %{buildroot} \( -type f -o -type l \) -printf '/%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%make_build check

%files -f %{name}.files
%license COPYING
%doc README.md

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.2.0-1
- Initial openEuler RISC-V package from the full package inventory.
