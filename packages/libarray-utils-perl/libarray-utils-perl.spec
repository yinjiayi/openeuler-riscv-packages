# SPDX-License-Identifier: Apache-2.0
Name:           perl-Array-Utils
Version:        0.5
Release:        1%{?dist}
Summary:        Pure-Perl array set operations
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Array-Utils
Source0:        Array-Utils-%{version}.tar.gz
Source1:        perl538-Copying
Source2:        perl538-Artistic

BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl(Test::Harness)
BuildRequires:  perl-generators

%description
Array::Utils supplies pure-Perl unique, intersection, symmetric
difference, and subtraction operations for lists.

%prep
%autosetup -n Array-Utils-%{version} -p1
cp -p %{SOURCE1} perl538-Copying
cp -p %{SOURCE2} perl538-Artistic

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# The complete upstream default suite is the one t/array-utils.t file.
timeout --kill-after=10s 180s %make_build test
# Repeat the unchanged default file with strict TAP statistics; never skip tests.
timeout --kill-after=10s 180s %{__perl} -Iblib/lib -Iblib/arch -MTest::Harness -e 'my @t=sort glob("t/*.t"); die "default file set" unless join(" ",@t) eq "t/array-utils.t"; my ($total,$failed)=Test::Harness::execute_tests(tests=>\@t); for my $k (qw(files tests good max ok bad skipped sub_skipped todo bonus)) { die "missing Harness $k" unless exists $total->{$k}; } for my $k (qw(files tests good)) { die "Harness $k" unless $total->{$k}==1; } for my $k (qw(max ok)) { die "Harness $k" unless $total->{$k}==17; } for my $k (qw(bad skipped sub_skipped todo bonus)) { die "Harness $k" unless $total->{$k}==0; } die "failed TAP" if keys %$failed; print "Complete original Harness Files=1 Assertions=17 Passed=17 Skips=0 TODO=0 Bonus=0 Failures=0\n";'

%files
%license Utils.pm perl538-Copying perl538-Artistic
%doc Changes README
%{perl_vendorlib}/Array/Utils.pm
%{_mandir}/man3/Array::Utils.3*

%changelog
* Tue Oct 06 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.5-1
- Retain the original grant and complete pinned Perl license terms.
- Bound the intact default suite and require 17 passes with zero skips or TODO.

* Tue Sep 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.5-1
- Package the official CPAN release and complete upstream test suite.
