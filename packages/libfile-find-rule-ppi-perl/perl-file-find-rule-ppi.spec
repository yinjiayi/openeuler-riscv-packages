# SPDX-License-Identifier: Apache-2.0
Name:           perl-file-find-rule-ppi
Version:        1.07
Release:        1%{?dist}
Summary:        Search Perl source files with File::Find::Rule and PPI
License:        Apache-2.0 AND (GPL-1.0-or-later OR Artistic-1.0-Perl)
URL:            https://metacpan.org/dist/File-Find-Rule-PPI
Source0:        File-Find-Rule-PPI-1.07.tar.gz
Source1:        Dist-Zilla-6.030.tar.gz
Source2:        Dist-Zilla-Plugin-Test-ReportPrereqs-0.029.tar.gz
Source3:        version-0.9908.tar.gz
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(File::Find::Rule) >= 0.20
BuildRequires:  perl(PPI) >= 1.000
BuildRequires:  perl(PPI::Find)
BuildRequires:  perl(Params::Util) >= 0.10
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
BuildRequires:  make
BuildRequires:  findutils
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-generators
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(CPAN::Meta) >= 2.120900
BuildRequires:  perl(CPAN::Meta::Prereqs)
BuildRequires:  tar
BuildRequires:  gzip
Requires:       perl
Requires:       perl(File::Find::Rule) >= 0.20
Requires:       perl(PPI) >= 1.000
Requires:       perl(PPI::Find)
Requires:       perl(Params::Util) >= 0.10
Requires:       perl(strict)
Requires:       perl(warnings)

%description
File::Find::Rule::PPI extends File::Find::Rule to search Perl source
using PPI's parsed documents and tokens.

%prep
%autosetup -n File-Find-Rule-PPI-%{version} -p1
# Retain original generated-source notices; no donor code is executed.
tar -xOzf "%{SOURCE1}" Dist-Zilla-6.030/LICENSE > LICENSE.Dist-Zilla
tar -xOzf "%{SOURCE2}" Dist-Zilla-Plugin-Test-ReportPrereqs-0.029/LICENSE > LICENSE.ReportPrereqs
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
%{perl_vendorlib}/File/Find/Rule/PPI.pm
%{_mandir}/man3/File::Find::Rule::PPI.3*

%changelog
* Mon Nov 09 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.07-1
- Package File::Find::Rule::PPI with unchanged defaults and generated-source notices.
