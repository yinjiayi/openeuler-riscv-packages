# SPDX-License-Identifier: Apache-2.0
Name:           perl-Cwd-Guard
Version:        0.05
Release:        1%{?dist}
Summary:        Temporarily change directory with scope-based restoration
License:        Artistic-1.0
URL:            https://metacpan.org/dist/Cwd-Guard
Source0:        https://cpan.metacpan.org/authors/id/K/KA/KAZEBURO/Cwd-Guard-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl >= 5.8.1
BuildRequires:  perl-generators
BuildRequires:  perl(Module::Build) >= 0.38
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Requires)
BuildRequires:  perl(File::Spec::Link) >= 0.080
BuildRequires:  perl(Test::Harness) = 3.48
BuildRequires:  coreutils
BuildRequires:  findutils
Requires:       perl >= 5.8.1
Requires:       perl(Cwd)
Requires:       perl(File::Temp)
Requires:       perl(Digest::SHA)
Requires:       util-linux
Requires:       coreutils
Requires:       bash
Requires:       grep

%description
Temporarily change the working directory and restore it when the returned guard
is destroyed. The original file-descriptor restoration and failure semantics
are preserved. This distribution selects the original generic Artistic License
alternative without rewriting upstream grants or excluding its GPL alternative.

%prep
%autosetup -n Cwd-Guard-%{version}

%build
perl Build.PL --installdirs vendor
./Build

%install
./Build install --destdir %{buildroot}
find %{buildroot} -type f \( -name .packlist -o -name '*.bs' \) -delete

%check
if [ -n "${PERL5OPT-}" ] || [ -n "${PERL5LIB-}" ] || [ -n "${PERLLIB-}" ] || \
   [ -n "${HARNESS_PERL-}" ] || [ -n "${HARNESS_PERL_SWITCHES-}" ] || \
   [ -n "${HARNESS_OPTIONS-}" ] || [ -n "${HARNESS_SUBCLASS-}" ] || \
   [ -n "${HARNESS_IGNORE_EXIT-}" ]; then
    echo 'Refusing Perl/Harness environment overrides before imports or tests' >&2
    exit 1
fi
test "$(id -u)" = 10001
test "$(id -g)" = 10001
perl -Iblib/lib -Iblib/arch -MModule::Build -MTest::More -MTest::Requires -MTest::Harness -MFile::Spec::Link -MCwd::Guard -e '
  Module::Build->VERSION(0.38);
  File::Spec::Link->VERSION(0.080);
  die "unexpected Harness interface" unless $Test::Harness::VERSION eq "3.48";
  die "original fchdir feature unavailable: full renamed default test required" unless Cwd::Guard::USE_FCHDIR;
  die "unsafe build identity" unless $< == 10001 && $> == 10001;
  print "BUILD UID=$< EUID=$> GID=$( EGID=$)\n";
  print "PRECHECK File::Spec::Link=$File::Spec::Link::VERSION USE_FCHDIR=1\n";
'
# Preserve the entire original Module::Build default suite before a strict repeat.
timeout --kill-after=10s 180s ./Build test
timeout --kill-after=10s 180s perl -Iblib/lib -Iblib/arch -MTest::Harness -e '
  die "unexpected Harness interface" unless $Test::Harness::VERSION eq "3.48";
  my @tests = sort glob("t/*.t");
  die "default suite changed" unless join(" ", @tests) eq "t/00_compile.t t/01_basic.t t/02_renamed.t";
  $Test::Harness::Verbose = 1;
  my ($total, $failed, $todo_passed) = Test::Harness::execute_tests(tests => \@tests);
  die "missing statistics maps" unless ref($total) eq "HASH" && ref($failed) eq "HASH" && ref($todo_passed) eq "HASH";
  my %want = (files=>3, tests=>3, good=>3, max=>7, ok=>7, bad=>0, skipped=>0, sub_skipped=>0, todo=>0, bonus=>0);
  for my $key (sort keys %want) {
    die "invalid statistic $key" unless exists($total->{$key}) && defined($total->{$key}) && !ref($total->{$key}) && $total->{$key} =~ /\A[0-9]+\z/ && $total->{$key} == $want{$key};
    print "STRICT $key=$total->{$key}\n";
  }
  die "failed test files" if keys %$failed;
  die "unexpected TODO successes" if keys %$todo_passed;
  print "Cwd::Guard original 3 files / 7 assertions / zero failures, skips, TODO and bonus PASS\n";
'

%files
%license LICENSE README.md Changes META.json META.yml lib/Cwd/Guard.pm
%{perl_vendorlib}/Cwd/Guard.pm
%{_mandir}/man3/Cwd::Guard.3pm*

%changelog
* Tue Oct 06 2026 yinjiayi <yinjiayi@users.noreply.github.com> - 0.05-1
- Preserve the official source, original Module::Build tests and full notices.
- Require the original renamed-directory test and strict zero-skip statistics.
