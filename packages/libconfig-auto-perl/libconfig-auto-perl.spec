# SPDX-License-Identifier: Apache-2.0
Name:           perl-Config-Auto
Version:        0.44
Release:        1%{?dist}
Summary:        Detect and parse configuration file formats in Perl
License:        (GPL-1.0-or-later OR Artistic-1.0-Perl) AND GPL-3.0-only
URL:            https://metacpan.org/dist/Config-Auto
Source0:        https://cpan.metacpan.org/authors/id/B/BI/BINGOS/Config-Auto-%{version}.tar.gz
Source1:        App-EUMM-Upgrade-0.21-NOTICE.txt
Source2:        GNU-GPL-3.txt
Source3:        Perl-Artistic.txt
Source4:        Perl-Copying.txt
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker) >= 7.70
BuildRequires:  perl(Getopt::Std)
BuildRequires:  perl(Carp)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(IO::String)
BuildRequires:  perl(Text::ParseWords)
BuildRequires:  perl(Config::IniFiles)
BuildRequires:  perl(YAML) >= 0.67
BuildRequires:  perl(YAML::Any) >= 0.67
BuildRequires:  perl(XML::Simple)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod) >= 1.14
BuildRequires:  perl(Test::Harness) = 3.48
BuildRequires:  make
BuildRequires:  coreutils
BuildRequires:  findutils
Requires:       perl
Requires:       perl(Carp)
Requires:       perl(File::Basename)
Requires:       perl(File::Spec::Functions)
Requires:       perl(File::Temp)
Requires:       perl(IO::String)
Requires:       perl(Text::ParseWords)
Requires:       perl(Config::IniFiles)
Requires:       perl(YAML) >= 0.67
Requires:       perl(YAML::Any) >= 0.67
Requires:       perl(XML::Simple)
Requires:       perl(Digest::SHA)
Requires:       util-linux
Requires:       coreutils
Requires:       bash
Requires:       grep

%description
Detect and parse colon, space, equal, XML, INI, list, YAML and Perl configuration
data. Preserve the original library dual same-Perl grant. The source aggregate
also accounts for the separately GPLv3 copied WriteMakefile1 build helper;
it does not relicense the complete runtime library GPLv3-only. The full original
origin notice and all applicable complete terms are preserved as license text.

