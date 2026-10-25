# SPDX-License-Identifier: Apache-2.0
Name:           perl-Algorithm-Diff
Version:        1.201
Release:        1%{?dist}
Summary:        Perl modules for computing differences between sequences
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Algorithm-Diff
Source0:        Algorithm-Diff-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators

%description
Algorithm::Diff computes longest common subsequences and edit differences
between Perl sequences. Algorithm::DiffOld retains the earlier comparison
callback interface.

%prep
%autosetup -n Algorithm-Diff-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Run both upstream t/ test files without exclusions.
%make_build test

%files
%doc Changes README
%{perl_vendorlib}/Algorithm/Diff.pm
%{perl_vendorlib}/Algorithm/DiffOld.pm
%{_mandir}/man3/Algorithm::Diff*.3*

%changelog
* Tue Sep 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.201-1
- Package the official CPAN release and both upstream test files.
