# SPDX-License-Identifier: Apache-2.0
%global debug_package %{nil}

Name:           perl-Data-Perl
Version:        0.002011
Release:        1%{?dist}
Summary:        Classes wrapping fundamental Perl data types
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Data-Perl
Source0:        Data-Perl-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Class::Method::Modifiers)
BuildRequires:  perl(List::MoreUtils)
BuildRequires:  perl(List::Util)
BuildRequires:  perl(Module::Runtime)
BuildRequires:  perl(Role::Tiny)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Test::Deep)
BuildRequires:  perl(Test::Fatal)
BuildRequires:  perl(Test::Harness)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Output)
BuildRequires:  perl(parent)
BuildRequires:  perl(strictures)
BuildRequires:  perl-generators

%description
Data::Perl offers wrapper classes and constructors for Perl strings,
numbers, booleans, code references, arrays, and hashes.

%prep
%autosetup -n Data-Perl-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make_build

%install
%make_install
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Run every unchanged upstream default t/*.t and t/collection/*.t file.
# The two author-only POD tests self-skip unless AUTHOR_TESTING is set.
%make_build test

%files
%license LICENSE
%doc Changes README.mkdn
%{perl_vendorlib}/Data/Perl.pm
%{perl_vendorlib}/Data/Perl/
%{_mandir}/man3/Data::Perl*.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.002011-1
- Package the official CPAN release with its unchanged default test suite.
