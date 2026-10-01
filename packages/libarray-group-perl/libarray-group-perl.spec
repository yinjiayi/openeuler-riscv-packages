# SPDX-License-Identifier: Apache-2.0
Name:           perl-Array-Group
Version:        4.2
Release:        1%{?dist}
Summary:        Group Perl arrays into rows or interleaved columns
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Array-Group
Source0:        Array-Group-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators

%description
Array::Group divides an array into fixed-size rows or interleaved columns.

%prep
%autosetup -n Array-Group-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Run the complete registered upstream t/ suite (nine assertions).
%make_build test

%files
%license README
%doc Changes
%{perl_vendorlib}/Array/Group.pm
%{_mandir}/man3/Array::Group.3*

%changelog
* Tue Sep 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.2-1
- Package the official CPAN release and complete default test suite.
