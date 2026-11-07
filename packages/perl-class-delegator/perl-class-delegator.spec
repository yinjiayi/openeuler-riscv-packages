# SPDX-License-Identifier: Apache-2.0
%global _default_patch_fuzz 0
Name:           perl-class-delegator
Version:        0.09
Release:        1%{?dist}
Summary:        Simple and fast object-oriented delegation for Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Class-Delegator
Source0:        Class-Delegator-0.09.tar.gz
Patch0:         0001-preserve-template-notice.patch
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl-devel
BuildRequires:  perl-Module-Build
BuildRequires:  perl-Test-Harness
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-Test-Pod
BuildRequires:  perl-Test-Pod-Coverage
BuildRequires:  perl-Carp
BuildRequires:  perl-generators
BuildRequires:  findutils
BuildRequires:  patch
Requires:       perl-Carp

%description
Class::Delegator installs object methods that forward to another object,
including renamed methods and delegation to multiple attributes.

%prep
%setup -q -n Class-Delegator-%{version}
%patch -P 0 -p1

%build
# Use the original Build.PL directly, not the generated CPAN-install fallback.
%{__perl} Build.PL --installdirs vendor
%{__perl} Build

%install
%{__perl} Build install --destdir %{buildroot}
find %{buildroot} -type f \( -name .packlist -o -name perllocal.pod \) -delete

%check
# Keep all original functional, POD and POD-coverage tests and their selection.
%{__perl} Build test

%files
%license README GENERATED-NOTICE
%doc Changes
%{perl_vendorlib}/Class/Delegator.pm
%{_mandir}/man3/Class::Delegator.3*

%changelog
* Sat Nov 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.09-1
- Retain original default tests and exact generated-template notices.
