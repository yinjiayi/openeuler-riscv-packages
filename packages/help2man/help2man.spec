# SPDX-License-Identifier: Apache-2.0
Name:           help2man
Version:        1.49.3
Release:        1%{?dist}
Summary:        Generate simple manual pages from program output
License:        GPL-3.0-or-later
URL:            https://www.gnu.org/software/help2man/
Source0:        help2man-%{version}.tar.xz

BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-Encode
BuildRequires:  perl-Locale-gettext

Requires:       perl
Requires:       perl-Locale-gettext

%description
GNU help2man produces manual pages from a program's --help and --version output.

%prep
%autosetup -p1

%build
%configure --enable-nls --libdir=%{_libdir}/help2man
%make_build

%install
%make_install
rm -f %{buildroot}%{_infodir}/dir

%check
cat > fixture <<'EOF'
#!/bin/sh
case "$1" in
  --version) echo 'fixture 1.0' ;;
  --help) echo 'Usage: fixture [OPTION]'; echo '  --flag  documented flag' ;;
esac
EOF
chmod +x fixture
./help2man --no-info --name='fixture utility' ./fixture > fixture.1
grep -F 'fixture utility' fixture.1
grep -F '\-\-flag' fixture.1

%files
%license COPYING
%doc NEWS README THANKS
%{_bindir}/help2man
%{_libdir}/help2man/
%{_datadir}/locale/*/LC_MESSAGES/help2man.mo
%{_infodir}/help2man*.info*
%{_mandir}/man1/help2man.1*
%{_mandir}/*/man1/help2man.1*

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.49.3-1
- Initial openEuler RISC-V package from frozen lineage and official source evidence.
