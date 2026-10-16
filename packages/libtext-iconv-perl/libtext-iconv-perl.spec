# SPDX-License-Identifier: Apache-2.0
Name:           perl-Text-Iconv
Version:        1.7
Release:        1%{?dist}
Summary:        Perl interface to iconv character set conversion
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Text-Iconv
Source0:        Text-Iconv-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  glibc-devel
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-devel
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-generators

%description
Text::Iconv exposes the system iconv character set conversion interface to
Perl. The supported encodings depend on the installed libc conversion tables.

%prep
%autosetup -n Text-Iconv-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Keep both default upstream t/*.t files (14 assertions). Upstream skips
# unsupported conversion pairs based on the target libc's iconv tables.
%make_build test

%files
%license README
%doc Changes
%{perl_vendorarch}/Text/Iconv.pm
%{perl_vendorarch}/auto/Text/Iconv/
%{_mandir}/man3/Text::Iconv.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.7-1
- Package official CPAN release with both unmodified default test files.
