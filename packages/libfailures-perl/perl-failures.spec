# SPDX-License-Identifier: Apache-2.0
Name:           perl-failures
Version:        0.004
Release:        1%{?dist}
Summary:        Create typed exception hierarchies in Perl
License:        Apache-2.0 AND (GPL-1.0-or-later OR Artistic-1.0-Perl)
URL:            https://metacpan.org/dist/failures
Source0:        failures-0.004.tar.gz
Source1:        Dist-Zilla-5.019.tar.gz
Source2:        Dist-Zilla-Plugin-Test-ReportPrereqs-0.013.tar.gz
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(Carp)
BuildRequires:  perl(Class::Tiny)
BuildRequires:  perl(overload)
BuildRequires:  perl(parent)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
BuildRequires:  make
BuildRequires:  findutils
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-generators
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(List::Util)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(lib)
BuildRequires:  perl(version)
BuildRequires:  perl(CPAN::Meta)
BuildRequires:  perl(CPAN::Meta::Requirements) >= 2.120900
BuildRequires:  perl(Test::FailWarnings) >= 0.007
BuildRequires:  tar
BuildRequires:  gzip
Requires:       perl
Requires:       perl(Carp)
Requires:       perl(Class::Tiny)
Requires:       perl(overload)
Requires:       perl(parent)
Requires:       perl(strict)
Requires:       perl(warnings)

%description
The failures and custom::failures modules create typed exception hierarchies.
Applications can define custom types that retain messages, traces, and payloads.

%prep
%autosetup -n failures-%{version} -p1
# Extract original license/notice bytes only; no donor code is executed.
tar -xOzf "%{SOURCE1}" Dist-Zilla-5.019/LICENSE > LICENSE.Dist-Zilla
tar -xOzf "%{SOURCE2}" Dist-Zilla-Plugin-Test-ReportPrereqs-0.013/LICENSE > LICENSE.ReportPrereqs
test -s LICENSE.Dist-Zilla
test -s LICENSE.ReportPrereqs

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
%{perl_vendorlib}/failures.pm
%{perl_vendorlib}/custom/failures.pm
%{_mandir}/man3/failures.3*
%{_mandir}/man3/custom::failures.3*

%changelog
* Mon Nov 09 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.004-1
- Package failures with unchanged upstream tests and generated-source notices.
