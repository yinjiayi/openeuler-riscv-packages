# SPDX-License-Identifier: Apache-2.0
Name:           perl-List-Keywords
Version:        0.11
Release:        1%{?dist}
Summary:        Perl list-utility keyword plugins
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/List-Keywords
Source0:        List-Keywords-%{version}.tar.gz

BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-devel
BuildRequires:  perl(B::Deparse)
BuildRequires:  perl(Carp)
BuildRequires:  perl(List::Util)
BuildRequires:  perl(Time::HiRes)
BuildRequires:  perl-ExtUtils-CBuilder
BuildRequires:  perl-Module-Build
BuildRequires:  perl-Test-Pod
BuildRequires:  perl-Test2-Suite
BuildRequires:  perl-XS-Parse-Keyword-Builder
BuildRequires:  perl-generators
Requires:       perl(XS::Parse::Keyword) >= 0.05

%description
List::Keywords provides list-utility operations as lexical Perl keyword
plugins, including first, any, all, reduce and related forms.

%prep
%autosetup -n List-Keywords-%{version} -p1

%build
%{__perl} Build.PL --installdirs vendor
./Build

%install
./Build install --destdir %{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Keep all 13 default upstream files, including POD syntax and the benchmark-labelled test.
./Build test

%files
%license LICENSE
%doc README Changes
%{perl_vendorarch}/List/Keywords.pm
%{perl_vendorarch}/auto/List/Keywords/
%{_mandir}/man3/List::Keywords.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.11-1
- Package the official CPAN release with all default upstream tests.
