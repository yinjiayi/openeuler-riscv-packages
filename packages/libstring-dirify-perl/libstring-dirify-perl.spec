# SPDX-License-Identifier: Apache-2.0
Name:           perl-String-Dirify
Version:        1.03
Release:        1%{?dist}
Summary:        Convert strings to safe directory names
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/String-Dirify
Source0:        String-Dirify-%{version}.tgz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-Test-Pod
BuildRequires:  perl-generators

%description
String::Dirify converts text, including HTML and high-ASCII characters,
into lowercase names suitable for directories.

%prep
%autosetup -n String-Dirify-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Run all three upstream default t/*.t files; xt/author/pod.t is author-only.
%make_build test

%files
%license LICENSE
%doc README Changes Changelog.ini
%{perl_vendorlib}/String/Dirify.pm
%{_mandir}/man3/String::Dirify.3*

%changelog
* Thu Oct 01 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.03-1
- Package official CPAN release with all default upstream tests.
