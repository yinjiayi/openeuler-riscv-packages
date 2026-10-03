# SPDX-License-Identifier: Apache-2.0
Name:           perl-Data-Censor
Version:        0.04
Release:        2%{?dist}
Summary:        Censor sensitive fields in Perl data structures
License:        Artistic-2.0
URL:            https://metacpan.org/dist/Data-Censor
Source0:        Data-Censor-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Ref::Util)
BuildRequires:  perl(Clone)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl-generators
Requires:       perl(Ref::Util)
Requires:       perl(Clone)

%description
Data::Censor masks sensitive values in nested Perl hashes. It can also
clone an input structure before applying the configured replacements.

%prep
%autosetup -n Data-Censor-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Preserve all four upstream default files. manifest.t is explicitly an
# author-only RELEASE_TESTING check; all functional/POD tests must run.
if ! %make_build test TEST_VERBOSE=1 > upstream-tests.log 2>&1; then
  cat upstream-tests.log
  exit 1
fi
cat upstream-tests.log
grep -q '^Result: PASS$' upstream-tests.log
grep -q '^Files=4, Tests=15,' upstream-tests.log
for name in 00-load 01-basic pod; do
  grep -Eq "^t/${name}\\.t[[:space:].]*$" upstream-tests.log
done
test "$(grep -Ec '^ok (8|9|10|11) - clone_and_censor' upstream-tests.log)" -eq 4
grep -Eq '^t/manifest\.t[[:space:]]+skipped: Author tests not required for installation$' upstream-tests.log
if grep -E '^t/.*skipped:' upstream-tests.log | grep -Ev '^t/manifest\.t[[:space:]]+skipped: Author tests not required for installation$'; then
  echo 'A non-author upstream test skipped unexpectedly' >&2
  exit 1
fi
if grep -Eiq 'Clone not installed|# SKIP.*clone_and_censor' upstream-tests.log; then
  echo 'The functional clone branch skipped unexpectedly' >&2
  exit 1
fi

%files
%doc README Changes
%{perl_vendorlib}/Data/Censor.pm
%{_mandir}/man3/Data::Censor.3*

%changelog
* Sat Oct 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.04-2
- Match the upstream verbose test headers without weakening test assertions.

* Sat Oct 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.04-1
- Package official CPAN release and retain all default upstream tests.
