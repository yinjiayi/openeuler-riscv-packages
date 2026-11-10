# SPDX-License-Identifier: Apache-2.0
Name:           perl-exporter-lite
Version:        0.09
Release:        1%{?dist}
Summary:        Lightweight exporting of Perl package variables and functions
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Exporter-Lite
Source0:        https://cpan.metacpan.org/authors/id/N/NE/NEILB/Exporter-Lite-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-generators
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Carp)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
Requires:       perl(Carp)
Requires:       perl(strict)
Requires:       perl(warnings)

%description
Lightweight exporting of Perl package variables and functions

%prep
%setup -q -n Exporter-Lite-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
%make_install

%check
make test

%files
%license lib/Exporter/Lite.pm
%doc README Changes
%{perl_vendorlib}/Exporter/Lite.pm
%{_mandir}/man3/Exporter::Lite.3pm*

%changelog
* Sun Nov 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.09-1
- Package fixed release, original grant and default tests.
