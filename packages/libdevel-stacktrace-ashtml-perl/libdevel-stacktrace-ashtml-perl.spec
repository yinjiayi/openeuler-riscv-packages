# SPDX-License-Identifier: Apache-2.0
Name:           perl-Devel-StackTrace-AsHTML
Version:        0.15
Release:        1%{?dist}
Summary:        Render Perl stack traces as HTML
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Devel-StackTrace-AsHTML
Source0:        Devel-StackTrace-AsHTML-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Devel::StackTrace)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Test::Harness)
BuildRequires:  perl(Test::More) >= 0.88
BuildRequires:  perl-generators
Requires:       perl(Data::Dumper)
Requires:       perl(Devel::StackTrace)
Requires:       perl(Scalar::Util)

%description
Devel::StackTrace::AsHTML adds an HTML renderer to Devel::StackTrace,
including source context and safely escaped values.

%prep
%autosetup -n Devel-StackTrace-AsHTML-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Preserve all seven default upstream files. Four author/release checks
# self-skip in the published suite; the three functional files must execute.
if ! %make_build test > upstream-tests.log 2>&1; then
  cat upstream-tests.log
  exit 1
fi
cat upstream-tests.log
grep -q '^Result: PASS$' upstream-tests.log
grep -Eq '^Files=7, Tests=4,' upstream-tests.log
for test_file in 00_compile encoding output; do
  grep -Eq "^t/${test_file}\\.t[[:space:].]+ok" upstream-tests.log
done
grep -Eq '^t/author-pod-syntax\.t[[:space:].]+skipped: these tests are for testing by the author$' upstream-tests.log
grep -Eq '^t/author-synopsis\.t[[:space:].]+skipped: these tests are for testing by the author$' upstream-tests.log
grep -Eq '^t/release-perlcritic\.t[[:space:].]+skipped: these tests are for release candidate testing$' upstream-tests.log
grep -Eq '^t/release-podspell\.t[[:space:].]+skipped: these tests are for release candidate testing$' upstream-tests.log
test "$(grep -Ec '^t/.*skipped:' upstream-tests.log)" -eq 4
if grep -Eq '# SKIP|# skip' upstream-tests.log; then
  echo 'An upstream assertion was skipped unexpectedly' >&2
  exit 1
fi

%files
%license LICENSE
%doc README Changes
%{perl_vendorlib}/Devel/StackTrace/AsHTML.pm
%{_mandir}/man3/Devel::StackTrace::AsHTML.3*

%changelog
* Sat Oct 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.15-1
- Package official CPAN release and preserve its complete default test suite.
