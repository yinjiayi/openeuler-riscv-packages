# SPDX-License-Identifier: Apache-2.0
Name:           perl-Class-Accessor-Children
Version:        0.02
Release:        1%{?dist}
Summary:        Generate child classes with normal and fast accessors
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Class-Accessor-Children
Source0:        Class-Accessor-Children-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl(Class::Accessor)
BuildRequires:  perl(Class::Accessor::Fast)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl-generators
Requires:       perl(Class::Accessor)
Requires:       perl(Class::Accessor::Fast)

%description
Class::Accessor::Children creates child classes with generated normal
or fast accessor methods, including read-only and write-only variants.

%prep
%autosetup -n Class-Accessor-Children-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Keep all eight unchanged default tests, including POD and fast accessors.
%{__perl} -MTest::Pod -e 1
if ! %make_build test > upstream-tests.log 2>&1; then
  cat upstream-tests.log
  exit 1
fi
cat upstream-tests.log
grep -q '^Result: PASS$' upstream-tests.log
grep -Eq '^Files=8, Tests=112,' upstream-tests.log
if grep -Eiq 'skipped:|# SKIP' upstream-tests.log; then
  echo 'A default upstream test was skipped' >&2
  exit 1
fi

%files
%doc README Changes
%{perl_vendorlib}/Class/Accessor/Children.pm
%{perl_vendorlib}/Class/Accessor/Children/Fast.pm
%{_mandir}/man3/Class::Accessor::Children.3*
%{_mandir}/man3/Class::Accessor::Children::Fast.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.02-1
- Package the official CPAN release with every default upstream test.
