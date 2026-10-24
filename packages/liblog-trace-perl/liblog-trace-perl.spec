# SPDX-License-Identifier: Apache-2.0
# Runtime sprintf turns Revision 1.70 into 1.070. Avoid a lexical-version
# ambiguity for this capability only; actual target generator proof awaits CI.
%global __provides_exclude ^perl[(]Log::Trace[)]([[:space:]]|$)
Name:           perl-Log-Trace
Version:        1.070
Release:        1%{?dist}
Summary:        Unified Perl tracing with buffers, callbacks and dump backends
License:        GPL-2.0-only
URL:            https://metacpan.org/dist/Log-Trace
Source0:        Log-Trace-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-Carp
BuildRequires:  perl-Data-Dumper
BuildRequires:  perl-Data-Serializer
BuildRequires:  perl(Data::Serializer::Data::Dumper)
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl(Fcntl)
BuildRequires:  perl-PathTools
BuildRequires:  perl-Sys-Syslog
BuildRequires:  perl-Test-Harness
BuildRequires:  perl-Test-Pod >= 1.00
BuildRequires:  perl-Test-Pod-Coverage >= 1.00
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-Time-HiRes
BuildRequires:  perl-generators
Requires:       coreutils
Requires:       perl
Requires:       perl-Carp
Requires:       perl-Data-Dumper
Requires:       perl-Data-Serializer
Requires:       perl(Data::Serializer::Data::Dumper)
Requires:       perl(Fcntl)
Requires:       perl-Sys-Syslog
Requires:       perl-Time-HiRes
Provides:       perl(Log::Trace) = 1.070

%description
Log::Trace provides tracing targets, level selection, deep imports, callbacks
and data dumps. The original module, manual and complete default tests remain
unchanged. This proposal is dependency-held: the fixed official target does
not currently supply Data::Serializer or its Data::Dumper backend. Their
requirements must be satisfied normally before any build acceptance.

%prep
%autosetup -n Log-Trace-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Private owned TMPDIR isolates the unchanged upstream fixed file basename.
test "$(id -u)" -ne 0
umask 077
oe_trace_tmpdir=$(mktemp -d "$PWD/oe-log-trace-tests.XXXXXX")
trap 'rmdir "$oe_trace_tmpdir"' EXIT
export TMPDIR="$oe_trace_tmpdir"
test -w "$TMPDIR"
test "$(stat -c '%a' "$TMPDIR")" = 700
test "$(stat -c '%u' "$TMPDIR")" = "$(id -u)"
%{__perl} -MCarp -MFcntl -MTime::HiRes -MData::Dumper -MData::Serializer -MData::Serializer::Data::Dumper -MSys::Syslog -MFile::Basename -MFile::Spec -MTest::More -MTest::Harness -MTest::Pod -MTest::Pod::Coverage -e 'Test::Pod->VERSION("1.00"); Test::Pod::Coverage->VERSION("1.00"); print "All default-test helpers and Serializer backend available; no skip fallback\n";'
%make_build test
# Eleven trace suites plan 80 assertions; two POD suites enumerate dynamically.
# Require all thirteen files and every observed assertion, not invented POD totals.
%{__perl} -Mblib -MTest::Harness -e 'my @t=sort glob "t/*.t"; die "incomplete default suite" unless @t==13; $Test::Harness::verbose=1; my($s,$failed,$todo)=Test::Harness::execute_tests(tests=>\@t); for my $key (qw(files tests good)) { die "Harness $key mismatch" unless defined($s->{$key}) && $s->{$key}==13; } for my $key (qw(bad skipped sub_skipped todo bonus)) { die "Harness $key nonzero" unless defined($s->{$key}) && $s->{$key}==0; } die "incomplete assertions" unless defined($s->{max}) && defined($s->{ok}) && $s->{max}>80 && $s->{ok}==$s->{max}; die "failed/TODO tests" if keys(%$failed) || keys(%$todo); print "Full default Harness gate Files=13 Tests=$s->{max} Skip=0 Failure=0 TODO=0 Bonus=0\n";'

%files
%license COPYING README lib/Log/Trace.pm lib/Log/Trace/Manual.pod Changes
%{perl_vendorlib}/Log/Trace.pm
%{perl_vendorlib}/Log/Trace/
%{_mandir}/man3/Log::Trace.3*
%{_mandir}/man3/Log::Trace::Manual.3*

%changelog
* Sun Oct 04 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.070-1
- Prepare unchanged official source, full tests and explicit Serializer hold.
