# SPDX-License-Identifier: Apache-2.0
Name:           perl-Class-Load
Version:        0.25
Release:        1%{?dist}
Summary:        Load Perl classes with optional loading and a pure-Perl fallback
License:        Artistic-1.0 AND Artistic-1.0-Perl AND Apache-2.0
URL:            https://metacpan.org/dist/Class-Load
Source0:        Class-Load-0.25.tar.gz
Source1:        reporter-0.027-LICENSE.txt
Source2:        reporter-0.027-README.txt
Source3:        bundle-0.141-LICENCE.txt
Source4:        bundle-0.141-README.txt
Source5:        changes-0.011-LICENSE.txt
Source6:        changes-0.011-README.txt
Source7:        version-0.9909-README.txt
Source8:        historical-perl-Copying.txt
Source9:        historical-perl-Artistic.txt
Source10:        class-mop-0.77-README.txt
Source11:        class-mop-0.77-original-module.txt
Source12:        class-mop-1.12-README.txt
Source13:        class-mop-1.12-original-module.txt
Source14:        compile-2.058-LICENCE.txt
Source15:        compile-2.058-README.txt
Source16:        compile-2.058-module-notice.txt
Source17:        ether-0.141-original-module.txt
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl >= 5.006
BuildRequires:  perl-generators
BuildRequires:  perl(CPAN::Meta) >= 2.120900
BuildRequires:  perl(Carp)
BuildRequires:  perl(Data::OptList) >= 0.110
BuildRequires:  perl(Digest::SHA)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Module::Implementation) >= 0.04
BuildRequires:  perl(Module::Runtime) >= 0.012
BuildRequires:  perl(Package::Stash) >= 0.14
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Test::Fatal)
BuildRequires:  perl(Test::Harness) = 3.48
BuildRequires:  perl(Test::More) >= 0.88
BuildRequires:  perl(Test::Needs)
BuildRequires:  perl(Test::Without::Module)
BuildRequires:  perl(Try::Tiny)
BuildRequires:  perl(base)
BuildRequires:  perl(constant)
BuildRequires:  perl(lib)
BuildRequires:  perl(strict)
BuildRequires:  perl(version)
BuildRequires:  perl(warnings)
Requires:       coreutils
Requires:       util-linux
Requires:       perl >= 5.006
Requires:       perl(Carp)
Requires:       perl(Data::OptList) >= 0.110
Requires:       perl(Exporter)
Requires:       perl(Module::Implementation) >= 0.04
Requires:       perl(Module::Runtime) >= 0.012
Requires:       perl(Package::Stash) >= 0.14
Requires:       perl(Scalar::Util)
Requires:       perl(Try::Tiny)
Requires:       perl(base)
Requires:       perl(strict)
Requires:       perl(warnings)
Requires:       perl(Digest::SHA)
Requires:       perl(File::Temp)

%description
Class::Load provides class loading, optional loading, version checks and a
pure-Perl fallback. Historical full notice supplements are inert text data.

