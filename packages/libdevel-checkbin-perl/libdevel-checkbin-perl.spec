# SPDX-License-Identifier: Apache-2.0
Name:           perl-Devel-CheckBin
Version:        0.04
Release:        1%{?dist}
Summary:        Check whether an external command is available from Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Devel-CheckBin
Source0:        Devel-CheckBin-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.64
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(Test::More) >= 0.98
BuildRequires:  perl-generators
Requires:       perl(Config)
Requires:       perl(Exporter)
Requires:       perl(ExtUtils::MakeMaker) >= 6.52
Requires:       perl(File::Spec)
Requires:       perl(parent)

%description
Devel::CheckBin checks whether an executable command is available on
the current search path for a Perl build or program.

%prep
%autosetup -n Devel-CheckBin-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Keep all three original default files and both nested positive/negative
# command-availability branches. The source's check_bin deliberately exits
# zero for a missing command, so the unchanged test checks its message.
if ! %make_build test TEST_VERBOSE=1 > upstream-tests.log 2>&1; then
  cat upstream-tests.log
  exit 1
fi
cat upstream-tests.log
grep -q '^Result: PASS$' upstream-tests.log
grep -Eq '^Files=3, Tests=5,' upstream-tests.log
grep -q "ok 1 - missing 'unknown_command_name_here'" upstream-tests.log
if grep -Eiq 'skipped:|# SKIP' upstream-tests.log; then
  echo 'A default upstream test was skipped' >&2
  exit 1
fi

%files
%license LICENSE
%doc README.md Changes
%{perl_vendorlib}/Devel/CheckBin.pm
%{_mandir}/man3/Devel::CheckBin.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.04-1
- Package the official CPAN release with every default upstream test.
