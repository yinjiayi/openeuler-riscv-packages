# SPDX-License-Identifier: Apache-2.0
Name:           perl-Getopt-Long-Descriptive
Version:        0.117
Release:        1%{?dist}
Summary:        Describe and validate command-line options with generated usage
License:        Artistic-1.0-Perl AND Apache-2.0
URL:            https://metacpan.org/dist/Getopt-Long-Descriptive
Source0:        Getopt-Long-Descriptive-%{version}.tar.gz
Source1:        report-prereqs-0.029-LICENSE.txt
Source2:        report-prereqs-0.029-README.txt
Source3:        changes-0.011-LICENSE.txt
Source4:        changes-0.011-README.txt
Source5:        version-0.9909-README.txt
Source6:        historical-perl-Copying.txt
Source7:        historical-perl-Artistic.txt
Source8:        checkbreaks-0.020-LICENCE.txt
Source9:        checkbreaks-0.020-README.txt
Source10:        compile-2.059-LICENCE.txt
Source11:        compile-2.059-README.txt
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl >= 5.12.0
BuildRequires:  perl-generators
BuildRequires:  perl(Carp)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.78
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Getopt::Long) >= 2.55
BuildRequires:  perl(List::Util)
BuildRequires:  perl(Params::Validate) >= 0.97
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Sub::Exporter) >= 0.972
BuildRequires:  perl(Sub::Exporter::Util)
BuildRequires:  perl(overload)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
BuildRequires:  perl(CPAN::Meta) >= 2.120900
BuildRequires:  perl(CPAN::Meta::Check) >= 0.011
BuildRequires:  perl(CPAN::Meta::Requirements)
BuildRequires:  perl(Term::ANSIColor)
BuildRequires:  perl(Test::Fatal)
BuildRequires:  perl(Test::More) >= 0.96
BuildRequires:  perl(Test::Warnings) = 0.031
BuildRequires:  perl(Test::Harness) >= 3.48
Requires:       coreutils
Requires:       perl >= 5.12.0
Requires:       perl(Carp)
Requires:       perl(File::Basename)
Requires:       perl(Getopt::Long) >= 2.55
Requires:       perl(List::Util)
Requires:       perl(Params::Validate) >= 0.97
Requires:       perl(Scalar::Util)
Requires:       perl(Sub::Exporter) >= 0.972
Requires:       perl(Sub::Exporter::Util)
Requires:       perl(overload)
Requires:       perl(strict)
Requires:       perl(warnings)
Requires:       perl(Digest::SHA)

%description
Getopt::Long::Descriptive builds option objects and usage descriptions with
validation, required and negatable switches, shortcircuit and completion data.
Historical source supplements are full notice data, not built dependencies.