%prep
%autosetup -n Config-Auto-%{version}
install -m 0644 %{SOURCE1} App-EUMM-Upgrade-0.21-NOTICE.txt
install -m 0644 %{SOURCE2} GNU-GPL-3.txt
install -m 0644 %{SOURCE3} Perl-Artistic.txt
install -m 0644 %{SOURCE4} Perl-Copying.txt
cat > .original-source.sha256 <<'ORIGINAL_SOURCE_SHA256'
c828f6b61f96e3d392ab4f365b19ce1cfe726bc1782476f2505fe5a4460c3deb  README
34b93d9e85d04c2df56e47ffb33888039015fa7314564d0ab0d2c34ebfc84dd2  Makefile.PL
dd360e3704ad09e2a1a3e8dc87c495673092b0c1ae999f442e38ebab8e5db4fd  Changes
9e37bfb2c6628f691d17d12a2e62883efd70353c14eebf3d72cb83be6fb2280e  MANIFEST
f355a17f3b771dea3ddbb606ba8ab1089d357310c5dd635d40287cf27e5dcebb  META.yml
fb4a6b87569e0063fc9e0485fc3dd5d12f30205887c646636d2d0498f2b5324e  META.json
da6267fed1e57d25835c2d68bc0d1d6853f1f62dbaa6cf926b5195b1f1620505  lib/Config/Auto.pm
625807d4ad0765acd3852350651af09a6e724669ff5d7b86b368afb0a2e7c6ac  t/06_const_it.t
b126ca5aa5a49ea821afa0968c2ca1497124e190f1feb7d98cc903b6e0eb6968  t/07_rt91891.t
c8c03d0c9afe594525eba98cb0c4e0577b9bdf25d9ee2f440c81da27d77f0802  t/02_parse.t
72621d88772cf9196d832ee289091744300cae36bc22d67974ccf3ae721e18cb  t/04_magic.t
b6d51e003f423b6837ad517b093737767dfb358ae1779904cedd88f3eadaf615  t/05_rt69984.t
6eb4b9b0cf6ffbd798f9bca74c991a19b6971b7931ae9e6b6afab57972a382aa  t/99_pod.t
7e7d4c9c8c9960131f36035ef1bd8257425f1dcd5e9c4dd2ea2d0fc3f1dc451d  t/00_load.t
b981520d8bc115c20505f5cd14938473c90efbff532917efc9aebfe5f1e42fb6  t/20_XML_unvailable.t
c0661cced32dacb6f617659c5da97871bae8ed57d297c5a551afe11863767095  t/fstab
b706695b484bf5afd40f9322354c58d23e65193dfeae4836c928c03348e0d149  t/01_OO.t
1868f89020d5dc73f652de8c17f4d48b6f05e18e8d8e3e2ce0fe8c9943ae3ad6  t/03_invalid.t
aca1806982537ecf684c00f58e17e15c7c17121e59df4d808de02812dde1d287  t/lib/XML/Simple.pm
0d099a91e693960d77ed48f75b23ed97dd8787dd3bab3c01c217e9b42ebed258  t/src/05_rt69984.conf
eb400188f4b35f8749b8c30d4ae4ed9bbf5c6b5b83499f418ce3936755d7eb5d  t/src/07_rt91891.conf
e621bcce928241db8b0609ac56504cd1e81a1d7d9625d6c00eca21d2de76295d  t/src/04_magic.config
d08188138c0c49b7a28c573a3d912d42cc7175ebbd9ccc7c090f08ee9ffe7b7b  App-EUMM-Upgrade-0.21-NOTICE.txt
3972dc9744f6499f0f9b2dbf76696f2ae7ad8af9b23dde66d6af86c9dfb36986  GNU-GPL-3.txt
dd90d4f42e4dcadf5a7c09eea0189d93c7b37ae560c91f0f6d5233ed3b9292a2  Perl-Artistic.txt
d77d235e41d54594865151f4751e835c5a82322b0e87ace266567c3391a4b912  Perl-Copying.txt
ORIGINAL_SOURCE_SHA256
sha256sum -c .original-source.sha256

%build
sha256sum -c .original-source.sha256
if [ -n "${PERL5OPT-}" ] || [ -n "${PERL5LIB-}" ] || [ -n "${PERLLIB-}" ] || \
   [ -n "${HARNESS_PERL-}" ] || [ -n "${HARNESS_PERL_SWITCHES-}" ] || \
   [ -n "${HARNESS_OPTIONS-}" ] || [ -n "${HARNESS_SUBCLASS-}" ] || \
   [ -n "${HARNESS_IGNORE_EXIT-}" ]; then
    echo 'Refusing Perl/Harness environment overrides before upstream execution' >&2
    exit 1
fi
test "$(id -u)" = 10001
test "$(id -g)" = 10001
# Upstream may search HOME or /etc; use a private HOME without changing original code.
install -d -m 0700 .config-auto-home
export HOME="$PWD/.config-auto-home"
perl Makefile.PL -x INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f \( -name .packlist -o -name '*.bs' -o -name perllocal.pod \) -delete

%check
sha256sum -c .original-source.sha256
if [ -n "${PERL5OPT-}" ] || [ -n "${PERL5LIB-}" ] || [ -n "${PERLLIB-}" ] || \
   [ -n "${HARNESS_PERL-}" ] || [ -n "${HARNESS_PERL_SWITCHES-}" ] || \
   [ -n "${HARNESS_OPTIONS-}" ] || [ -n "${HARNESS_SUBCLASS-}" ] || \
   [ -n "${HARNESS_IGNORE_EXIT-}" ]; then
    echo 'Refusing Perl/Harness environment overrides before checks' >&2
    exit 1
