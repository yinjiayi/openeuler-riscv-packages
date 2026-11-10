# SPDX-License-Identifier: Apache-2.0
Name:           libjson-pointer-perl
Version:        0.07
Release:        1%{?dist}
Summary:        Resolve JSON Pointers and apply pointer-based updates in Perl
License:        (GPL-1.0-or-later OR Artistic-1.0-Perl) AND Artistic-2.0
URL:            https://metacpan.org/dist/JSON-Pointer
Source0:        JSON-Pointer-0.07.tar.gz
Source1:        Minilla-v1.0.0-LICENSE.txt
Source2:        Mojolicious-v4.0-Artistic-2.0.txt
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl-generators
BuildRequires:  perl(Module::Build) >= 0.38
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(CPAN::Meta)
BuildRequires:  perl(CPAN::Meta::Prereqs)
BuildRequires:  perl(B)
BuildRequires:  perl(Carp) >= 1.20
BuildRequires:  perl(Class::Accessor::Lite) >= 0.05
BuildRequires:  perl(Clone) >= 0.36
BuildRequires:  perl(Exporter)
BuildRequires:  perl(JSON) >= 2.53
BuildRequires:  perl(URI::Escape) >= 3.31
BuildRequires:  perl(Test::Exception) >= 0.31
BuildRequires:  perl(Test::More) >= 0.98
Requires:       perl
Requires:       perl(B)
Requires:       perl(Carp) >= 1.20
Requires:       perl(Class::Accessor::Lite) >= 0.05
Requires:       perl(Clone) >= 0.36
Requires:       perl(Exporter)
Requires:       perl(JSON) >= 2.53
Requires:       perl(URI::Escape) >= 3.31

%description
Resolve pointers into Perl JSON data and apply pointer-based updates.

%prep
%autosetup -n JSON-Pointer-%{version} -p1
cp -p %{SOURCE1} %{SOURCE2} .
cat <<'DONOR_NOTICE' > SOURCE-DONOR-NOTICE
Build.PL was generated from Minilla v1.0.0 (copyright 2013 tokuhirom)
using the ModuleBuild template and JSON::Pointer's project settings.
The complete donor Perl dual grant is in Minilla-v1.0.0-LICENSE.txt.
Reference: https://github.com/tokuhirom/Minilla/blob/dabf5aaae1e7896ad078b6170024fa5476c22f8a/lib/Minilla/ModuleMaker/ModuleBuild.pm

The adapted test t/003_mojo_json_pointer_compat.t includes assertions
derived from Mojolicious v4.0, copyright 2008-2013 Sebastian Riedel.
The adaptation uses JSON::Pointer instead of Mojo::JSON::Pointer,
adds percent-encoded path cases, and omits the donor's separate
Unicode and RFC 6901 blocks. The adapted test source is available in
Source0 and may be redistributed under Artistic License 2.0; the
complete original terms are in Mojolicious-v4.0-Artistic-2.0.txt.
Reference: https://github.com/mojolicious/mojo/blob/ad31e23ba56b4082aa9d2e291f11f3ec1e56c7ab/t/mojo/json_pointer.t
DONOR_NOTICE

%build
%{__perl} Build.PL --installdirs vendor
%{__perl} ./Build

%install
%{__perl} ./Build install --destdir "%{buildroot}" --create_packlist 0

%check
HARNESS_VERBOSE=1 %{__perl} ./Build test

%files
%license LICENSE Minilla-v1.0.0-LICENSE.txt Mojolicious-v4.0-Artistic-2.0.txt SOURCE-DONOR-NOTICE
%doc README.md Changes
%{perl_vendorlib}/JSON/Pointer.pm
%{perl_vendorlib}/JSON/Pointer/Context.pm
%{perl_vendorlib}/JSON/Pointer/Exception.pm
%{perl_vendorlib}/JSON/Pointer/Syntax.pm
%{_mandir}/man3/JSON::Pointer.3pm*
%{_mandir}/man3/JSON::Pointer::Context.3pm*
%{_mandir}/man3/JSON::Pointer::Exception.3pm*
%{_mandir}/man3/JSON::Pointer::Syntax.3pm*

%changelog
* Mon Nov 09 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.07-1
- Package the signed official release, original tests, and donor notices.
