# SPDX-License-Identifier: Apache-2.0
Name:           perl-test-mockrandom
Version:        1.01
Release:        1%{?dist}
Summary:        Provide deterministic random sequences for Perl tests
License:        Apache-2.0 AND (GPL-1.0-or-later OR Artistic-1.0-Perl)
URL:            https://metacpan.org/dist/Test-MockRandom
Source0:        Test-MockRandom-1.01.tar.gz
Source1:        Dist-Zilla-5.012.tar.gz
Source2:        Dist-Zilla-Plugin-Test-ReportPrereqs-0.013.tar.gz
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(Carp)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
BuildRequires:  make
BuildRequires:  findutils
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-generators
BuildRequires:  perl(Test::More)
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(List::Util)
BuildRequires:  perl(lib)
BuildRequires:  perl(version)
BuildRequires:  perl(CPAN::Meta)
BuildRequires:  perl(CPAN::Meta::Requirements) >= 2.120900
BuildRequires:  tar
BuildRequires:  gzip
Requires:       perl
Requires:       perl(Carp)
Requires:       perl(strict)
Requires:       perl(warnings)

%description
Test::MockRandom supplies a deterministic sequence for Perl tests that
would otherwise depend on random input.

%prep
%autosetup -n Test-MockRandom-%{version} -p1
# Preserve the original notices for both checked-in generated files.
tar -xOzf "%{SOURCE1}" Dist-Zilla-5.012/LICENSE > LICENSE.Dist-Zilla
tar -xOzf "%{SOURCE2}" Dist-Zilla-Plugin-Test-ReportPrereqs-0.013/LICENSE > LICENSE.ReportPrereqs
test -s LICENSE.Dist-Zilla && test -s LICENSE.ReportPrereqs

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
%{__make} pure_install DESTDIR="%{buildroot}"
find "%{buildroot}" -type f \( -name .packlist -o -name perllocal.pod \) -delete

%check
%{__make} test TEST_VERBOSE=1

%files
%license LICENSE LICENSE.Dist-Zilla LICENSE.ReportPrereqs
%doc README Changes
%{perl_vendorlib}/Test/MockRandom.pm
%{_mandir}/man3/Test::MockRandom.3*

%changelog
* Mon Nov 09 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.01-1
- Package Test::MockRandom with its original tests and generator notices.
