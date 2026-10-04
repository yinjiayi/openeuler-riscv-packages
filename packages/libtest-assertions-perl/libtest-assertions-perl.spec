# SPDX-License-Identifier: Apache-2.0
# Only the two sprintf-VERSION capabilities are supplied explicitly.
# Preserve automatic Requires generation and every other generated Provides.
%global __provides_exclude ^perl[(]Test::Assertions(::TestScript)?[)]([[:space:]]|$)
Name:           perl-Test-Assertions
Version:        1.054
Release:        1%{?dist}
Summary:        Building blocks for unit tests and runtime assertions
License:        GPL-2.0-only
URL:            https://metacpan.org/dist/Test-Assertions
Source0:        Test-Assertions-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-Carp
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Getopt-Long
BuildRequires:  perl-Log-Trace
BuildRequires:  perl-PathTools
BuildRequires:  perl-Test-Harness
BuildRequires:  perl-Test-Pod >= 1.00
BuildRequires:  perl-Test-Pod-Coverage >= 1.00
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators
Requires:       coreutils
Requires:       perl
Requires:       perl-Carp
Requires:       perl-Digest-SHA
Requires:       perl-File-Temp
Requires:       perl-Getopt-Long
Requires:       perl-IO-CaptureOutput
Requires:       perl-Log-Trace
Requires:       perl-PathTools
Requires:       perl-Test-Simple
Provides:       perl(Test::Assertions) = 1.054
Provides:       perl(Test::Assertions::TestScript) = 1.018

%description
Test::Assertions supplies deep comparisons, TAP assessment, file comparisons,
compilation checks and runtime assertion styles. TestScript supplies tracing
and command-line test setup. This dependency-held draft retains both modules
and COMPILES stderr capture; unavailable suppliers are not silently removed.

%prep
%autosetup -n Test-Assertions-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Explicit default suppliers prevent upstream POD skip-all paths.
%{__perl} -MLog::Trace -MTest::More -MTest::Harness -MTest::Pod -MTest::Pod::Coverage -e 'Test::Pod->VERSION("1.00"); Test::Pod::Coverage->VERSION("1.00"); die "LogTrace API missing" unless Log::Trace->can("import");'
%make_build test
# Keep all four original tests and child fixtures. POD totals are dynamic.
%{__perl} -Mblib -MTest::Harness -e 'my @t=sort glob "t/*.t"; die "incomplete default suite" unless @t==4; $Test::Harness::verbose=1; my($s,$failed,$todo)=Test::Harness::execute_tests(tests=>\@t); my $want={files=>4,tests=>4,good=>4,bad=>0,skipped=>0,sub_skipped=>0,todo=>0,bonus=>0}; for my $key (sort keys %$want) { die "Harness $key mismatch" unless defined($s->{$key}) && $s->{$key}==$want->{$key}; } die "incomplete assertion plans" unless defined($s->{max}) && defined($s->{ok}) && $s->{max}>=59 && $s->{max}==$s->{ok}; die "failed/TODO tests" if keys(%$failed) || keys(%$todo); print "Full original Harness gate Files=4 Tests=$s->{ok} Skip=0 Failure=0\n";'

%files
%license COPYING README Changes lib/Test/Assertions.pm lib/Test/Assertions/TestScript.pm lib/Test/Assertions/Manual.pod
%{perl_vendorlib}/Test/Assertions.pm
%{perl_vendorlib}/Test/Assertions/
%{_mandir}/man3/Test::Assertions.3*
%{_mandir}/man3/Test::Assertions::TestScript.3*
%{_mandir}/man3/Test::Assertions::Manual.3*

%changelog
* Sun Oct 04 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.054-1
- Prepare complete dependency-held draft; retain original source and tests.
