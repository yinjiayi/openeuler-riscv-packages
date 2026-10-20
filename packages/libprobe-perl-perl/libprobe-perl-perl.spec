# SPDX-License-Identifier: Apache-2.0
Name:           perl-Probe-Perl
Version:        0.03
Release:        1%{?dist}
Summary:        Inspect the currently running Perl interpreter
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Probe-Perl
Source0:        Probe-Perl-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators

%description
Probe::Perl provides information about the current Perl interpreter,
its configuration and executable path.

%prep
%autosetup -n Probe-Perl-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Run both registered upstream t/ files. The upstream author-critic test
# explicitly skips unless AUTHOR_TESTING is set.
%make_build test

%files
%license LICENSE
%doc Changes README
%{perl_vendorlib}/Probe/Perl.pm
%{_mandir}/man3/Probe::Perl.3*

%changelog
* Tue Sep 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.03-1
- Package the official CPAN release and default upstream test suite.
