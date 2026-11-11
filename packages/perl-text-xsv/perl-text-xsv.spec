# SPDX-License-Identifier: Apache-2.0
Name:           perl-Text-xSV
Version:        0.21
Release:        1%{?dist}
Summary:        Read and write character-separated text records in Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Text-xSV
Source0:        Text-xSV-0.21.tar.gz
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Harness
BuildRequires:  perl-generators
BuildArch:      noarch
Requires:       perl

%description
Read and write character-separated text records in Perl

%prep
%autosetup -p1 -n Text-xSV-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f \( -name .packlist -o -name perllocal.pod \) -delete

%check
%make_build test
# The legacy test.pl emits TAP but does not return failure on a not-ok line.
# Re-run unchanged under Test::Harness so all 48 assertions gate the build.
rm -f temp.csv
prove -b test.pl

%files
%license lib/Text/xSV.pm
%doc README Changes
%{perl_vendorlib}/Text/xSV.pm
%{_mandir}/man3/Text::xSV.3*

%changelog
* Thu Oct 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.21-1
- Package the upstream release and preserve its default test suite.