%prep
%autosetup -n Getopt-Long-Descriptive-%{version} -p1
mkdir packaging-notices
cp -p %{SOURCE1} packaging-notices/report-prereqs-0.029-LICENSE.txt
cp -p %{SOURCE2} packaging-notices/report-prereqs-0.029-README.txt
cp -p %{SOURCE3} packaging-notices/changes-0.011-LICENSE.txt
cp -p %{SOURCE4} packaging-notices/changes-0.011-README.txt
cp -p %{SOURCE5} packaging-notices/version-0.9909-README.txt
cp -p %{SOURCE6} packaging-notices/historical-perl-Copying.txt
cp -p %{SOURCE7} packaging-notices/historical-perl-Artistic.txt
cp -p %{SOURCE8} packaging-notices/checkbreaks-0.020-LICENCE.txt
cp -p %{SOURCE9} packaging-notices/checkbreaks-0.020-README.txt
cp -p %{SOURCE10} packaging-notices/compile-2.059-LICENCE.txt
cp -p %{SOURCE11} packaging-notices/compile-2.059-README.txt
cat > packaging-notices/PACKAGING-NOTICE.txt <<'NOTICE_EOF'
2026-10-06 downstream notice-reference addition, not upstream modification.
Source0 is unmodified complete Getopt-Long-Descriptive0.117 from the official RJBS
release. Core Hans Dieter Pearcey2005 / Ricardo Signes original grant and all
contributor notices remain intact. Distribution selects existing ten-clause
Perl Artistic1.0 branches, with separately retained Apache2 template scope;
all original GPL alternatives remain intact, no upstream file is relicensed.
t/00-report-prereqs.t is whole-byte identical to TestReportPrereqs0.029 DATA
after seven original configured literal substitutions. Full David Golden2012
Apache2 LICENSE/README preserve all seven contributor credits.
xt/release/changes_has_content.t is whole-byte identical to CheckChangesHasContent
0.011 DATA after four literal substitutions and the explicit DATA __END__ boundary.
Full David Golden2017 / Karen Etheridge Apache2 LICENSE/README retain credits.
t/zzz-check-breaks.t matches CheckBreaks0.020 whole template after five literal
substitutions and the template's terminal double-newline to single-newline
normalization; full Karen Etheridge2014 LICENCE/README retain Perl dual terms.
xt/author/00-compile.t matches TestCompile2.059 whole template after twelve literal
substitutions; full Jerome Quelin2009 LICENCE/README retain Perl dual terms.
Its original perlfaq8 credit remains untouched. Official versioned reference
https://perldoc.perl.org/5.38.0/perlfaq8 (AUTHOR AND COPYRIGHT and capture STDERR)
credits Benjamin Goldberg code samples and explicitly places code examples in
the public domain. This is bounded reference context, not proof of oldest FAQ
ancestor or a public-domain claim for the whole FAQ document.
The reporter's credited version::LAX grammar matches historical version0.9909
by literal normalization under /x, not full module identity or originally loaded
version. Full John Peacock2004-2010 README plus complete historical Perl
Copying/Artistic from d2c3426b4ccfd6a61af7f4e904f371945d63fdc8 retain terms/credits.
Eleven supplements are unmodified notice data, not executable generators or
historical modules. SPDX conjunction records reviewed scopes, not complete
oldest legal genealogy or legal certainty. No signature verification claim.
This newly authored packaging commentary only is repository Apache2.0 material.
NOTICE_EOF

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Real mandatory dependency loading/version validation, unlike reporter's pass.
timeout --kill-after=10s 30s %{__perl} <<'PREFLIGHT_EOF'
use strict;
use warnings;
die 'Perl minimum' if $] < 5.012;
my @requirements=(
 ['ExtUtils::MakeMaker','6.78'],['Carp',0],['File::Basename',0],
 ['Getopt::Long','2.55'],['List::Util',0],['Params::Validate','0.97'],
 ['Scalar::Util',0],['Sub::Exporter','0.972'],['Sub::Exporter::Util',0],
 ['overload',0],['strict',0],['warnings',0],['CPAN::Meta::Check','0.011'],
 ['CPAN::Meta::Requirements',0],['ExtUtils::MakeMaker',0],['File::Spec',0],
 ['Term::ANSIColor',0],['Test::Fatal',0],['Test::More','0.96'],['Test::Warnings','0.005']);
