# SPDX-License-Identifier: Apache-2.0
Name:           perl-IO-TieCombine
Version:        1.005
Release:        1%{?dist}
Summary:        Produce separate tied output variables with combined output
License:        Artistic-1.0 AND Artistic-1.0-Perl AND Apache-2.0
URL:            https://metacpan.org/dist/IO-TieCombine
Source0:        IO-TieCombine-%{version}.tar.gz
Source1:        changes-LICENSE.txt
Source2:        changes-README.txt
Source3:        jerome-LICENSE.txt
Source4:        jerome-README.txt
Source5:        reporter-LICENSE.txt
Source6:        reporter-README.txt
Source7:        version-Artistic.txt
Source8:        version-Copying.txt
Source9:        version-README.txt
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl >= 5.18.0
BuildRequires:  perl-Carp
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-PathTools
BuildRequires:  perl-Test-Harness
BuildRequires:  perl-Test-Simple >= 0.96
BuildRequires:  perl-generators
Requires:       coreutils
Requires:       perl >= 5.18.0
Requires:       perl-Carp
Requires:       perl-Digest-SHA

%description
IO::TieCombine accumulates separate tied scalar/filehandle output slots
and combined output in write order.
Historical source supplements are original notice texts, not built dependencies.

%prep
%autosetup -n IO-TieCombine-%{version} -p1
# Separate packaging-added notice data; no original source/test member is edited.
mkdir packaging-notices
cp -p %{SOURCE1} packaging-notices/changes-LICENSE.txt
cp -p %{SOURCE2} packaging-notices/changes-README.txt
cp -p %{SOURCE3} packaging-notices/jerome-LICENSE.txt
cp -p %{SOURCE4} packaging-notices/jerome-README.txt
cp -p %{SOURCE5} packaging-notices/reporter-LICENSE.txt
cp -p %{SOURCE6} packaging-notices/reporter-README.txt
cp -p %{SOURCE7} packaging-notices/version-Artistic.txt
cp -p %{SOURCE8} packaging-notices/version-Copying.txt
cp -p %{SOURCE9} packaging-notices/version-README.txt
cat > packaging-notices/PACKAGING-NOTICE.txt <<'NOTICE_EOF'
2026-10-06 downstream packaging notice-reference addition, not upstream modification.
Original IO1.005 Source0 and every original code/default/extra file remain unchanged.
Core Ricardo SIGNES2015 samePerl dual grant: this distribution selects its generic
nine-clause Artistic1.0 branch; the original GPL alternative remains untouched.
xt/release/changes_has_content.t is whole-byte identical to the CheckChangesHasContent
0.008 DATA template after the original upstream three configured literal substitutions.
Full David Golden2015/Karen Etheridge Apache2 terms/credits accompany that copied test.
t/00-report-prereqs.t is whole-byte identical to TestReportPrereqs0.021 DATA after
the original upstream five configured literal substitutions; full David Golden2012
Apache2 terms and all five contributor credits accompany that unchanged test.
The reporter credited version::LAX grammar matches historical version0.9909 by literal
grammar expansion under /x, not full module identity or the original loaded version.
Full John Peacock2004-2010 version README and exact historical Perl Copying/Artistic
retain terms/credits; selected LAX branch is ten-clause Artistic1.0-Perl.
The explicit Jerome Quelin copied/adapted credit remains in the original release test.
Git2.036 full Jerome2009 dual grant/README supplement supplies family notice context;
its parser differs, so it is not asserted as the exact oldest copied ancestor.
The nine supplemental texts are unmodified official data, not installed generator,
Git or historical version executables. SPDX conjunction is scoped accounting, not
relicensing original files or a legal certainty claim. No source signature is verified.
This newly authored commentary only is repository Apache2.0 packaging material.
NOTICE_EOF


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
%{__perl} -MExtUtils::MakeMaker -MTest::More -MTest::Harness -MFile::Spec -MCarp -MSymbol -e 'die "target Perl too old" if $] < 5.018; Test::More->VERSION(0.96);'
timeout --kill-after=10s 180s make test
# Preserve all original default files. The target enters the original say branch.
timeout --kill-after=10s 180s %{__perl} -Mblib -MTest::Harness <<'HARNESS_EOF'
use strict;
use warnings;
my @t=sort glob 't/*.t';
die "incomplete default suite" unless join(' ',@t) eq 't/00-report-prereqs.t t/basic.t';
$Test::Harness::verbose=1;
open my $tap,'>','default-harness.log' or die $!;
my ($s,$failed)=Test::Harness::execute_tests(tests=>\@t,out=>$tap);
close $tap or die $!;
open my $log,'<','default-harness.log' or die $!;
local $/; my $raw=<$log>; close $log or die $!; print $raw;
my $want={files=>2,tests=>2,good=>2,max=>7,ok=>7,bad=>0,skipped=>0,sub_skipped=>0,todo=>0,bonus=>0};
for my $k (sort keys %$want) {die "Harness $k mismatch" unless defined($s->{$k}) && $s->{$k}==$want->{$k};}
die 'failed tests' if keys(%$failed);
# The aggregate alone does not prove the unchanged say child actually ran.
my @child=$raw =~ /^# Subtest: the 'say' built-in\r?\n(.*?)^ok 6 - the 'say' built-in\r?$/msg;
die 'missing or duplicate say subtest' unless @child==1;
my @plans=$child[0] =~ /^    1\.\.1\r?$/mg;
my @passed=$child[0] =~ /^    ok 1 - say appends a newline\r?$/mg;
die 'nested say assertion/plan mismatch' unless @plans==1 && @passed==1;
die 'nested skip/TODO/failure/bailout' if $child[0] =~ /(?:^\s*not ok\b|\bBail out!|#\s*(?:SKIP|TODO)\b)/mi;
my @lines=grep {length && !/^\s*#/} split /\r?\n/,$child[0];
die 'unexpected nested TAP' unless @lines==2 && !grep {!/^    (?:1\.\.1|ok 1 - say appends a newline)$/} @lines;
print "Strict default gate Files=2 Outer=7 SayNested=1 Skip=0 TODO=0 Bonus=0 Failure=0\n";
HARNESS_EOF

%files
%license LICENSE README Changes packaging-notices
%{perl_vendorlib}/IO/TieCombine.pm
%{perl_vendorlib}/IO/TieCombine/
%{_mandir}/man3/IO::TieCombine.3*
%{_mandir}/man3/IO::TieCombine::Handle.3*
%{_mandir}/man3/IO::TieCombine::Scalar.3*

%changelog
* Tue Oct 06 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.005-1
- Package unchanged source/default/extra tests with separately scoped original notices.
