# SPDX-License-Identifier: Apache-2.0
Name:           perl-Devel-FindPerl
Version:        0.016
Release:        1%{?dist}
Summary:        Locate a Perl interpreter matching the current configuration
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Devel-FindPerl
Source0:        Devel-FindPerl-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl(Carp)
BuildRequires:  perl(Config)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(IPC::Open2)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Test::Harness)
BuildRequires:  perl(Test::More)
BuildRequires:  perl-generators
Requires:       perl(Carp)
Requires:       perl(Config)
Requires:       perl(Cwd)
Requires:       perl(Exporter)
Requires:       perl(File::Basename)
Requires:       perl(File::Spec::Functions)
Requires:       perl(IPC::Open2)
Requires:       perl(Scalar::Util)

%description
Devel::FindPerl discovers an executable Perl interpreter with the same
configuration as the one running the caller, including in taint mode.

%prep
%autosetup -n Devel-FindPerl-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Keep both original files and their two assertions, including taint mode.
if ! %make_build test > upstream-tests.log 2>&1; then
  cat upstream-tests.log
  exit 1
fi
cat upstream-tests.log
grep -q '^Result: PASS$' upstream-tests.log
grep -Eq '^Files=2, Tests=2,' upstream-tests.log
for test_file in 10-basics 11-tainted; do
  grep -Eq "^t/${test_file}\\.t[[:space:].]+ok" upstream-tests.log
done
if grep -Eiq 'skipped:|# SKIP' upstream-tests.log; then
  echo 'A default upstream test was skipped' >&2
  exit 1
fi

%files
%license LICENSE
%doc README Changes
%{perl_vendorlib}/Devel/FindPerl.pm
%{_mandir}/man3/Devel::FindPerl.3*

%changelog
* Sat Oct 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.016-1
- Package official CPAN release and preserve both default tests.
