# SPDX-License-Identifier: Apache-2.0
Name:           perl-Path-Iter
Version:        0.2
Release:        1%{?dist}
Summary:        Lightweight iterator for directory trees
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Path-Iter
Source0:        Path-Iter-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-Test-Pod
BuildRequires:  perl-Test-Pod-Coverage
BuildRequires:  perl-generators
BuildRequires:  perl(File::Spec)

%description
Path::Iter yields paths from a directory tree and supports custom handling
for symbolic links and directory traversal order.

%prep
%autosetup -n Path-Iter-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Retain all four upstream default files. perlcritic.t is an explicitly
# development-only check unless do_perl_critic_tests is set upstream.
%make_build test
test -f %{buildroot}%{perl_vendorlib}/Path/Iter.pm
PERL5LIB=%{buildroot}%{perl_vendorlib} %{__perl} -MPath::Iter -e 'die "unexpected version\n" unless $Path::Iter::VERSION == 0.2'

%files
%license lib/Path/Iter.pod
%doc README Changes
%{perl_vendorlib}/Path/Iter.pm
%{perl_vendorlib}/Path/Iter.pod
%{_mandir}/man3/Path::Iter.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.2-1
- Package official CPAN release with unchanged upstream default tests.
