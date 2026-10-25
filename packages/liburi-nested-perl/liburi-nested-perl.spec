# SPDX-License-Identifier: Apache-2.0
Name:           perl-URI-Nested
Version:        0.10
Release:        1%{?dist}
Summary:        Represent nested URI schemes in Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/URI-Nested
Source0:        URI-Nested-%{version}.tar.gz
Patch0:         0001-load-direct-runtime-dependencies.patch

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-generators
BuildRequires:  perl(Carp)
BuildRequires:  perl(Module::Build) >= 0.30
BuildRequires:  perl(Test::More)
BuildRequires:  perl(URI) >= 1.40
BuildRequires:  perl(URI::QueryParam)
Requires:       perl(Carp)
Requires:       perl(URI) >= 1.40

%description
URI::Nested represents a URI containing another URI, including JDBC-style
scheme prefixes.

%prep
%autosetup -n URI-Nested-%{version} -p1

%build
%{__perl} Build.PL --installdirs vendor
./Build

%install
./Build install --destdir %{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
./Build test
%{__perl} -Iblib/lib -MURI::Nested -e '
  my $uri = URI::Nested->new("http://example.com/a");
  die "direct URI::Nested import failed\n"
    unless $uri->nested_uri->scheme eq "http"
      && $uri->nested_uri->host eq "example.com"
      && $uri->nested_uri->path eq "/a";
'

%files
%license README.md
%doc Changes
%{perl_vendorlib}/URI/Nested.pm
%{_mandir}/man3/URI::Nested.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.10-1
- Package official CPAN source with unchanged upstream tests and direct-use fix.
