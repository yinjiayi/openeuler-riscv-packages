# SPDX-License-Identifier: Apache-2.0
Name:           perl-Mixin-Linewise
Version:        0.111
Release:        1%{?dist}
Summary:        Generate linewise readers and writers for files and strings
License:        GPL-1.0-or-later OR Artistic-1.0
URL:            https://metacpan.org/dist/Mixin-Linewise
Source0:        Mixin-Linewise-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl >= 5.12.0
BuildRequires:  perl-Carp
BuildRequires:  perl-Encode
BuildRequires:  perl-ExtUtils-MakeMaker >= 6.78
BuildRequires:  perl-PathTools
BuildRequires:  perl-PerlIO-utf8_strict
BuildRequires:  perl-Sub-Exporter
BuildRequires:  perl-Test-Harness
BuildRequires:  perl-Test-Simple >= 0.96
BuildRequires:  perl-generators
Requires:       coreutils
Requires:       perl >= 5.12.0
Requires:       perl-Carp
Requires:       perl-Digest-SHA
Requires:       perl-Encode
Requires:       perl-File-Temp
Requires:       perl-PerlIO-utf8_strict
Requires:       perl-Sub-Exporter

%description
Mixin::Linewise::Readers and Writers generate file and string methods
around caller-supplied handle methods, with configurable encoding layers.
The top-level Mixin::Linewise namespace is documentation-only and
intentionally raises an exception when loaded.

%prep
%autosetup -n Mixin-Linewise-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Original report-prereqs warns then passes; use explicit dependency gates.
%{__perl} -MExtUtils::MakeMaker -MTest::More -MTest::Harness -MEncode -MFile::Spec -MIO::File -MCarp -MPerlIO::utf8_strict -MSub::Exporter -Mlib -Mutf8 -Mstrict -Mwarnings -e 'ExtUtils::MakeMaker->VERSION(6.78); Test::More->VERSION(0.96); print "Default-test dependencies verified\n";'
%make_build test
# All four original default files; do not confuse files with TAP assertions.
%{__perl} -Mblib -MTest::Harness -e 'my @t=sort glob "t/*.t"; die "incomplete default suite" unless @t==4; $Test::Harness::verbose=1; my($s,$failed,$todo)=Test::Harness::execute_tests(tests=>\@t); my $want={files=>4,tests=>4,good=>4,max=>17,ok=>17,bad=>0,skipped=>0,sub_skipped=>0,todo=>0,bonus=>0}; for my $key (sort keys %$want) { die "Harness $key mismatch" unless defined($s->{$key}) && $s->{$key}==$want->{$key}; } die "failed/TODO tests" if keys(%$failed) || keys(%$todo); print "Full default Harness gate Files=4 Tests=17 Skip=0 Failure=0\n";'

%files
%license LICENSE README Changes
%{perl_vendorlib}/Mixin/Linewise.pm
%{perl_vendorlib}/Mixin/Linewise/
%{_mandir}/man3/Mixin::Linewise.3*
%{_mandir}/man3/Mixin::Linewise::Readers.3*
%{_mandir}/man3/Mixin::Linewise::Writers.3*

%changelog
* Mon Oct 05 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.111-1
- Preserve official source, complete default tests and original license terms.
