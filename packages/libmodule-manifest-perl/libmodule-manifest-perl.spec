# SPDX-License-Identifier: Apache-2.0
Name:           libmodule-manifest-perl
Version:        1.09
Release:        1%{?dist}
Summary:        Read and examine Perl distribution manifest files
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Module-Manifest
Source0:        Module-Manifest-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Params::Util) >= 0.10
BuildRequires:  perl(CPAN::Meta)
BuildRequires:  perl(Test::Exception)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Warn)
Requires:       perl(Params::Util) >= 0.10

%description
Module::Manifest reads a Perl distribution MANIFEST and an optional
MANIFEST.SKIP, exposing the listed files and testing exclusion patterns.

%prep
%autosetup -n Module-Manifest-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install DESTDIR=%{buildroot}

%check
# The stock release does not include MANIFEST.SKIP. Run the unchanged
# default tests as shipped, then add only a temporary positive test
# fixture and run the same tests again to exercise the guarded cases.
test ! -e MANIFEST.SKIP
printf '%s\n' 'Module::Manifest stock upstream suite'
make test TEST_VERBOSE=1
trap 'rm -f -- MANIFEST.SKIP' EXIT
printf '%s\n' '(^|/)\.git(/|$)' > MANIFEST.SKIP
printf '%s\n' 'Module::Manifest supplemental fixture suite'
make test TEST_VERBOSE=1

%files
%license LICENSE
%doc Changes README
%{perl_vendorlib}/Module/Manifest.pm
%{_mandir}/man3/Module::Manifest.3pm*

%changelog
* Sun Nov 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.09-1
- Package the fixed upstream release and retain the complete default suite.
