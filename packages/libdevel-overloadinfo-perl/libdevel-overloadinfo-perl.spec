# SPDX-License-Identifier: Apache-2.0
Name:           perl-Devel-OverloadInfo
Version:        0.008
Release:        1%{?dist}
Summary:        Introspect Perl overloaded operators
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Devel-OverloadInfo
Source0:        Devel-OverloadInfo-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-devel
BuildRequires:  perl(B)
BuildRequires:  perl(Exporter) >= 5.57
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(MRO::Compat)
BuildRequires:  perl(Package::Stash) >= 0.14
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Sub::Util) >= 1.40
BuildRequires:  perl(Test::Fatal)
BuildRequires:  perl(Test::Harness)
BuildRequires:  perl(Test::More) >= 0.88
BuildRequires:  perl(Text::ParseWords)
BuildRequires:  perl(overload)
BuildRequires:  perl(parent)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
BuildRequires:  perl-generators
Requires:       perl(B)
Requires:       perl(Exporter) >= 5.57
Requires:       perl(MRO::Compat)
Requires:       perl(Package::Stash) >= 0.14
Requires:       perl(Scalar::Util)
Requires:       perl(Sub::Util) >= 1.40
Requires:       perl(overload)
Requires:       perl(strict)
Requires:       perl(warnings)

%description
Devel::OverloadInfo reports overloaded Perl operators, their defining
classes and implementation code references.

%prep
%autosetup -n Devel-OverloadInfo-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Keep all four upstream default files. Both author-only checks self-skip;
# the two functional files must run all 22 assertions without a skip.
if ! %make_build test > upstream-tests.log 2>&1; then
  cat upstream-tests.log
  exit 1
fi
cat upstream-tests.log
grep -q '^Result: PASS$' upstream-tests.log
grep -Eq '^Files=4, Tests=22,' upstream-tests.log
grep -Eq '^t/basic\.t[[:space:].]+ok' upstream-tests.log
grep -Eq '^t/rt106379-inheritance-corruption\.t[[:space:].]+ok' upstream-tests.log
grep -Eq '^t/author-pod-spell\.t[[:space:].]+skipped: these tests are for testing by the author$' upstream-tests.log
grep -Eq '^t/author-pod-syntax\.t[[:space:].]+skipped: these tests are for testing by the author$' upstream-tests.log
test "$(grep -Ec '^t/.*skipped:' upstream-tests.log)" -eq 2
if grep -Eq '# SKIP|# skip' upstream-tests.log; then
  echo 'An upstream assertion was skipped unexpectedly' >&2
  exit 1
fi
%{__perl} -Iblib/lib -MDevel::OverloadInfo -MScalar::Util=refaddr -MSub::Util -e 'die "Sub::Util branch not active\n" unless refaddr(\&Devel::OverloadInfo::subname) == refaddr(\&Sub::Util::subname)'

%files
%license LICENSE
%doc README Changes
%{perl_vendorlib}/Devel/OverloadInfo.pm
%{_mandir}/man3/Devel::OverloadInfo.3*

%changelog
* Sat Oct 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.008-1
- Package official CPAN release and preserve its complete default test suite.
