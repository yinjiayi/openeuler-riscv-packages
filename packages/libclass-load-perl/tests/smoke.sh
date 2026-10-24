#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
export LC_ALL=C
if [ "$(id -u)" = 0 ]; then
  test "$#" = 0
  exec setpriv --reuid=10001 --regid=10001 --clear-groups bash "$0" --unprivileged-smoke
fi
if [ "$#" != 0 ]; then
  test "$#" = 1 && test "$1" = --unprivileged-smoke
fi
test "$(id -u)" = 10001
test "$(id -g)" = 10001
test "$(id -G)" = 10001
id
rpm -q perl-Class-Load
test "$(rpm -q --qf '%{VERSION}\n' perl-Class-Load)" = 0.25
provides="$(rpm -q --provides perl-Class-Load)"
printf '%s\n' "$provides" | grep -Fx 'perl(Class::Load) = 0.25'
printf '%s\n' "$provides" | grep -Fx 'perl(Class::Load::PP) = 0.25'
timeout --kill-after=10s 60s perl <<'SMOKE_PERL'
use strict;
use warnings;
use Class::Load ':all';
use Class::Load::PP ();
use Module::Implementation ();
use File::Temp qw(tempdir);
use Digest::SHA qw(sha256_hex);
die 'module versions' unless $Class::Load::VERSION eq '0.25' && $Class::Load::PP::VERSION eq '0.25';
my %hashes=(
 $INC{'Class/Load.pm'}=>'e6ea3a21d9e13b48a8d536f86a55c966796e0f56874389533983212b8b8831ee',
 $INC{'Class/Load/PP.pm'}=>'f2bd0284d7594120f008649f8c514faf867238f4db35c0e697e8e14cb543ab20',
 '/usr/share/licenses/perl-Class-Load/LICENSE'=>'dc030e63f20035291b90d09c2c40f296224e85878caf829ea981fc2f10910f9d',
 '/usr/share/licenses/perl-Class-Load/README'=>'32b6b6b7c1044b21e60cebe1eea253ffe2d22d0078cae4d41a9fadc49a593b96',
 '/usr/share/licenses/perl-Class-Load/Changes'=>'640caa893750f1f9d522d4e9b8472ced635455d4c8bbdf7fb9f633a97194f264',
 '/usr/share/licenses/perl-Class-Load/Load.pm'=>'e6ea3a21d9e13b48a8d536f86a55c966796e0f56874389533983212b8b8831ee',
 '/usr/share/licenses/perl-Class-Load/PP.pm'=>'f2bd0284d7594120f008649f8c514faf867238f4db35c0e697e8e14cb543ab20',
 '/usr/share/licenses/perl-Class-Load/packaging-notices/reporter-0.027-LICENSE.txt'=>'4c5f87ffa218ebe4027858643dad7133fcb8401f842cfaa4f425393fae1ddea2',
 '/usr/share/licenses/perl-Class-Load/packaging-notices/reporter-0.027-README.txt'=>'e6b0390fd69e5789cdabdd45f61905214d3627180555b9a29e641348a7136f1c',
 '/usr/share/licenses/perl-Class-Load/packaging-notices/bundle-0.141-LICENCE.txt'=>'ad98742459e575ff569f50a350a1a5ffde95cae88a897a5b12dd438960617434',
 '/usr/share/licenses/perl-Class-Load/packaging-notices/bundle-0.141-README.txt'=>'25a5abef01dfed2a3a5fd1c8fb5dadfca0bee9430dc4b9017f7761c18a7c8be0',
 '/usr/share/licenses/perl-Class-Load/packaging-notices/changes-0.011-LICENSE.txt'=>'b9edff2945afbd8a4482d6d09ed49fe64f65be61d355feeb7328ab53487cd5b4',
 '/usr/share/licenses/perl-Class-Load/packaging-notices/changes-0.011-README.txt'=>'f75ccf813c752850aa21aabff3dced2b53792b0657b387e0f47cb341629728ea',
 '/usr/share/licenses/perl-Class-Load/packaging-notices/version-0.9909-README.txt'=>'2281261147b4fc710bd1920d48e78aa44bc181306dba919ad98cb121a0c8ad21',
 '/usr/share/licenses/perl-Class-Load/packaging-notices/historical-perl-Copying.txt'=>'d77d235e41d54594865151f4751e835c5a82322b0e87ace266567c3391a4b912',
 '/usr/share/licenses/perl-Class-Load/packaging-notices/historical-perl-Artistic.txt'=>'8e6beb9ca0ffbc4b9c6550d56f622ecd33d5635ee8af9a8f269fd81f40fb6801',
 '/usr/share/licenses/perl-Class-Load/packaging-notices/class-mop-0.77-README.txt'=>'8d43b5cb3d29826651e08e2192b11fc999eb50c312429c6aa70efc29bfa6d397',
 '/usr/share/licenses/perl-Class-Load/packaging-notices/class-mop-0.77-original-module.txt'=>'4f2f9f6667f42bc6fac3917cbfb8edbb2976f3dfe0be383cfa1cfbd8f53eb20b',
 '/usr/share/licenses/perl-Class-Load/packaging-notices/class-mop-1.12-README.txt'=>'a6dfdd5208f6c652b768e714137bbc6e7fedd412b8476a5cd065d132e013720b',
 '/usr/share/licenses/perl-Class-Load/packaging-notices/class-mop-1.12-original-module.txt'=>'cb07b41fa8b5f72cecaad4c2edfed37ff0529f72c908d055b2c58002e3213a00',
 '/usr/share/licenses/perl-Class-Load/packaging-notices/compile-2.058-LICENCE.txt'=>'67523c952f52f6910dd844be488e93db8478fb55f595e782df629e370ecb598a',
 '/usr/share/licenses/perl-Class-Load/packaging-notices/compile-2.058-README.txt'=>'211faab7197b273477bcf9d17ffb1bb67e493c13937d9ce432c516fbed999c5e',
 '/usr/share/licenses/perl-Class-Load/packaging-notices/compile-2.058-module-notice.txt'=>'78b89f393740e4a74216d1be4971778c1daeb99ae9835632da6e9e3f7bd67acd',
 '/usr/share/licenses/perl-Class-Load/packaging-notices/ether-0.141-original-module.txt'=>'6fee29325a0c2e766357552b035d6b5beb849f44a5d672300fb53587166c60ad',
 '/usr/share/licenses/perl-Class-Load/packaging-notices/PACKAGING-NOTICE.txt'=>'2366b1fc9d70930976a8061a8d608168d30f6e10d24ae593e2b2f618838747dd',
);
for my $path (sort keys %hashes) {
 open my $fh,'<',$path or die "$path: $!"; binmode $fh; my $bytes=do {local $/; <$fh>}; close $fh or die $!;
 die "original module/full notice hash $path" unless sha256_hex($bytes) eq $hashes{$path};
 print "# Original module/notice hash OK $path\n";
}
print "1..6\nok 1 - installed exact module versions/capabilities/full notice bytes\n";
for my $k (qw(PERL5OPT PERL5LIB PERL5DB CLASS_LOAD_IMPLEMENTATION)) {
 die "unexpected loader override $k" if defined($ENV{$k}) && length($ENV{$k});
}
my $implementation=Module::Implementation::implementation_for('Class::Load');
die 'default backend missing' unless defined($implementation) && $implementation =~ /\A(?:PP|XS)\z/;
print "# Actual selected default implementation=$implementation (no XS/native coverage claim)\n";
my $dir=tempdir('class-load-smoke-XXXXXXXX',TMPDIR=>1,CLEANUP=>1);
chmod 0700,$dir or die $!;
die 'private fixture directory' unless -d $dir && (((stat($dir))[2] & 0777)==0700);
mkdir "$dir/ClassLoadPackaging" or die $!;
for my $r (['Available',q{package ClassLoadPackaging::Available; our $VERSION='1.2'; sub answer {42} 1;}],
           ['SyntaxError',q{package ClassLoadPackaging::SyntaxError; my $broken = ; 1;}]) {
 open my $fh,'>',"$dir/ClassLoadPackaging/$r->[0].pm" or die $!;
 print {$fh} $r->[1],"\n" or die $!; close $fh or die $!;
}
local @INC=($dir,@INC);
my $class='ClassLoadPackaging::Available'; my $missing='ClassLoadPackaging::DefinitelyAbsent';
die 'load_class return' unless load_class($class) eq $class && $class->answer==42;
die 'loaded/version predicates' unless is_class_loaded($class) && is_class_loaded($class,{-version=>'1.2'}) && !is_class_loaded($class,{-version=>'9.0'});
print "ok 2 - actual load_class and versioned class detection\n";
my ($ok,$error)=try_load_class($missing);
die 'try_load failure/error' if $ok || !defined($error) || $error !~ /Can't locate ClassLoadPackaging\/DefinitelyAbsent\.pm in \@INC/ || !defined($Class::Load::ERROR) || $Class::Load::ERROR ne $error;
die 'optional missing/low/available' if load_optional_class($missing) || load_optional_class($class,{-version=>'9.0'}) || !load_optional_class($class);
print "ok 3 - try_load_class error and optional missing/version semantics\n";
die 'first-existing missing fallback' unless load_first_existing_class($missing,$class) eq $class;
die 'first-existing version fallback' unless load_first_existing_class($class=>{-version=>'9.0'},$class=>{-version=>'1.2'}) eq $class;
print "ok 4 - actual ordered and versioned first-existing fallback\n";
eval {load_optional_class('Not a module name')}; die 'invalid module name accepted' unless $@;
eval {load_first_existing_class('ClassLoadPackaging::SyntaxError',$class)};
die 'syntax error incorrectly treated as absent' unless $@ =~ /Couldn't load class \(ClassLoadPackaging::SyntaxError\) because:/;
print "ok 5 - invalid-name and syntax-error negative loading semantics\n";
{package ClassLoadPackaging::InlineVersion; our $VERSION='2';}
{package ClassLoadPackaging::InlineMethod; sub answer {42}}
die 'PP inline version/method' unless Class::Load::PP::is_class_loaded('ClassLoadPackaging::InlineVersion') && Class::Load::PP::is_class_loaded('ClassLoadPackaging::InlineMethod') && !Class::Load::PP::is_class_loaded($missing);
print "ok 6 - bundled PP basic inline version/method detection\n";
SMOKE_PERL
