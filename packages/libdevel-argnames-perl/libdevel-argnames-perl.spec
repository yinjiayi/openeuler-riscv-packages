# SPDX-License-Identifier: Apache-2.0
Name:           perl-Devel-ArgNames
Version:        0.03
Release:        1%{?dist}
Summary:        Identify variable names passed to Perl subroutines
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Devel-ArgNames
Source0:        Devel-ArgNames-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-PadWalker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators
Requires:       perl(PadWalker)
Requires:       perl(Test::use::ok)

%description
Devel::ArgNames uses PadWalker to discover the names of lexical or package
variables passed into Perl subroutines, for diagnostic and debugging output.

%prep
%autosetup -n Devel-ArgNames-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make_build

%install
%make_install pure_install
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Preserve the sole upstream default file, including lexical and unnamed args.
%make_build test

%files
%license lib/Devel/ArgNames.pm
%{perl_vendorlib}/Devel/ArgNames.pm
%{_mandir}/man3/Devel::ArgNames.3*

%changelog
* Sun Oct 04 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.03-1
- Package official CPAN source and retain complete upstream test file.
