# SPDX-License-Identifier: Apache-2.0
Name:           libperlio-eol-perl
Version:        0.19
Release:        1%{?dist}
Summary:        Normalize line endings through a PerlIO layer
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/PerlIO-eol
Source0:        PerlIO-eol-%{version}.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Temp) >= 0.19
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(IPC::Open3)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(XSLoader)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
Requires:       perl

%description
PerlIO::eol provides a native PerlIO layer for normalizing LF, CRLF and
CR line endings when reading and writing files.

%prep
%autosetup -n PerlIO-eol-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1 OPTIMIZE="%{optflags}"
%make_build
test -s blib/arch/auto/PerlIO/eol/eol.so

%install
make pure_install DESTDIR=%{buildroot}

%check
# Preserve the complete default suite, including its trailing-CR TODO.
make test TEST_VERBOSE=1

%files
%license LICENSE README
%doc Changes
%{perl_vendorarch}/PerlIO/eol.pm
%{perl_vendorarch}/auto/PerlIO/eol/
%{_mandir}/man3/PerlIO::eol.3pm*

%changelog
* Sun Nov 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.19-1
- Package the fixed XS release with the complete upstream default tests.
