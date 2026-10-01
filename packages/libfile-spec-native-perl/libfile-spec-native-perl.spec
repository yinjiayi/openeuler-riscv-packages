# SPDX-License-Identifier: Apache-2.0
Name:           perl-File-Spec-Native
Version:        1.004
Release:        1%{?dist}
Summary:        Access the native File::Spec implementation explicitly
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/File-Spec-Native
Source0:        File-Spec-Native-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-generators
BuildRequires:  perl(Path::Class)
BuildRequires:  perl(Test::More)

%description
File::Spec::Native exposes the native operating-system File::Spec
implementation as an explicit class for Perl path handling.

%prep
%autosetup -n File-Spec-Native-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Keep all four default upstream suites, include optional Path::Class
# assertions and enable module-load warnings check.
AUTHOR_TESTING=1 %make_build test

%files
%license LICENSE
%doc Changes README
%{perl_vendorlib}/File/Spec/Native.pm
%{_mandir}/man3/File::Spec::Native.3*

%changelog
* Tue Sep 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.004-1
- Package official stable CPAN release and complete default tests.
