# SPDX-License-Identifier: Apache-2.0
Name:           perl-Class-Accessor-Chained
Version:        0.01
Release:        1%{?dist}
Summary:        Generate ordinary and fast chained object accessors
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Class-Accessor-Chained
Source0:        Class-Accessor-Chained-%{version}.tar.gz
Source1:        perl-5.8.7-README
Source2:        perl-5.8.7-Artistic
Source3:        perl-5.8.7-Copying

BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-Carp
BuildRequires:  perl-Class-Accessor
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Harness
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators
Requires:       coreutils
Requires:       perl
Requires:       perl-Carp
Requires:       perl-Class-Accessor
Requires:       perl-Digest-SHA
Requires:       perl(Scalar::Util)

%description
Class::Accessor::Chained generates accessors that return their object when
setting a value, allowing chained calls. Its ordinary and Fast interfaces
retain upstream behavior and depend on Class::Accessor. Only Chained declares
its own VERSION 0.01; Chained::Fast has no version declaration of its own.

%prep
%autosetup -n Class-Accessor-Chained-%{version}
cp -p %{SOURCE1} %{SOURCE2} %{SOURCE3} .

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
%{__perl} -MClass::Accessor -MClass::Accessor::Fast -MTest::More -MTest::Harness -e 'die "ClassAccessor provider missing" unless Class::Accessor->can("mk_accessors") && Class::Accessor::Fast->can("mk_ro_accessors") && Class::Accessor::Fast->can("mk_wo_accessors");'
%make_build test
# Preserve both complete original tests; fail closed on TAP failures and skips.
%{__perl} -Mblib -MTest::Harness -e 'my @t=sort glob "t/*.t"; die "incomplete default suite" unless @t==2; $Test::Harness::verbose=1; my($s,$failed,$todo)=Test::Harness::execute_tests(tests=>\@t); my $want={files=>2,tests=>2,good=>2,max=>8,ok=>8,bad=>0,skipped=>0,sub_skipped=>0,todo=>0,bonus=>0}; for my $key (sort keys %$want) { die "Harness $key mismatch" unless defined($s->{$key}) && $s->{$key}==$want->{$key}; } die "failed/TODO tests" if keys(%$failed) || keys(%$todo); print "Full default Harness gate Files=2 Tests=8 Skip=0 Failure=0\n";'

%files
%license README Changes lib/Class/Accessor/Chained.pm lib/Class/Accessor/Chained/Fast.pm perl-5.8.7-README perl-5.8.7-Artistic perl-5.8.7-Copying
%{perl_vendorlib}/Class/Accessor/Chained.pm
%{perl_vendorlib}/Class/Accessor/Chained/
%{_mandir}/man3/Class::Accessor::Chained.3*
%{_mandir}/man3/Class::Accessor::Chained::Fast.3*

%changelog
* Sun Oct 04 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.01-1
- Preserve official source, complete default tests and actual module notices.
