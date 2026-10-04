# SPDX-License-Identifier: Apache-2.0
Name:           perl-Logfile-Rotate
Version:        1.04
Release:        1%{?dist}
Summary:        Rotate private log files with callbacks and optional gzip compression
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Logfile-Rotate
Source0:        Logfile-Rotate-%{version}.tar.gz
Source1:        perl-5.8.7-README
Source2:        perl-5.8.7-Artistic
Source3:        perl-5.8.7-Copying

BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  gzip
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-Carp
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-IO-Compress
BuildRequires:  perl-Test-Harness
BuildRequires:  perl-generators
Requires:       coreutils
Requires:       gzip
Requires:       perl
Requires:       perl-Carp
Requires:       perl-File-Temp
Requires:       perl-IO-Compress
Requires:       util-linux

%description
Logfile::Rotate provides private-file rotation, retention, callbacks,
relocation, and library or external gzip compression. The official archive
and RPM version are 1.04; its unchanged module declares VERSION 1.05, which
the Perl automatic provider generator retains. Both are intentional facts.

%prep
%autosetup -n Logfile-Rotate-%{version} -p1
cp -p %{SOURCE1} %{SOURCE2} %{SOURCE3} .

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Unprivileged private files; retain all nine original tests/115 planned TAP assertions.
test "$(id -u)" -ne 0
id
test -x /usr/bin/gzip
rpm -qf /usr/bin/gzip
%{__perl} -MConfig -MCompress::Zlib -MTest::Harness -e 'print "Build identity realUID=$< effectiveUID=$> realGIDs=$( effectiveGIDs=$)\n"; die "missing Config gzip" unless defined $Config{gzip} && length $Config{gzip}; die "missing gzip executable" unless -x "/usr/bin/gzip";'
%make_build test
# Legacy tests print not-ok; Harness must propagate failure, never bare perl.
%{__perl} -Mblib -MTest::Harness -e 'my @t=sort glob "t/*.t"; die "incomplete default suite" unless @t==9; $Test::Harness::verbose=1; my($s,$failed,$todo)=Test::Harness::execute_tests(tests=>\@t); my $want={files=>9,tests=>9,good=>9,max=>115,ok=>115,bad=>0,skipped=>0,sub_skipped=>0,todo=>0,bonus=>0}; for my $key (sort keys %$want) { die "Harness $key mismatch" unless defined($s->{$key}) && $s->{$key}==$want->{$key}; } die "failed/TODO tests" if keys(%$failed) || keys(%$todo); print "Full default Harness gate Files=9 Tests=115 Skip=0 Failure=0\n";'

%files
%license README Logfile-Rotate.man.html Changes perl-5.8.7-README perl-5.8.7-Artistic perl-5.8.7-Copying
%{perl_vendorlib}/Logfile/Rotate.pm
%{_mandir}/man3/Logfile::Rotate.3*

%changelog
* Sun Oct 04 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.04-1
- Preserve official source/module-version distinction and complete default suite.
