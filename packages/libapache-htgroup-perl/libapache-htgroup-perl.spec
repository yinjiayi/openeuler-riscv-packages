# SPDX-License-Identifier: Apache-2.0
Name:           perl-Apache-Htgroup
Version:        1.23
Release:        1%{?dist}
Summary:        Manage Apache authentication group files in Perl
License:        Artistic-1.0
URL:            https://metacpan.org/dist/Apache-Htgroup
Source0:        https://cpan.metacpan.org/authors/id/R/RB/RBOW/Apache-Htgroup-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker) >= 7.70
BuildRequires:  perl(Test) >= 1.31
BuildRequires:  perl(Test::Harness) >= 3.48
BuildRequires:  make
BuildRequires:  coreutils
BuildRequires:  findutils
Requires:       perl
Requires:       perl(File::Temp)
Requires:       perl(Digest::SHA)
Requires:       util-linux
Requires:       coreutils
Requires:       bash
Requires:       grep

%description
Pure Perl management of Apache authentication group files. It is not a
mod_perl module and does not require or start an Apache server. This packaging
selects the original generic Artistic1.0 alternative and preserves the full
upstream license, dual grant and notices unchanged.

%prep
%autosetup -n Apache-Htgroup-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
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
perl -MTest -MTest::Harness -MExtUtils::MakeMaker -e 'Test->VERSION(1.31); Test::Harness->VERSION(3.48); ExtUtils::MakeMaker->VERSION(7.70); print "BUILD UID=$< EUID=$> GID=$( EGID=$)\n"; die "unsafe build identity" unless $< == 10001 && $> == 10001;'
# Keep the complete original MakeMaker suite before a strict statistics repeat.
timeout --kill-after=10s 180s make test
timeout --kill-after=10s 180s perl -Iblib/lib -Iblib/arch -MTest::Harness -e '
  my @t = sort glob("t/*.t");
  die "default suite changed" unless join(" ", @t) eq "t/00load.t t/01basic.t t/02scratch.t t/03add.t";
  $Test::Harness::Verbose = 1;
  my ($total, $failed, $todo_passed) = Test::Harness::execute_tests(tests => \@t);
  die "missing totals" unless ref($total) eq "HASH" && ref($failed) eq "HASH" && ref($todo_passed) eq "HASH";
  my %want = (files=>4, tests=>4, good=>4, max=>11, ok=>11, bad=>0, skipped=>0, sub_skipped=>0, todo=>0, bonus=>0);
  for my $k (sort keys %want) {
    die "invalid $k" unless exists($total->{$k}) && defined($total->{$k}) && !ref($total->{$k}) && $total->{$k} =~ /\A[0-9]+\z/ && $total->{$k} == $want{$k};
    print "STRICT $k=$total->{$k}\n";
  }
  die "failed test files" if keys %$failed;
  die "unexpected TODO successes" if keys %$todo_passed;
  print "Apache::Htgroup original 4 files / 11 assertions / zero failures, skips, TODO and bonus PASS\n";
'

%files
%license LICENSE README lib/Apache/Htgroup.pm
%{perl_vendorlib}/Apache/Htgroup.pm
%{_mandir}/man3/Apache::Htgroup.3pm*

%changelog
* Tue Oct 06 2026 yinjiayi <yinjiayi@users.noreply.github.com> - 1.23-1
- Proposed unchanged upstream release, full original tests and notices.
