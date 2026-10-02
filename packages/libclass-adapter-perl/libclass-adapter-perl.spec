# SPDX-License-Identifier: Apache-2.0
Name:           perl-Class-Adapter
Version:        1.09
Release:        2%{?dist}
Summary:        Adapt Perl objects to another class interface
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Class-Adapter
Source0:        Class-Adapter-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl(CPAN::Meta)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Scalar::Util) >= 1.10
BuildRequires:  perl(Test::More)
BuildRequires:  perl(base)
BuildRequires:  perl(constant)
BuildRequires:  perl-generators
Requires:       perl(Carp)
Requires:       perl(Scalar::Util) >= 1.10

%description
Class::Adapter wraps Perl objects, while its Clear and Builder modules
provide transparent delegation and generated adapter classes.

%prep
%autosetup -n Class-Adapter-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Keep all eight original default files, including Builder, Clear,
# AUTOLOAD, static dispatch and destruction behavior.
if ! %make_build test TEST_VERBOSE=1 > upstream-tests.log 2>&1; then
  cat upstream-tests.log
  exit 1
fi
cat upstream-tests.log
grep -q '^Result: PASS$' upstream-tests.log
grep -Eq '^Files=8, Tests=65,' upstream-tests.log
# TEST_VERBOSE=1 prints the file header, TAP, and final "ok" separately.
# Overall PASS and exact aggregate above still require the whole suite to pass.
grep -Eq '^t/07_destroy\.t[[:space:]]' upstream-tests.log
if grep -Eiq 'skipped:|# SKIP' upstream-tests.log; then
  echo 'A default upstream test was skipped' >&2
  exit 1
fi

%files
%license LICENSE
%doc README Changes
%{perl_vendorlib}/Class/Adapter.pm
%{perl_vendorlib}/Class/Adapter/Builder.pm
%{perl_vendorlib}/Class/Adapter/Clear.pm
%{_mandir}/man3/Class::Adapter.3*
%{_mandir}/man3/Class::Adapter::Builder.3*
%{_mandir}/man3/Class::Adapter::Clear.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.09-2
- Keep the complete verbose upstream suite and recognize its split file header.

* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.09-1
- Package the official CPAN release with all default upstream tests.