for my $r (@requirements) {
 my ($m,$min)=@$r; (my $file=$m)=~s{::}{/}g; require "$file.pm";
 $m->VERSION($min) if $min; print "required $m minimum=$min loaded
";
}
require CPAN::Meta; CPAN::Meta->VERSION('2.120900');
require Test::Harness; Test::Harness->VERSION('3.48');
die 'count source changed: Test::Warnings version' unless Test::Warnings->VERSION eq '0.031';
print "Mandatory original prerequisites loaded; strict counters bind Test::Warnings0.031
";
PREFLIGHT_EOF
printf '%s  %s\n' '5996417e8ae9973f82860dcf6d5f180d285d5c4b046e0346d06ed22802a3452b' 't/00-report-prereqs.t' | sha256sum -c -
printf '%s  %s\n' 'ea625a20e8d9826e727f8b221ce870dbd41e3410be92db1b4c97fb9f395cda26' 't/descriptive.t' | sha256sum -c -
printf '%s  %s\n' '98011eb5b7858891714681b2ba2dd9f460d8516c3f901ffd0ffd80726c61eaa9' 't/shortcircuit.t' | sha256sum -c -
printf '%s  %s\n' '3d97110ba93413cf16b6df74dfe38b861531203815cf177ee90d8458715eff62' 't/zzz-check-breaks.t' | sha256sum -c -
timeout --kill-after=10s 180s make test
# Execute every unchanged default again, with per-file summary and raw TAP proof.
timeout --kill-after=10s 180s %{__perl} -Mblib -MTest::Harness <<'HARNESS_EOF'
use strict;
use warnings;
my @tests=sort glob 't/*.t';
die 'default suite changed' unless join(' ',@tests) eq 't/00-report-prereqs.t t/descriptive.t t/shortcircuit.t t/zzz-check-breaks.t';
$Test::Harness::verbose=1;
my @counts=(1,66,11,2);
my $all_skips=0;
for my $i (0..$#tests) {
 my $t=$tests[$i]; my $want=$counts[$i]; my $path="strict-$i.log";
 open my $out,'>',$path or die $!;
 my ($s,$failed,$bonus)=Test::Harness::execute_tests(tests=>[$t],out=>$out);
 close $out or die $!; open my $in,'<',$path or die $!;
 my $raw=do {local $/; <$in>}; close $in or die $!; print "STRICT FILE $t\n$raw";
 my $expected={files=>1,tests=>1,good=>1,max=>$want,ok=>$want,bad=>0,skipped=>0,todo=>0,bonus=>0};
 for my $k (sort keys %$expected) {die "Harness $t $k" unless defined($s->{$k}) && $s->{$k}==$expected->{$k};}
 die "Harness failure $t" if keys(%$failed) || keys(%$bonus);
 die "bad TAP $t" if $raw =~ /^\s*(?:not ok\b|Bail out!)/m || $raw =~ /#[ \t]*TODO\b/i;
 my @plans=$raw =~ /^1\.\.(\d+)\r?$/mg;
 die "outer plan $t" unless @plans==1 && $plans[0]==$want;
 my @oks=$raw =~ /^(ok[ \t]+\d+(?:[ \t].*)?)\r?$/mg;
 die "outer count $t" unless @oks==$want;
 my $skips=0;
 for my $n (1..$want) {
  my $line=$oks[$n-1]; die "outer order $t" unless $line =~ /^ok[ \t]+$n(?:[ \t]|$)/;
  if ($line =~ /#[ \t]*SKIP\b/i) {
   die 'unexpected skip' unless $i==3 && $n==1 && $line =~ /#[ \t]*SKIP[ \t]+no Moose::Conflicts module found[ \t]*$/i;
   $skips++;
  }
 }
 die "skip count $t" unless defined($s->{sub_skipped}) && $s->{sub_skipped}==$skips && $skips<=1;
 if ($i==3) {
  eval {require Moose::Conflicts}; my $available=exists $INC{'Moose/Conflicts.pm'};
  die 'optional branch mismatch' unless $skips==($available?0:1);
  die 'remaining compatibility assertion absent' unless $oks[1] =~ /^ok 2 - checked x_breaks data$/;
 }
 if ($i==1) {
  my @names=('descriptions for option value types','completion skips non-option specs');
  my @nested=(18,2);
  for my $c (0..1) {
   my @blocks=$raw =~ /^# Subtest: \Q$names[$c]\E\r?\n(.*?)^ok \d+ - \Q$names[$c]\E\r?$/msg;
   die 'child missing' unless @blocks==1;
   my $child=$blocks[0]; my @plans=$child =~ /^    1\.\.(\d+)\r?$/mg;
   my @child_oks=$child =~ /^    ok[ \t]+(\d+)(?:[ \t].*)?\r?$/mg;
   die 'child plan/count' unless @plans==1 && $plans[0]==$nested[$c] && @child_oks==$nested[$c];
   for my $n (1..$nested[$c]) {die 'child order' unless $child_oks[$n-1]==$n;}
   die 'child directive' if $child =~ /#[ \t]*(?:SKIP|TODO)\b/i;
  }
  my @children=$raw =~ /^    ok[ \t]+\d+(?:[ \t].*)?\r?$/mg;
  die 'unexpected nested totals' unless @children==20;
 } else {die 'unexpected nested TAP' if $raw =~ /^    (?:ok\b|1\.\.)/m;}
 $all_skips+=$skips;
 print "Strict $t planned=$want ok=$want positive=",$want-$skips," optional_compat_skipped=$skips bad=0 todo=0 bonus=0\n";
}
die 'unexpected aggregate skip' if $all_skips>1;
print "Getopt original defaults: files=4 planned_outer=80 positive_outer=",80-$all_skips," optional_compat_skipped=$all_skips positive_nested=20 bad=0 todo=0 bonus=0\n";
HARNESS_EOF

%files
%license LICENSE README Changes
%license lib/Getopt/Long/Descriptive.pm lib/Getopt/Long/Descriptive/Opts.pm lib/Getopt/Long/Descriptive/Usage.pm
%license packaging-notices
%{perl_vendorlib}/Getopt/Long/Descriptive.pm
%{perl_vendorlib}/Getopt/Long/Descriptive/
%{_mandir}/man3/Getopt::Long::Descriptive*.3*

%changelog
* Tue Oct 06 2026 yinjiayi <yinjiayi@users.noreply.github.com> - 0.117-1
- Retain original complete source/default tests and scoped full notice supplements.
- Add mandatory loading/version guards and exact per-file/nested acceptance.
