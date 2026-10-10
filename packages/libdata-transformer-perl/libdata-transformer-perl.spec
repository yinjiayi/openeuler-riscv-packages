# SPDX-License-Identifier: Apache-2.0
%global debug_package %{nil}

Name:           perl-Data-Transformer
Version:        0.04
Release:        1%{?dist}
Summary:        Traverse and transform Perl data structures in place
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Data-Transformer
Source0:        Data-Transformer-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::Harness)
BuildRequires:  perl(Test::Simple) >= 0.44
BuildRequires:  perl-generators

%description
Data::Transformer traverses nested Perl data structures and applies
callbacks to change values and references in place while tracking
previously visited nodes.

%prep
%autosetup -n Data-Transformer-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make_build

%install
%make_install
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Run the sole unchanged upstream test file and all 29 assertions.
%make_build test

%files
%license LICENSE
%doc Changes README Todo
%{perl_vendorlib}/Data/Transformer.pm
%{_mandir}/man3/Data::Transformer.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.04-1
- Package the official CPAN release with its unchanged default test suite.
