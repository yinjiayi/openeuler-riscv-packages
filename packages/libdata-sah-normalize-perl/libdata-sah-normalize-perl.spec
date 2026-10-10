# SPDX-License-Identifier: Apache-2.0
%global debug_package %{nil}

Name:           perl-Data-Sah-Normalize
Version:        0.051
Release:        1%{?dist}
Summary:        Normalize Sah schemas and clause sets
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Data-Sah-Normalize
Source0:        Data-Sah-Normalize-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(IPC::Open3)
BuildRequires:  perl(Test::Exception)
BuildRequires:  perl(Test::More)
BuildRequires:  perl-generators

%description
Data::Sah::Normalize converts Sah schema and clause-set shorthand into
normalized structures without the full Data::Sah dependency tree.

%prep
%autosetup -n Data-Sah-Normalize-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make_build

%install
%make_install
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Run all unchanged upstream default files. The three author-only files
# self-skip unless AUTHOR_TESTING is set by the upstream distribution.
%make_build test

%files
%license LICENSE
%doc Changes README
%{perl_vendorlib}/Data/Sah/Normalize.pm
%{_mandir}/man3/Data::Sah::Normalize.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.051-1
- Package the official CPAN release and retain its full default test suite.
