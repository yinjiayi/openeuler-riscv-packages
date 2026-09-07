# SPDX-License-Identifier: Apache-2.0
Name:           findutils
Epoch:          2
Version:        4.11.0
Release:        2%{?dist}
Summary:        GNU utilities for finding files
License:        GPL-3.0-or-later
URL:            https://www.gnu.org/software/findutils/
Source0:        findutils-%{version}.tar.xz
Patch0:         0001-gnulib-normalize-unsigned-char-localeconv-sentinel.patch

BuildRequires:  dejagnu
BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  libselinux-devel
BuildRequires:  make
BuildRequires:  python3

%description
GNU findutils provides find, xargs, locate, and updatedb for locating files
and applying commands to selected path names.

%package help
Summary:        Documentation and translations for GNU findutils
BuildArch:      noarch

%description help
Manual pages, Info manuals, documentation, and translations for GNU findutils.

%prep
%autosetup -p1

%build
export gl_cv_func_localeconv_works=no
%configure \
  --with-packager="openEuler RISC-V" \
  --with-packager-version="%{epoch}:%{version}-%{release}"
%make_build

%install
%make_install
%find_lang %{name}
rm -f %{buildroot}%{_infodir}/dir
# The fixed target ships locate and updatedb from mlocate. Build and test the
# complete upstream locate implementation, but do not create file conflicts.
rm -f \
  %{buildroot}%{_bindir}/locate \
  %{buildroot}%{_bindir}/updatedb \
  %{buildroot}%{_libexecdir}/frcode \
  %{buildroot}%{_mandir}/man1/locate.1 \
  %{buildroot}%{_mandir}/man1/updatedb.1 \
  %{buildroot}%{_mandir}/man5/locatedb.5

%check
timeout 60m make -j1 check

%files
%license COPYING
%{_bindir}/find
%{_bindir}/xargs

%files help -f %{name}.lang
%license COPYING
%doc AUTHORS ChangeLog NEWS README THANKS TODO
%{_infodir}/find.info*
%{_infodir}/find-maint.info*
%{_mandir}/man1/find.1*
%{_mandir}/man1/xargs.1*

%changelog
* Tue Sep 01 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2:4.11.0-2
- Select the patched gnulib localeconv replacement for unsigned-char sentinels.

* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2:4.11.0-1
- Initial openEuler RISC-V package with the complete upstream check suite.
