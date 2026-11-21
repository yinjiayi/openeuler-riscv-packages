# SPDX-License-Identifier: Apache-2.0
Name:           perl-test-tempdir-tiny
Version:        0.018
Release:        1%{?dist}
Summary:        Temporary directories for Perl tests with failure retention
License:        Apache-2.0 AND (GPL-1.0-or-later OR Artistic-1.0-Perl)
URL:            https://metacpan.org/dist/Test-TempDir-Tiny
Source0:        Test-TempDir-Tiny-0.018.tar.gz
Source1:        Dist-Zilla-6.012.tar.gz
Source2:        Dist-Zilla-Plugin-Test-ReportPrereqs-0.027.tar.gz
Source3:        version-0.9908.tar.gz
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(B)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(Exporter) >= 5.57
BuildRequires:  perl(File::Path) >= 2.07
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(File::Temp) >= 0.2308
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
BuildRequires:  make
BuildRequires:  findutils
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-generators
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Harness)
BuildRequires:  perl(CPAN::Meta) >= 2.120900
BuildRequires:  perl(CPAN::Meta::Prereqs)
BuildRequires:  perl(Capture::Tiny) >= 0.12
BuildRequires:  tar
BuildRequires:  gzip
Requires:       perl
Requires:       perl(B)
Requires:       perl(Carp)
Requires:       perl(Cwd)
Requires:       perl(Exporter) >= 5.57
Requires:       perl(File::Path) >= 2.07
Requires:       perl(File::Spec::Functions)
Requires:       perl(File::Temp) >= 0.2308
Requires:       perl(strict)
Requires:       perl(warnings)

%description
Test::TempDir::Tiny creates temporary directories for tests, cleaning up
after passing tests and preserving directories after failures.

%prep
%autosetup -n Test-TempDir-Tiny-%{version} -p1
# Extract original license/notice bytes only; no donor code is executed.
tar -xOzf "%{SOURCE1}" Dist-Zilla-6.012/LICENSE > LICENSE.Dist-Zilla
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
%{perl_vendorlib}/Test/TempDir/Tiny.pm
%{_mandir}/man3/Test::TempDir::Tiny.3*

%changelog
* Mon Nov 09 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.018-1
- Package Test::TempDir::Tiny with unchanged upstream tests and generated-source notices.
