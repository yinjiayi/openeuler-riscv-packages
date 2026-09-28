# SPDX-License-Identifier: Apache-2.0
Name:           perl-File-chdir
Version:        0.1011
Release:        1%{?dist}
Summary:        Localizable current working directory for Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/File-chdir
Source0:        File-chdir-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators

%description
File::chdir exposes a localizable current-working-directory variable for
Perl programs, allowing a nested directory change to restore the original
working directory when its scope ends.

%prep
%autosetup -n File-chdir-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Run all seven default upstream test files. Author/release quality checks
# under xt/ retain their upstream opt-in status.
%make_build test

%files
%license LICENSE
%doc Changes README CONTRIBUTING.mkdn
%{perl_vendorlib}/File/chdir.pm
%{_mandir}/man3/File::chdir.3*

%changelog
* Tue Sep 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.1011-1
- Package the official CPAN release and complete default upstream tests.
