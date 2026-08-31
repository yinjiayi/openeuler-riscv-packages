# SPDX-License-Identifier: Apache-2.0
Name:           jwhois
Version:        4.0
Release:        1%{?dist}
Summary:        An Internet Whois client
License:        GPL-3.0-or-later
URL:            https://www.gnu.org/software/jwhois/
Source0:        jwhois-4.0.tar.gz
BuildRequires:  gcc
BuildRequires:  make


%description
An Internet Whois client

%prep
%autosetup -p1
# The 4.0 release defines timeout_init in utils.c but omits its declaration.
sed -i '/^int add_text_to_buffer/i void timeout_init(void);' include/utils.h

%build
%configure
%make_build

%install
%make_install
%find_lang %{name}
rm -f %{buildroot}%{_infodir}/dir

%check
%make_build check

%files -f %{name}.lang
%license COPYING
%doc AUTHORS
%doc ChangeLog
%doc NEWS
%doc README
%{_bindir}/*
%config(noreplace) %{_sysconfdir}/jwhois.conf
%{_infodir}/jwhois.info*
%{_mandir}/man1/jwhois.1*
%{_mandir}/*/man1/jwhois.1*

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.0-1
- Initial openEuler RISC-V package from the full package inventory.
