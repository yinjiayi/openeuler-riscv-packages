# SPDX-License-Identifier: Apache-2.0
Name:           bftpd
Version:        6.7
Release:        1%{?dist}
Summary:        Small configurable FTP server
License:        GPL-2.0-only
URL:            https://bftpd.sourceforge.net/
Source0:        bftpd-6.7.tar.gz

BuildRequires:  gcc
BuildRequires:  make

%description
bftpd is a small and configurable FTP server that can run from inetd or as a
standalone daemon. This build does not enable optional PAM or zlib support.

%prep
%autosetup -p1 -n bftpd

%build
# Upstream's legacy configure macro treats both --enable-* and --disable-*
# as enabling the option.  Omit both flags to retain the disabled defaults.
%configure
%make_build

%install
install -D -m 0755 bftpd %{buildroot}%{_sbindir}/bftpd
install -D -m 0644 bftpd.8 %{buildroot}%{_mandir}/man8/bftpd.8
install -D -m 0600 bftpd.conf %{buildroot}%{_sysconfdir}/bftpd.conf

%check
./bftpd -v | grep -F 'Bftpd version %{version}'

%files
%license COPYING
%doc CHANGELOG README
%{_sbindir}/bftpd
%{_mandir}/man8/bftpd.8*
%config(noreplace) %{_sysconfdir}/bftpd.conf

%changelog
* Sat Aug 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 6.7-1
- Initial openEuler RISC-V package.
