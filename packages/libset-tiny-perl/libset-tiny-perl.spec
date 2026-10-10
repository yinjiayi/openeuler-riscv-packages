# SPDX-License-Identifier: Apache-2.0
Name:           perl-Set-Tiny
Version:        0.06
Release:        1%{?dist}
Summary:        Small pure-Perl set implementation
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Set-Tiny
Source0:        Set-Tiny-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl(CPAN::Meta)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(IPC::Open3)
BuildRequires:  perl(Test::More)
BuildRequires:  perl-generators

%description
Set::Tiny provides set creation, membership, union, intersection and
difference operations in a small pure-Perl module.

%prep
%autosetup -n Set-Tiny-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Keep all four unchanged upstream default t/*.t files, including prereq reporting.
%{__perl} -MCPAN::Meta -MCPAN::Meta::Prereqs -e 1
if ! %make_build test > upstream-tests.log 2>&1; then
  cat upstream-tests.log
  exit 1
fi
cat upstream-tests.log
grep -q '^Result: PASS$' upstream-tests.log
grep -Eq '^Files=4, Tests=68,' upstream-tests.log
if grep -Eiq 'skipped:|# SKIP' upstream-tests.log; then
  echo 'A default upstream test was skipped' >&2
  exit 1
fi

%files
%license LICENSE
%doc README Changes
%{perl_vendorlib}/Set/Tiny.pm
%{_mandir}/man3/Set::Tiny.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.06-1
- Package the official CPAN release with every default upstream test.
