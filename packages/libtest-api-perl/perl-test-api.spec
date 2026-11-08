# SPDX-License-Identifier: Apache-2.0
Name:           perl-test-api
Version:        0.010
Release:        1%{?dist}
Summary:        Check the public Perl API provided by a module
License:        Apache-2.0 AND (GPL-1.0-or-later OR Artistic-1.0-Perl)
URL:            https://metacpan.org/dist/Test-API
Source0:        Test-API-0.010.tar.gz
Source1:        Dist-Zilla-6.011.tar.gz
Source2:        Dist-Zilla-Plugin-Test-ReportPrereqs-0.027.tar.gz
Source3:        version-0.9908.tar.gz
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(Symbol)
BuildRequires:  perl(Test::Builder::Module)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
BuildRequires:  make
BuildRequires:  findutils
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-generators
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Test::Builder::Tester)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(constant)
BuildRequires:  perl(lib)
BuildRequires:  perl(CPAN::Meta)
BuildRequires:  perl(CPAN::Meta::Prereqs)
BuildRequires:  tar
BuildRequires:  gzip
Requires:       perl
Requires:       perl(Symbol)
Requires:       perl(Test::Builder::Module)
Requires:       perl(strict)
Requires:       perl(warnings)

%description
Test::API checks the functions, exports, and methods provided by a Perl
module. It can identify unexpected changes to a module's public interface.

%prep
%autosetup -n Test-API-%{version} -p1
# Extract the original donor notices only; no donor code is executed.
tar -xOzf "%{SOURCE1}" Dist-Zilla-6.011/LICENSE > LICENSE.Dist-Zilla
tar -xOzf "%{SOURCE2}" Dist-Zilla-Plugin-Test-ReportPrereqs-0.027/LICENSE > LICENSE.ReportPrereqs
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
%{perl_vendorlib}/Test/API.pm
%{_mandir}/man3/Test::API.3*

%changelog
* Sun Nov 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.010-1
- Package Test::API with unchanged upstream defaults and generated-source notices.
