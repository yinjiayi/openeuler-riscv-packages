# SPDX-License-Identifier: Apache-2.0
Name:           perl-Class-Base
Version:        0.09
Release:        1%{?dist}
Summary:        Base class for deriving Perl modules
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Class-Base
Source0:        Class-Base-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl(Clone)
BuildRequires:  perl(CPAN::Meta)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(IPC::Open3)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(base)
BuildRequires:  perl(vars)
BuildRequires:  perl-generators
Requires:       perl(Clone)

%description
Class::Base supplies a constructor, configuration helpers, cloning, error
handling, and debugging methods for derived Perl classes.

%prep
%autosetup -n Class-Base-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Exercise all unchanged default tests, including the CPAN::Meta prereq branch.
%{__perl} -MCPAN::Meta -MCPAN::Meta::Prereqs -e 'CPAN::Meta->VERSION("2.120900")'
if ! %make_build test > upstream-tests.log 2>&1; then
  cat upstream-tests.log
  exit 1
fi
cat upstream-tests.log
grep -q '^Result: PASS$' upstream-tests.log
grep -Eq '^Files=3, Tests=47,' upstream-tests.log
if grep -Eiq 'skipped:|# SKIP' upstream-tests.log; then
  echo 'A default upstream test was skipped' >&2
  exit 1
fi

%files
%license LICENSE
%doc README README.mkdn Changes
%{perl_vendorlib}/Class/Base.pm
%{_mandir}/man3/Class::Base.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.09-1
- Package the official CPAN release with every default upstream test.
