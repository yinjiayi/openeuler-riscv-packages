# SPDX-License-Identifier: Apache-2.0
Name:           sed
Version:        4.10
Release:        2%{?dist}
Summary:        GNU stream-oriented text editor
License:        GPL-3.0-or-later
URL:            https://www.gnu.org/software/sed/
Source0:        sed-%{version}.tar.xz
Patch0:         0001-gnulib-normalize-unsigned-char-localeconv-sentinel.patch

BuildRequires:  gcc
BuildRequires:  gettext-devel
BuildRequires:  glibc-all-langpacks
BuildRequires:  libacl-devel
BuildRequires:  libselinux-devel
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl(FileHandle)
BuildRequires:  perl-Getopt-Long

Provides:       /bin/sed
Provides:       bundled(gnulib)

%description
GNU sed is a non-interactive stream editor. It transforms text using editing
commands supplied on the command line or in a script.

%prep
%autosetup -p1

%build
export gl_cv_func_localeconv_works=no
%configure \
  --disable-silent-rules \
  --with-included-regex
%make_build

%install
%make_install
rm -f %{buildroot}%{_infodir}/dir
%find_lang %{name}

%check
%make_build check

%files -f %{name}.lang
%license COPYING
%doc AUTHORS BUGS NEWS README THANKS
%{_bindir}/sed
%{_infodir}/sed.info*
%{_mandir}/man1/sed.1*

%changelog
* Mon Aug 31 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.10-2
- Export the localeconv cache result so configure selects the patched gnulib replacement.

* Tue Aug 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.10-1
- Initial openEuler RISC-V package from reviewed Fedora 44 and upstream evidence.
