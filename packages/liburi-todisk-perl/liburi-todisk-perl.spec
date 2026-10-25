# SPDX-License-Identifier: Apache-2.0
Name:           perl-URI-ToDisk
Version:        1.12
Release:        1%{?dist}
Summary:        Map Perl URIs to filesystem paths
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/URI-ToDisk
Source0:        URI-ToDisk-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Clone
BuildRequires:  perl-Params-Util
BuildRequires:  perl-URI
BuildRequires:  perl-Scalar-List-Utils
BuildRequires:  perl-PathTools
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators
Requires:       perl(Clone) >= 0.21
Requires:       perl(Params::Util) >= 0.10
Requires:       perl(URI)
Requires:       perl(List::Util) >= 1.11
Requires:       perl(File::Spec)

%description
URI::ToDisk pairs a URI with a filesystem path and supports URI-aware
catdir and catfile operations. It does not create files or directories.

%prep
%autosetup -n URI-ToDisk-%{version} -p1

%build
# Upstream's bundled inc::Module::Install needs the source root in @INC.
%{__perl} -I. Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Keep all four original default tests; upstream skips two author-only files.
%make_build test

%files
%license LICENSE
%doc Changes README
%{perl_vendorlib}/URI/ToDisk.pm
%{_mandir}/man3/URI::ToDisk.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.12-1
- Package official CPAN release with all default upstream tests retained.
