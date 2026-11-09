# SPDX-License-Identifier: Apache-2.0
Name:           perl-parse-edid
Version:        1.0.7
Release:        1%{?dist}
Summary:        Parse display EDID data from Perl
License:        GPL-3.0-or-later
URL:            https://metacpan.org/dist/Parse-EDID
Source0:        Parse-EDID-1.0.7.tar.gz
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(Exporter)
BuildRequires:  perl(base)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
BuildRequires:  make
BuildRequires:  findutils
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-generators
BuildRequires:  perl(Test::More) >= 0.93
BuildRequires:  perl(Test::Warn)
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(Test::Pod::Coverage)
BuildRequires:  perl(Pod::Coverage)
BuildRequires:  perl(Devel::Symdump)
BuildRequires:  perl(Pod::Find)
BuildRequires:  perl(English)
Requires:       perl
Requires:       perl(Exporter)
Requires:       perl(base)
Requires:       perl(strict)
Requires:       perl(warnings)

%description
Parse::EDID decodes the binary display identification data reported by
monitors and extracts EDID blocks from text output such as xrandr.

%prep
%autosetup -n Parse-EDID-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
%{__make} pure_install DESTDIR="%{buildroot}"
find "%{buildroot}" -type f \( -name .packlist -o -name perllocal.pod \) -delete

%check
%{__make} test TEST_VERBOSE=1

%files
%license LICENSE
%doc README Changes
%{perl_vendorlib}/Parse/EDID.pm
%{_mandir}/man3/Parse::EDID.3*

%changelog
* Mon Nov 09 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.7-1
- Package Parse::EDID with its original tests and GPL license.
