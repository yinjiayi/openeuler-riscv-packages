# SPDX-License-Identifier: Apache-2.0
Name:           libhttp-request-ascgi-perl
Version:        1.2
Release:        1%{?dist}
Summary:        Set up a CGI environment from an HTTP request
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/HTTP-Request-AsCGI
Source0:        HTTP-Request-AsCGI-1.2.tar.gz
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
BuildRequires:  perl(bytes)
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Class::Accessor)
BuildRequires:  perl(Class::Accessor::Fast)
BuildRequires:  perl(HTTP::Request)
BuildRequires:  perl(HTTP::Response) >= 1.53
BuildRequires:  perl(HTTP::Status)
BuildRequires:  perl(IO::File)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(URI)
BuildRequires:  perl(URI::Escape)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Config)
BuildRequires:  perl(Encode)
Requires:       perl
Requires:       perl(strict)
Requires:       perl(warnings)
Requires:       perl(bytes)
Requires:       perl(base)
Requires:       perl(Carp)
Requires:       perl(Class::Accessor::Fast)
Requires:       perl(HTTP::Request)
Requires:       perl(HTTP::Response) >= 1.53
Requires:       perl(HTTP::Status)
Requires:       perl(IO::File)
Requires:       perl(IO::Handle)
Requires:       perl(URI)
Requires:       perl(URI::Escape)

%description
Set up a CGI environment from an HTTP request

%prep
%autosetup -n HTTP-Request-AsCGI-%{version} -p1
cat <<'DONOR_NOTICE' > Dist-Zilla-NOTICE
The templates used for Makefile.PL and t/release-pod-{coverage,syntax}.t
come from Dist-Zilla 1.093400 (MakeMaker, PodTests and ExtraTests).
Copyright (c) 2009 by Ricardo SIGNES.
Redistributable under the same terms as Perl 5; see the accompanying LICENSE.
Source: https://cpan.metacpan.org/authors/id/R/RJ/RJBS/Dist-Zilla-1.093400.tar.gz
DONOR_NOTICE

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install DESTDIR=%{buildroot}
test -f %{buildroot}%{perl_vendorlib}/HTTP/Request/AsCGI.pm
test -f %{buildroot}%{_mandir}/man3/HTTP::Request::AsCGI.3pm

%check
make test TEST_VERBOSE=1

%files
%license LICENSE Dist-Zilla-NOTICE
%doc README Changes
%{perl_vendorlib}/HTTP/Request/AsCGI.pm
%{_mandir}/man3/HTTP::Request::AsCGI.3pm*

%changelog
* Mon Nov 09 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.2-1
- Package the original module, tests, and generated-template notice.
