# SPDX-License-Identifier: Apache-2.0
Name:           perl-List-Maker
Version:        0.005
Release:        1%{?dist}
Summary:        Compact list construction syntax for Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/List-Maker
Source0:        List-Maker-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  perl
BuildRequires:  perl-Devel-Symdump
BuildRequires:  perl-Module-Build
BuildRequires:  perl-Pod-Coverage
BuildRequires:  perl-Pod-Parser
BuildRequires:  perl-Scalar-List-Utils
BuildRequires:  perl-Test-Pod
BuildRequires:  perl-Test-Pod-Coverage
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators

%description
List::Maker provides a compact list-construction syntax by adapting Perl's
glob syntax within code that explicitly imports the module.

%prep
%autosetup -n List-Maker-%{version} -p1

%build
%{__perl} Build.PL --installdirs vendor
./Build

%install
./Build install --destdir %{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
./Build test

%files
%license README
%doc Changes
%{perl_vendorlib}/List/Maker.pm
%{perl_vendorlib}/List/Maker/
%{_mandir}/man3/List::Maker.3*

%changelog
* Thu Oct 01 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.005-1
- Package the official CPAN release with all default upstream tests.
