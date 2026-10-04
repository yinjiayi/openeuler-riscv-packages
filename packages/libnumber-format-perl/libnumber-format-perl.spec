# SPDX-License-Identifier: Apache-2.0
Name:           perl-Number-Format
Version:        1.79
Release:        1%{?dist}
Summary:        Format numeric values, prices, pictures and byte quantities
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Number-Format
Source0:        Number-Format-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  glibc-all-langpacks
BuildRequires:  make
BuildRequires:  perl >= 5.12.0
BuildRequires:  perl-Carp
BuildRequires:  perl-Exporter
BuildRequires:  perl-ExtUtils-MakeMaker >= 6.78
BuildRequires:  perl-PathTools
BuildRequires:  perl-Test-Harness
BuildRequires:  perl-Test-Simple >= 0.96
BuildRequires:  perl-constant
BuildRequires:  perl-generators
Requires:       coreutils
Requires:       perl >= 5.12.0
Requires:       perl-Carp
Requires:       perl-Digest-SHA
Requires:       perl-Exporter
Requires:       perl-constant

%description
Number::Format formats numeric values, monetary values, fixed-width
pictures and traditional or IEC byte quantities. It also rounds and
parses formatted values and supports explicit formatting configurations.

%prep
%autosetup -n Number-Format-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# The original report-prereqs test is diagnostic, not a dependency gate.
%{__perl} -MExtUtils::MakeMaker -MTest::More -MTest::Harness -MFile::Spec -MCarp -MExporter -Mbase -Mconstant -Mwarnings -Mstrict -MPOSIX -e 'ExtUtils::MakeMaker->VERSION(6.78); Test::More->VERSION(0.96); for my $locale (qw(de_DE.utf8 ru_RU.utf8 en_US.utf8 C)) { die "missing locale $locale" unless defined POSIX::setlocale(POSIX::LC_ALL(), $locale); print "Default-test locale $locale available\n"; }'
%make_build test
# Preserve all ten original default files and fail closed on locale skips.
%{__perl} -Mblib -MTest::Harness -e 'my @t=sort glob "t/*.t"; die "incomplete default suite" unless @t==10; $Test::Harness::verbose=1; my($s,$failed,$todo)=Test::Harness::execute_tests(tests=>\@t); my $want={files=>10,tests=>10,good=>10,max=>183,ok=>183,bad=>0,skipped=>0,sub_skipped=>0,todo=>0,bonus=>0}; for my $key (sort keys %$want) { die "Harness $key mismatch" unless defined($s->{$key}) && $s->{$key}==$want->{$key}; } die "failed/TODO tests" if keys(%$failed) || keys(%$todo); print "Full default Harness gate Files=10 Tests=183 Skip=0 Failure=0\n";'

%files
%license LICENSE README Changes
%{perl_vendorlib}/Number/Format.pm
%{_mandir}/man3/Number::Format.3*

%changelog
* Sun Oct 04 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.79-1
- Preserve official stable source and full default suite with real locale data.