fi
test "$(id -u)" = 10001
test "$(id -g)" = 10001
export HOME="$PWD/.config-auto-home"
test -d "$HOME"
test "$(stat -c %%a "$HOME")" = 700
test "$(stat -c %%u "$HOME")" = 10001
test -f t/fstab
test -f t/lib/XML/Simple.pm
perl -Iblib/lib -Iblib/arch -MXML::Simple -MYAML -MYAML::Any -MConfig::IniFiles -MTest::Pod -MTest::Harness -MConfig::Auto -e '
  die "unexpected Harness interface" unless $Test::Harness::VERSION eq "3.48";
  YAML->VERSION(0.67); YAML::Any->VERSION(0.67); Test::Pod->VERSION(1.14);
  die "negative XML fixture used as positive supplier" if $INC{"XML/Simple.pm"} =~ m{(?:^|/)t/lib/};
  die "unsafe build identity" unless $< == 10001 && $> == 10001;
  print "PRECHECK UID=$< XML=$XML::Simple::VERSION YAML=$YAML::VERSION POD=$Test::Pod::VERSION\n";
'
# The entire default MakeMaker selector remains untouched, including dynamic POD.
timeout --kill-after=10s 240s make test
timeout --kill-after=10s 240s perl -Iblib/lib -Iblib/arch -MTest::Harness -e '
  die "unexpected Harness interface" unless $Test::Harness::VERSION eq "3.48";
  my @tests = sort glob("t/*.t");
  die "default suite changed" unless join(" ", @tests) eq "t/00_load.t t/01_OO.t t/02_parse.t t/03_invalid.t t/04_magic.t t/05_rt69984.t t/06_const_it.t t/07_rt91891.t t/20_XML_unvailable.t t/99_pod.t";
  $Test::Harness::Verbose = 1;
  my ($total, $failed, $todo_passed) = Test::Harness::execute_tests(tests => \@tests);
  die "missing statistics maps" unless ref($total) eq "HASH" && ref($failed) eq "HASH" && ref($todo_passed) eq "HASH";
  my %want = (files=>10, tests=>10, good=>10, bad=>0, skipped=>0, sub_skipped=>0, todo=>0, bonus=>0);
  for my $key (sort keys %want) {
    die "invalid statistic $key" unless exists($total->{$key}) && defined($total->{$key}) && !ref($total->{$key}) && $total->{$key} =~ /\A[0-9]+\z/ && $total->{$key} == $want{$key};
    print "STRICT $key=$total->{$key}\n";
  }
  for my $key (qw(max ok)) {
    die "invalid assertion count" unless exists($total->{$key}) && defined($total->{$key}) && !ref($total->{$key}) && $total->{$key} =~ /\A[0-9]+\z/;
    print "STRICT $key=$total->{$key}\n";
  }
  die "lost functional or dynamic POD coverage" unless $total->{max} >= 379 && $total->{ok} == $total->{max};
  die "failed test files" if keys %$failed;
  die "unexpected TODO successes" if keys %$todo_passed;
  print "Config::Auto original10files / nine-functional378static plus dynamicPOD / zero failures-skips-TODO-bonus PASS\n";
'
sha256sum -c .original-source.sha256

%files
%license README Changes MANIFEST META.json META.yml lib/Config/Auto.pm Makefile.PL
%license App-EUMM-Upgrade-0.21-NOTICE.txt GNU-GPL-3.txt Perl-Artistic.txt Perl-Copying.txt
%{perl_vendorlib}/Config/Auto.pm
%{_mandir}/man3/Config::Auto.3pm*

%changelog
* Thu Oct 08 2026 yinjiayi <yinjiayi@users.noreply.github.com> - 0.44-1
- Preserve the official source, complete default tests, scoped helper notice and full terms.
