# SPDX-License-Identifier: Apache-2.0
Name:           perl-test-diaginc
Version:        0.010
Release:        1%{?dist}
Summary:        Diagnose loaded Perl modules when tests fail
License:        Apache-2.0 AND (GPL-1.0-or-later OR Artistic-1.0-Perl)
URL:            https://metacpan.org/dist/Test-DiagINC
Source0:        Test-DiagINC-0.010.tar.gz
Source1:        Dist-Zilla-6.025.tar.gz
Source2:        Dist-Zilla-Plugin-Test-ReportPrereqs-0.028.tar.gz
Source3:        version-0.9908.tar.gz
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(B)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
BuildRequires:  make
BuildRequires:  findutils
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-generators
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Capture::Tiny) >= 0.21
BuildRequires:  perl(Config)
BuildRequires:  perl(CPAN::Meta)
BuildRequires:  tar
BuildRequires:  gzip
Requires:       perl
Requires:       perl(B)
Requires:       perl(Cwd)
Requires:       perl(File::Spec)
Requires:       perl(strict)
Requires:       perl(warnings)

%description
Test::DiagINC reports loaded Perl modules and their versions when a test
fails or its process exits unsuccessfully.

%prep
%autosetup -n Test-DiagINC-%{version} -p1
# Preserve complete notices for the checked-in generated files.
tar -xOzf "%{SOURCE1}" Dist-Zilla-6.025/LICENSE > LICENSE.Dist-Zilla
tar -xOzf "%{SOURCE2}" Dist-Zilla-Plugin-Test-ReportPrereqs-0.028/LICENSE > LICENSE.ReportPrereqs
tar -xOzf "%{SOURCE3}" version-0.9908/README > NOTICE.version
test -s LICENSE.Dist-Zilla && test -s LICENSE.ReportPrereqs && test -s NOTICE.version

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
%{perl_vendorlib}/Test/DiagINC.pm
%{_mandir}/man3/Test::DiagINC.3*

%changelog
* Mon Nov 09 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.010-1
- Package Test::DiagINC with its original tests and generated-file notices.
