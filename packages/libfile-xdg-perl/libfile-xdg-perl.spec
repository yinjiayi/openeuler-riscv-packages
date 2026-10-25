# SPDX-License-Identifier: Apache-2.0
Name:           perl-File-XDG
Version:        1.03
Release:        1%{?dist}
Summary:        Access XDG base directories from Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/File-XDG
Source0:        File-XDG-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-generators
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(Path::Class)
BuildRequires:  perl(Path::Tiny)
BuildRequires:  perl(Ref::Util)
BuildRequires:  perl(Test::More)
# The default API dynamically loads Path::Class, which automated Perl
# dependency generation cannot infer from a string-valued class name.
Requires:       perl(Path::Class)

%description
File::XDG gives Perl programs XDG configuration, data, cache and runtime
directory locations and related lookup methods.

%prep
%autosetup -n File-XDG-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# The full upstream lookup suite writes under HOME. Isolate HOME and remove
# inherited XDG home overrides rather than shortening the suite.
test_home="$(mktemp -d)"
trap 'rm -r -- "$test_home"' EXIT
env -u XDG_CONFIG_HOME -u XDG_DATA_HOME -u XDG_CACHE_HOME HOME="$test_home" %make_build test

%files
%license LICENSE
%doc Changes README
%{perl_vendorlib}/File/XDG.pm
%{_mandir}/man3/File::XDG.3*

%changelog
* Tue Sep 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.03-1
- Package official stable CPAN release and isolate its full XDG tests.
