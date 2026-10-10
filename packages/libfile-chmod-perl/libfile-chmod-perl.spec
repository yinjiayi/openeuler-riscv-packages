# SPDX-License-Identifier: Apache-2.0
Name:           perl-File-chmod
Version:        0.42
Release:        1%{?dist}
Summary:        Symbolic and ls-style chmod modes for Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/File-chmod
Source0:        File-chmod-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-File-Temp
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators

%description
File::chmod extends Perl's chmod operation to accept symbolic and ls-style
permission modes in addition to numeric modes.

%prep
%autosetup -n File-chmod-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Preserve all 19 upstream default tests and their author/release conditions.
%make_build test

%files
%license LICENSE
%doc README Changes CONTRIBUTING
%{perl_vendorlib}/File/chmod.pm
%{_mandir}/man3/File::chmod.3*

%changelog
* Tue Sep 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.42-1
- Package official CPAN release with the complete default upstream test set.