%prep
%autosetup -n Class-Load-%{version} -p1
sha256sum -c - <<'ORIGINAL_SHA_EOF'
640caa893750f1f9d522d4e9b8472ced635455d4c8bbdf7fb9f633a97194f264  Changes
4d89b14d4b723b416c306a718ec38f7f5731634e032798894503a5cbc36dbb74  CONTRIBUTING
2ae4c4c536901a157b28c8b3319c12a8cc5f8ac3261f2a70b8d785fdd3193731  dist.ini
6de19d7b756df2d6c5912e8f2fa7ca79f169c70e007e1f6b8cfd5122fd73ed28  INSTALL
dc030e63f20035291b90d09c2c40f296224e85878caf829ea981fc2f10910f9d  LICENSE
7ab24e4797aa3c431f747d52f4518725a90df19175f425c63b2d75b1fa53ae9c  Makefile.PL
4c59263cca038768e3859418de2ff97499d370143508879c1d89096b230077b9  MANIFEST
6c0a5f4aae8707a10df0367728754ab479373893078abe805d61b2548f6679d2  META.json
ebf43baba6254e94083b717ef6bb42dfe9f2f008a69b18f0ea68dbd1262ee9f1  META.yml
32b6b6b7c1044b21e60cebe1eea253ffe2d22d0078cae4d41a9fadc49a593b96  README
3553c9b8eb81e3322f9a692685349931ab8d1535267e84d31f06e1c969b3931f  xt/release/changes_has_content.t
f01b1c021d2a667978e559521daf1fa74723886bd94febabb8f3d3bfffb41e52  xt/release/cpan-changes.t
2e9b021ebd8bc92130968364df790af1e366ad49da0f03dd6eac19d95e09a549  xt/release/distmeta.t
982cfdcae889e38a9f628115a338ce36552a01af7a5e2225f62fafbd49149885  xt/author/00-compile.t
d3d8ceb7e8e1cab85aec31f7cdf352fe8fd9eb5fd51bac5a8c0a45c84fd60824  xt/author/changes_has_content.t
b40d526f11adcb3c0030c2da9623b87a00ae3f380bfbfe93bf20c38313201e1f  xt/author/eol.t
d37a5da6ee4b9d268fb9e1ade2bc1ba3668a74878e5f467027bb25377d354589  xt/author/kwalitee.t
bbadc8cd707f4111b77ddc57b14dde3a3f59648c728b8af801742cd1fb14a220  xt/author/minimum-version.t
89f6335b90cbedf340afef47053adab386d8b38faded020e58c76beda202e14f  xt/author/mojibake.t
748a190a93181610be491513639d124838768de61e35a761a0034ae9909936e4  xt/author/no-tabs.t
69a3db1acf181de7537fc0e01aaa497a864b234d389780f9b1b2f65fcffa936e  xt/author/pod-spell.t
01c189b60dbbc17780700c3d394ebe0930b9802329799f968dcce40436484111  xt/author/pod-syntax.t
419849c8760d9c5b43870f3b0bc3247ddf4b5284374e86fef6cbe58ceda61fb0  xt/author/portability.t
43979a26a85becfcfedbcb46b2e91ef5ca77a449526cd7f0ecdb3ff43279c01f  t/00-report-prereqs.dd
b7c5725c9f01e90cf73f45e8d0cf5ebfeb517409aa1a36c2bc094988cc904cf2  t/00-report-prereqs.t
78da1b4b0dafb9460598ca91902b7c73f17a3dc8ea37cc08fa2175f4204eb519  t/000-load.t
911c10d9d06395560e1d11b8864205d60d70c55e721ae402fec97dec9bb4b615  t/001-is-class-loaded.t
ddf07114a25548e13bba5c9727623b7f3a3e94ffe520b3691ddde7e649421da2  t/002-try-load-class.t
a25223c66802ecebc6b4265a9f3d300d1d7d991f101099ba8b91681a46670f05  t/003-load-class.t
b251e810bbfe813fdc47204c0830aa3b4728fcc59b3ae73cd89ecce15c07113c  t/004-load-double.t
d533aa4f585f376fd4ffeda33e61814a9de655ec761e128f25f05183cabb730a  t/005-load-optional.t
48c2f2ab8c7297cf19ed26daa98630fe9e93b9bbfeb23fb80fb696bec733479d  t/006-returned-error.t
b8dfcd72e596fbad6dff4ae65e9107c0d2ac6a4b75cb23663d452e7b7c19b08c  t/007-first-existing.t
a0faa57621fc96c2703b1f4e9ddbe6e87f32d2cde2ff419fc1068bfd3327ceb6  t/008-gvstash-bug.t
21387c026cdc4ba902fb9a851506a8af73e1bf3bdf68eadc2f70381b8df006bd  t/009-invalid-module-name.t
eefe4504def589e3dd326f86699f7c843dd51807298ccb7f6cc69d5504f9b2bd  t/010-isa-false-positive.t
aa60efd3a91a4c2de925ceedd48bd4234f5176c3851001db28c7504950dbd937  t/011-without-xs.t
1a71cde5a699bb6210c05ac1ed39b738e5f83260c00151c72639e3459b1165b8  t/012-without-implementation.t
2da7c4fcbd0dcef5ac24616193a395290d809eca70b2f83f93620053768a50d2  t/013-errors.t
fcd64db7cad7717c07c0506f74ad9ec1ccd4e2a6b901e5119823a7a9cee5c03e  t/014-weird-constants.t
c150aa499d9d666278bbed2f480b99637d4e63c081e5ee2caf3197f78f320f69  t/lib/Test/Class/Load.pm
ca4b6a96bea21edd02b1a20af6d4d025a2edcd523f6472bed31f3c5ec65e993b  t/lib/Class/Load/OK.pm
6ba2643af9976937eba274ce9f67417445e929f8d7e2cbc2eed373bc5406160d  t/lib/Class/Load/Stash.pm
789b56d2ab5c6d50d59ae3d406eb9bc1fbcc7a0b1d49977c14c1ae7d3b098994  t/lib/Class/Load/SyntaxError.pm
47d8169841a8ab416d45187ab20735c66ac0868165066587d2c23134c12bddcc  t/lib/Class/Load/VersionCheck.pm
8c09c19c21db99734133e68013c357200c41bfa6c1d3f10963274163d2d74529  t/lib/Class/Load/VersionCheck2.pm
8c06c439270df3c0cc2ad83a9d066de693c9752de7f5df84ba50aab9e901a2a9  t/lib/Class/Load/Stash/Sub.pm
927b397213450f339060dc30bd480f3e966be7e8655f96bed50bf3140eedad5b  t/lib/Class/Load/Error/DieAfterBeginIsa.pm
d5e348b1e491093cf78c8bdf0107734f430a9bf7d4b2312f48d25daed92f7da8  t/lib/Class/Load/Error/DieAfterIsa.pm
f92cef7f6c274b08311da103b7e7872d003d9b493c00e6fe971619c84c533343  t/lib/Class/Load/Error/SyntaxErrorAfterIsa.pm
e6ea3a21d9e13b48a8d536f86a55c966796e0f56874389533983212b8b8831ee  lib/Class/Load.pm
f2bd0284d7594120f008649f8c514faf867238f4db35c0e697e8e14cb543ab20  lib/Class/Load/PP.pm
ORIGINAL_SHA_EOF
mkdir packaging-notices
cp -p %{SOURCE1} packaging-notices/reporter-0.027-LICENSE.txt
cp -p %{SOURCE2} packaging-notices/reporter-0.027-README.txt
cp -p %{SOURCE3} packaging-notices/bundle-0.141-LICENCE.txt
cp -p %{SOURCE4} packaging-notices/bundle-0.141-README.txt
cp -p %{SOURCE5} packaging-notices/changes-0.011-LICENSE.txt
cp -p %{SOURCE6} packaging-notices/changes-0.011-README.txt
cp -p %{SOURCE7} packaging-notices/version-0.9909-README.txt
cp -p %{SOURCE8} packaging-notices/historical-perl-Copying.txt
cp -p %{SOURCE9} packaging-notices/historical-perl-Artistic.txt
cp -p %{SOURCE10} packaging-notices/class-mop-0.77-README.txt
cp -p %{SOURCE11} packaging-notices/class-mop-0.77-original-module.txt
cp -p %{SOURCE12} packaging-notices/class-mop-1.12-README.txt
cp -p %{SOURCE13} packaging-notices/class-mop-1.12-original-module.txt
cp -p %{SOURCE14} packaging-notices/compile-2.058-LICENCE.txt
cp -p %{SOURCE15} packaging-notices/compile-2.058-README.txt
cp -p %{SOURCE16} packaging-notices/compile-2.058-module-notice.txt
cp -p %{SOURCE17} packaging-notices/ether-0.141-original-module.txt
cat > packaging-notices/PACKAGING-NOTICE.txt <<'NOTICE_EOF'
2026-10-06 downstream notice-reference addition, not upstream modification.
Source0 is complete unmodified official ETHER Class-Load0.25; all52 original
files/16default/13extra tests, Shawn M Moore2008 grant and original contributors
remain intact. Original full LICENSE/README/Changes and both original modules
are retained separately as notices, not replaced or relicensed.
The distribution selects existing Artistic branches: core, ETHERBundle0.141
and TestCompile2.058 use generic nine-clause Artistic1; historical LAX/ClassMOP
notice scope uses Perl-specific ten-clause Artistic1; reporter and Changes
template scopes are Apache2. Original GPL alternatives remain untouched.
The conjunction Artistic-1.0 AND Artistic-1.0-Perl AND Apache-2.0 records these
reviewed scopes, not complete legal genealogy or blanket legal certainty.
t/00-report-prereqs.t matches whole TestReportPrereqs0.027 DATA after seven
configured literal substitutions, including actual metadata prerequisites;
David Golden2012 full Apache2 LICENSE/README and original contributors retained.
The credited version::LAX grammar matches historical version0.9909 by literal
/x-normalization, not originally loaded version or oldest copied ancestor.
Full John Peacock2004-2010 README and full historical Perl Copying/Artistic
from immutable d2c3426b4ccfd6a61af7f4e904f371945d63fdc8 retain terms/credits.
Release changes_has_content.t matches exact ChangesHasContent0.011 configured
DATA with four literal substitutions; David Golden2017/Karen Etheridge full
Apache2 LICENSE/README retained. No same-name license inference is used.
ETHERBundle0.141 share templates match complete CONTRIBUTING after eleven
literal blocks and complete author changes file directly. Renderer0.014 is
named in metadata but no renderer code bytes are copied in these files.
Full Karen Etheridge2013 LICENCE/README/whole module retains all six contributor
names/emails, including the original Cyrillic name, without translation.
ClassLoadPP's credited historical ClassMOP method is materially adapted:
ClassMOP0.77 is_class_loaded pure-Perl range contains the exact shared comments
and normalized scalar-reference condition; ClassMOP1.12's first-existing
loader supplies shared options/name/error-flow material, not whole-byte copy.
Complete two historical original modules and READMEs retain Infinity
Interactive2006-2008/2006-2010, Stevan Little and all original credits and
same-Perl grants. No claim of exact copy event or oldest ancestor is made.
ClassLoad xt author compile matches TestCompile2.058 whole DATA with original
configured substitutions; complete Jerome Quelin2009 LICENCE/README/module
retain Karen Etheridge and all contributors. The original perlfaq8 reference
remains; official versioned https://perldoc.perl.org/5.38.0/perlfaq8 explains
the same capture-STDERR code idiom and grants code examples public-domain use.
This is bounded reference context, not earliest FAQ identity or a public-domain
claim for the entire FAQ document. No extra author tests are claimed executed.
Seventeen full notice supplements are inert text data. Historical .pm bodies
are stored as .txt only in the license directory, not the Perl module path,
not generated capabilities, not new software/runtime dependencies.
Current publisher CHECKSUMS omits ETHERBundle0.141 and ClassMOP0.77; exact
authorized historical release API SHA and official fixed HTTPS archive bytes
are bound separately, not a false current publisher agreement/signature claim.
This newly authored packaging commentary alone is repository Apache2 material.
NOTICE_EOF

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
test "$(id -u)" = 10001
test "$(id -g)" = 10001
id
test "$(id -G)" = 10001
export TMPDIR="$(mktemp -d /tmp/class-load-check.XXXXXXXX)"
chmod 0700 "$TMPDIR"
trap 'rm -rf -- "$TMPDIR"' EXIT
# Reporter warnings then pass do not satisfy mandatory suppliers.
timeout --kill-after=10s 30s %{__perl} <<'PREFLIGHT_EOF'
use strict;
use warnings;
die 'Perl minimum' if $] < 5.006;
for my $k (qw(PERL5OPT PERL5LIB PERL5DB CLASS_LOAD_IMPLEMENTATION AUTHOR_TESTING RELEASE_TESTING HARNESS_OPTIONS HARNESS_PERL_SWITCHES HARNESS_PERL HARNESS_IGNORE_EXIT HARNESS_SUBCLASS HARNESS_SKIP_ALL_TESTS SKIP_TESTS NO_TESTS TEST_SKIP)) {
 die "unexpected test override: $k" if defined($ENV{$k}) && length($ENV{$k});
}
my @requirements=(
 ['CPAN::Meta','2.120900'],
 ['Carp','0'],
 ['Data::OptList','0.110'],
 ['Digest::SHA','0'],
 ['Exporter','0'],
 ['ExtUtils::MakeMaker','0'],
 ['File::Spec','0'],
 ['Module::Implementation','0.04'],
 ['Module::Runtime','0.012'],
 ['Package::Stash','0.14'],
 ['Scalar::Util','0'],
 ['Test::Fatal','0'],
 ['Test::Harness','3.48'],
 ['Test::More','0.88'],
 ['Test::Needs','0'],
 ['Test::Without::Module','0'],
 ['Try::Tiny','0'],
 ['base','0'],
 ['constant','0'],
 ['lib','0'],
 ['strict','0'],
 ['version','0'],
 ['warnings','0'],
);
for my $r (@requirements) {
 my ($m,$minimum)=@$r; (my $file=$m)=~s{::}{/}g; require "$file.pm";
 $m->VERSION($minimum) if $minimum;
 my $loaded_path=$INC{$file.'.pm'};
 print "required $m minimum=$minimum actual=",$m->VERSION," path=$loaded_path\n";
}
die 'strict Harness API changed' unless Test::Harness->VERSION eq '3.48';
PREFLIGHT_EOF
sha256sum -c - <<'DEFAULT_SHA_EOF'
43979a26a85becfcfedbcb46b2e91ef5ca77a449526cd7f0ecdb3ff43279c01f  t/00-report-prereqs.dd
b7c5725c9f01e90cf73f45e8d0cf5ebfeb517409aa1a36c2bc094988cc904cf2  t/00-report-prereqs.t
78da1b4b0dafb9460598ca91902b7c73f17a3dc8ea37cc08fa2175f4204eb519  t/000-load.t
911c10d9d06395560e1d11b8864205d60d70c55e721ae402fec97dec9bb4b615  t/001-is-class-loaded.t
ddf07114a25548e13bba5c9727623b7f3a3e94ffe520b3691ddde7e649421da2  t/002-try-load-class.t
a25223c66802ecebc6b4265a9f3d300d1d7d991f101099ba8b91681a46670f05  t/003-load-class.t
b251e810bbfe813fdc47204c0830aa3b4728fcc59b3ae73cd89ecce15c07113c  t/004-load-double.t
d533aa4f585f376fd4ffeda33e61814a9de655ec761e128f25f05183cabb730a  t/005-load-optional.t
48c2f2ab8c7297cf19ed26daa98630fe9e93b9bbfeb23fb80fb696bec733479d  t/006-returned-error.t
b8dfcd72e596fbad6dff4ae65e9107c0d2ac6a4b75cb23663d452e7b7c19b08c  t/007-first-existing.t
a0faa57621fc96c2703b1f4e9ddbe6e87f32d2cde2ff419fc1068bfd3327ceb6  t/008-gvstash-bug.t
21387c026cdc4ba902fb9a851506a8af73e1bf3bdf68eadc2f70381b8df006bd  t/009-invalid-module-name.t
eefe4504def589e3dd326f86699f7c843dd51807298ccb7f6cc69d5504f9b2bd  t/010-isa-false-positive.t
aa60efd3a91a4c2de925ceedd48bd4234f5176c3851001db28c7504950dbd937  t/011-without-xs.t
1a71cde5a699bb6210c05ac1ed39b738e5f83260c00151c72639e3459b1165b8  t/012-without-implementation.t
2da7c4fcbd0dcef5ac24616193a395290d809eca70b2f83f93620053768a50d2  t/013-errors.t
fcd64db7cad7717c07c0506f74ad9ec1ccd4e2a6b901e5119823a7a9cee5c03e  t/014-weird-constants.t
c150aa499d9d666278bbed2f480b99637d4e63c081e5ee2caf3197f78f320f69  t/lib/Test/Class/Load.pm
ca4b6a96bea21edd02b1a20af6d4d025a2edcd523f6472bed31f3c5ec65e993b  t/lib/Class/Load/OK.pm
6ba2643af9976937eba274ce9f67417445e929f8d7e2cbc2eed373bc5406160d  t/lib/Class/Load/Stash.pm
789b56d2ab5c6d50d59ae3d406eb9bc1fbcc7a0b1d49977c14c1ae7d3b098994  t/lib/Class/Load/SyntaxError.pm
47d8169841a8ab416d45187ab20735c66ac0868165066587d2c23134c12bddcc  t/lib/Class/Load/VersionCheck.pm
8c09c19c21db99734133e68013c357200c41bfa6c1d3f10963274163d2d74529  t/lib/Class/Load/VersionCheck2.pm
8c06c439270df3c0cc2ad83a9d066de693c9752de7f5df84ba50aab9e901a2a9  t/lib/Class/Load/Stash/Sub.pm
927b397213450f339060dc30bd480f3e966be7e8655f96bed50bf3140eedad5b  t/lib/Class/Load/Error/DieAfterBeginIsa.pm
d5e348b1e491093cf78c8bdf0107734f430a9bf7d4b2312f48d25daed92f7da8  t/lib/Class/Load/Error/DieAfterIsa.pm
f92cef7f6c274b08311da103b7e7872d003d9b493c00e6fe971619c84c533343  t/lib/Class/Load/Error/SyntaxErrorAfterIsa.pm
DEFAULT_SHA_EOF
timeout --kill-after=10s 180s make test
# Repeat the same full suite; bind actual raw TAP and all three legacy maps.
timeout --kill-after=10s 180s %{__perl} -Mblib -MTest::Harness <<'HARNESS_EOF'
use strict;
use warnings;
my @tests=sort glob 't/*.t';
die 'default suite filename changed' unless join(' ',@tests) eq 't/00-report-prereqs.t t/000-load.t t/001-is-class-loaded.t t/002-try-load-class.t t/003-load-class.t t/004-load-double.t t/005-load-optional.t t/006-returned-error.t t/007-first-existing.t t/008-gvstash-bug.t t/009-invalid-module-name.t t/010-isa-false-positive.t t/011-without-xs.t t/012-without-implementation.t t/013-errors.t t/014-weird-constants.t';
$Test::Harness::verbose=1;
my $todo_file='t/010-isa-false-positive.t';
my $reason=q{I'm not sure this is fixable as it's really an interpreter issue.};
my ($planned_total,$positive_total,$todo_negative_total,$todo_bonus_total)=(0,0,0,0);
for my $i (0..$#tests) {
 my $t=$tests[$i]; my $path="strict-$i.log";
 open my $out,'>',$path or die $!;
 my ($s,$failed,$bonus)=Test::Harness::execute_tests(tests=>[$t],out=>$out);
 close $out or die $!;
 open my $in,'<',$path or die $!; my $raw=do {local $/; <$in>}; close $in or die $!;
 print "STRICT FILE $t\n$raw";
 my $payload=$raw;
 die 'missing exact final Console success wrapper' unless $payload =~ s/\nok\n\z/\n/;
 die "summary maps $t" unless ref($s) eq 'HASH' && ref($failed) eq 'HASH' && ref($bonus) eq 'HASH';
 die "failed test process $t" if keys %$failed;
 die "bailout $t" if $payload =~ /^\s*Bail out!/mi;
 die "nested TAP not original $t" if $payload =~ /^\s+(?:(?:not )?ok\b|1\.\.)/m;
 my @plans=$payload =~ /^1\.\.(\d+)\r?$/mg;
 my @plan_lines=$payload =~ /^1\.\..*$/mg;
 die "positive exact plan $t" unless @plans==1 && @plan_lines==1 && $plans[0]>0;
 my $want=$plans[0];
 my @lines=$payload =~ /^((?:not )?ok[ \t]+\d+(?:[ \t].*)?)\r?$/mg;
 my @test_lines=$payload =~ /^(?:not )?ok\b.*$/mg;
 die "ordered count $t" unless @lines==$want && @test_lines==$want;
 die 't010 original plan' if $t eq $todo_file && $want!=6;
 my (@negative_todo,@positive_todo); my $positive=0;
 for my $n (1..$want) {
  my $line=$lines[$n-1];
  die "number/order $t" unless $line =~ /^(?:not )?ok[ \t]+$n(?:[ \t]|$)/;
  die "unexpected skip $t" if $line =~ /#[ \t]*SKIP\b/i;
  my $is_positive=($line =~ /^ok\b/);
  if ($t eq $todo_file && ($n==2 || $n==4)) {
   die 'original TODO reason changed' unless $line =~ /#[ \t]*TODO[ \t]+\Q$reason\E[ \t]*\r?$/;
   push @{ $is_positive ? \@positive_todo : \@negative_todo },$n;
  } else {
   die "unexpected TODO or failed assertion $t/$n" if !$is_positive || $line =~ /#[ \t]*TODO\b/i;
   $positive++;
  }
 }
 my $todo=($t eq $todo_file?2:0); my $bonus_count=scalar @positive_todo;
 my %expected=(files=>1,tests=>1,good=>1,bad=>0,max=>$want,ok=>$want,skipped=>0,sub_skipped=>0,todo=>$todo,bonus=>$bonus_count);
 for my $k (sort keys %expected) {die "Harness $t $k" unless defined($s->{$k}) && !ref($s->{$k}) && $s->{$k}=~/\A[0-9]+\z/ && $s->{$k}==$expected{$k};}
 if ($bonus_count) {
  die 'unexpected TODO-pass files' unless join(' ',sort keys %$bonus) eq $t;
  my $b=$bonus->{$t}; die 'TODO-pass record type' unless ref($b) eq 'HASH';
  die 'TODO-pass fields' unless join(' ',sort keys %$b) eq 'canon estat failed max name wstat';
  die 'TODO-pass undefined/reference fields' if grep { !defined($b->{$_}) || ref($b->{$_}) } qw(canon estat failed max name wstat);
  die 'TODO-pass numeric counters' if grep { $b->{$_} !~ /\A[0-9]+\z/ } qw(failed max);
  die 'TODO-pass success statuses' if grep { $b->{$_} ne '' && $b->{$_} ne '0' } qw(estat wstat);
  die 'TODO-pass canon' unless $b->{canon} eq join(' ',@positive_todo);
  die 'TODO-pass counts/name/status' unless $b->{failed}==$bonus_count && $b->{max}==2 && $b->{name} eq $t && !$b->{estat} && !$b->{wstat};
 } else {die 'unexpected TODO-pass record' if keys %$bonus;}
 $planned_total+=$want; $positive_total+=$positive; $todo_negative_total+=scalar @negative_todo; $todo_bonus_total+=$bonus_count;
 print "Strict $t planned=$want logical_ok=$want positive_nonTODO=$positive TODO_negative=",join(',',@negative_todo)," TODO_bonus=",join(',',@positive_todo)," bad=0 skipped=0\n";
}
die 'original TODO accounting' unless $todo_negative_total+$todo_bonus_total==2;
print "ClassLoad original defaults: files=16 actual_planned=$planned_total logical_ok=$planned_total positive_nonTODO=$positive_total TODO_negative=$todo_negative_total TODO_unexpected_positive=$todo_bonus_total bad=0 skipped=0\n";
HARNESS_EOF

%files
%license LICENSE README Changes
%license lib/Class/Load.pm lib/Class/Load/PP.pm
%license packaging-notices
%{perl_vendorlib}/Class/Load.pm
%{perl_vendorlib}/Class/Load/
%{_mandir}/man3/Class::Load*.3*

%changelog
* Tue Oct 06 2026 yinjiayi <yinjiayi@users.noreply.github.com> - 0.25-1
- Retain whole official source, original defaults and bounded historical full notices.
- Add mandatory supplier guards and exact per-file original TODO/raw-TAP accounting.
