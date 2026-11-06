# SPDX-License-Identifier: Apache-2.0
%global debug_package %{nil}

Name:           perl-Data-MethodProxy
Version:        0.05
Release:        1%{?dist}
Summary:        Inject dynamic method results into static Perl data
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Data-MethodProxy
Source0:        Data-MethodProxy-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  perl
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Module::Runtime) >= 0.014
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Test2::V0) >= 0.000071
BuildRequires:  perl-Module-Build-Tiny >= 0.035
BuildRequires:  perl-generators

%description
Data::MethodProxy substitutes selected method results into structured Perl
data. Config::MethodProxy supplies its compatibility API.

%prep
%autosetup -n Data-MethodProxy-%{version} -p1

%build
%{__perl} Build.PL --installdirs vendor
./Build build

%install
./Build install --destdir %{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Run both default upstream test files without exclusions or assertion changes.
./Build test

%files
%license LICENSE
%doc README.md Changes
%{perl_vendorlib}/Data/MethodProxy.pm
%{perl_vendorlib}/Config/MethodProxy.pm
%{_mandir}/man3/Data::MethodProxy.3*
%{_mandir}/man3/Config::MethodProxy.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.05-1
- Package the official CPAN release with its unchanged default test suite.
