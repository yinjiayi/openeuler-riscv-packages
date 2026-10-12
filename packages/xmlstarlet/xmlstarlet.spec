# SPDX-License-Identifier: Apache-2.0
Name:           xmlstarlet
Version:        1.6.1
Release:        15%{?dist}
Summary:        Command-line toolkit for processing XML documents
License:        MIT
URL:            https://xmlstar.sourceforge.net/
Source0:        xmlstarlet-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  libxml2-devel = 2.11.9-7.oe2403sp3
BuildRequires:  libxslt-devel = 1.1.39-7.oe2403sp3
BuildRequires:  make

%description
XMLStarlet is a command-line toolkit for querying, transforming, validating,
editing, and formatting XML documents with libxml2 and libxslt.

%package help
Summary:        Manual page for XMLStarlet
BuildArch:      noarch

%description help
The XMLStarlet command manual page.

%prep
%autosetup -p1

%build
%configure \
  --disable-build-docs \
  --with-libxml-include-prefix=%{_includedir}/libxml2 \
  --with-libxml-libs-prefix=%{_libdir} \
  --with-libxslt-include-prefix=%{_includedir} \
  --with-libxslt-libs-prefix=%{_libdir}
%make_build

%install
%make_install
mv %{buildroot}%{_bindir}/xml %{buildroot}%{_bindir}/xmlstarlet
rm -rf %{buildroot}%{_docdir}/xmlstarlet

%check
%make_build check

%files
%license COPYING Copyright
%doc AUTHORS ChangeLog NEWS README TODO
%{_bindir}/xmlstarlet

%files help
%{_mandir}/man1/xmlstarlet.1*

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.6.1-15
- Rebuild the fixed target package with all 79 upstream tests and explicit target library paths.
