# SPDX-License-Identifier: Apache-2.0
Name:           perl-File-Copy-Recursive-Reduced
Version:        0.008
Release:        1%{?dist}
Summary:        Reduced recursive file-copy routines for the Perl toolchain
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/File-Copy-Recursive-Reduced
Source0:        File-Copy-Recursive-Reduced-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-generators
BuildRequires:  perl(Capture::Tiny)
BuildRequires:  perl(File::Copy::Recursive)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(Path::Tiny)
BuildRequires:  perl(Test::More)

%description
File::Copy::Recursive::Reduced supplies file and directory copy routines
used by the Perl toolchain, with a smaller interface than File::Copy::Recursive.

%prep
%autosetup -n File-Copy-Recursive-Reduced-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Keep all three default upstream suites and enable their author-only
# comparisons against the separately available File::Copy::Recursive.
PERL_AUTHOR_TESTING=1 %make_build test

%files
%license LICENSE
%doc Changes README Todo
%{perl_vendorlib}/File/Copy/Recursive/Reduced.pm
%{_mandir}/man3/File::Copy::Recursive::Reduced.3*

%changelog
* Tue Sep 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.008-1
- Package the official stable CPAN release and upstream comparison tests.
