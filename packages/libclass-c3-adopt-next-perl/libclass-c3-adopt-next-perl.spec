# SPDX-License-Identifier: Apache-2.0
Name:           perl-Class-C3-Adopt-NEXT
Version:        0.14
Release:        1%{?dist}
Summary:        Use C3 method resolution for legacy NEXT dispatch
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Class-C3-Adopt-NEXT
Source0:        Class-C3-Adopt-NEXT-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl(CPAN::Meta) >= 2.120900
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(List::Util) >= 1.33
BuildRequires:  perl(MRO::Compat)
BuildRequires:  perl(Module::Build::Tiny) >= 0.039
BuildRequires:  perl(NEXT)
BuildRequires:  perl(Test::Exception) >= 0.27
BuildRequires:  perl(Test::Harness)
BuildRequires:  perl(Test::More)
BuildRequires:  perl-generators
Requires:       perl(List::Util) >= 1.33
Requires:       perl(MRO::Compat)
Requires:       perl(NEXT)

%description
Class::C3::Adopt::NEXT adapts legacy NEXT method dispatch to C3 method
resolution, easing gradual migration of Perl class hierarchies.

%prep
%autosetup -n Class-C3-Adopt-NEXT-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Keep all eight default t/*.t files and 26 assertions. The checksum-verified
# release includes t/00-report-prereqs.dd; PERL5LIB=. lets its unchanged test
# load that report on Perl versions which omit '.' from @INC.
if ! PERL5LIB=. %make_build test TEST_VERBOSE=1 > upstream-tests.log 2>&1; then
  cat upstream-tests.log
  exit 1
fi
cat upstream-tests.log
grep -q '^Result: PASS$' upstream-tests.log
grep -Eq '^Files=8, Tests=26,' upstream-tests.log
grep -q 'Configure Requires' upstream-tests.log
grep -q 'Module::Build::Tiny' upstream-tests.log
for test_file in 00-report-prereqs basic disable disable_regex import incompatible nowarn warning_package; do
  grep -Eq "^t/${test_file}\\.t" upstream-tests.log
done
if grep -Eiq 'skipped:|# SKIP' upstream-tests.log; then
  echo 'A default upstream test was skipped' >&2
  exit 1
fi

%files
%license LICENSE
%doc README Changes
%{perl_vendorlib}/Class/C3/Adopt/NEXT.pm
%{_mandir}/man3/Class::C3::Adopt::NEXT.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.14-1
- Package official CPAN release with all eight default upstream tests.
