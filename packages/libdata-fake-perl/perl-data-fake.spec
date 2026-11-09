# SPDX-License-Identifier: Apache-2.0
Name:           perl-data-fake
Version:        0.006
Release:        1%{?dist}
Summary:        Generate synthetic test data with Perl
License:        Apache-2.0 AND (GPL-1.0-or-later OR Artistic-1.0-Perl)
URL:            https://metacpan.org/dist/Data-Fake
Source0:        Data-Fake-0.006.tar.gz
Source1:        Dist-Zilla-6.017.tar.gz
Source2:        Dist-Zilla-Plugin-Test-ReportPrereqs-0.028.tar.gz
Source3:        version-0.9908.tar.gz
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Import::Into)
BuildRequires:  perl(List::Util)
BuildRequires:  perl(Text::Lorem)
BuildRequires:  perl(Time::Piece)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
BuildRequires:  make
BuildRequires:  findutils
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-generators
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Deep)
BuildRequires:  perl(CPAN::Meta) >= 2.120900
BuildRequires:  perl(CPAN::Meta::Prereqs)
BuildRequires:  tar
BuildRequires:  gzip
Requires:       perl
Requires:       perl(Carp)
Requires:       perl(Exporter)
Requires:       perl(Import::Into)
Requires:       perl(List::Util)
Requires:       perl(Text::Lorem)
Requires:       perl(Time::Piece)
Requires:       perl(strict)
Requires:       perl(warnings)

%description
Data::Fake creates synthetic input for tests, including numbers, text,
dates, names, and Internet-style identifiers.

%prep
%autosetup -n Data-Fake-%{version} -p1
# Extract original license/notice bytes only; no donor code is executed.
tar -xOzf "%{SOURCE1}" Dist-Zilla-6.017/LICENSE > LICENSE.Dist-Zilla
tar -xOzf "%{SOURCE2}" Dist-Zilla-Plugin-Test-ReportPrereqs-0.028/LICENSE > LICENSE.ReportPrereqs
tar -xOzf "%{SOURCE3}" version-0.9908/README > NOTICE.version
test -s LICENSE.Dist-Zilla
test -s LICENSE.ReportPrereqs
test -s NOTICE.version

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
%{__make} pure_install DESTDIR="%{buildroot}"
find "%{buildroot}" -type f \( -name .packlist -o -name perllocal.pod \) -delete

%check
%{__make} test TEST_VERBOSE=1

%files
%license LICENSE LICENSE.Dist-Zilla LICENSE.ReportPrereqs NOTICE.version
%doc README Changes
%{perl_vendorlib}/Data/Fake.pm
%dir %{perl_vendorlib}/Data/Fake
%{perl_vendorlib}/Data/Fake/Company.pm
%{perl_vendorlib}/Data/Fake/Core.pm
%{perl_vendorlib}/Data/Fake/Dates.pm
%{perl_vendorlib}/Data/Fake/Examples.pod
%{perl_vendorlib}/Data/Fake/Internet.pm
%{perl_vendorlib}/Data/Fake/Names.pm
%{perl_vendorlib}/Data/Fake/Text.pm
%{_mandir}/man3/Data::Fake.3*
%{_mandir}/man3/Data::Fake::Company.3*
%{_mandir}/man3/Data::Fake::Core.3*
%{_mandir}/man3/Data::Fake::Dates.3*
%{_mandir}/man3/Data::Fake::Examples.3*
%{_mandir}/man3/Data::Fake::Internet.3*
%{_mandir}/man3/Data::Fake::Names.3*
%{_mandir}/man3/Data::Fake::Text.3*

%changelog
* Mon Nov 09 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.006-1
- Package Data::Fake with unchanged upstream tests and generated-source notices.
