# SPDX-License-Identifier: Apache-2.0
Name:           ed
Version:        1.22.6
Release:        1%{?dist}
Summary:        GNU line-oriented text editor
License:        GPL-2.0-only AND GFDL-1.3-no-invariants-or-later
URL:            https://www.gnu.org/software/ed/
Source0:        ed-1.22.6.tar.lz

BuildRequires:  gcc
BuildRequires:  lzip
BuildRequires:  make

%description
GNU ed is a line-oriented text editor for creating, displaying, and modifying
text files interactively or from shell scripts.

%prep
%autosetup -p1

%build
%set_build_flags
./configure \
    --prefix=%{_prefix} \
    --exec-prefix=%{_exec_prefix} \
    --bindir=%{_bindir} \
    --datarootdir=%{_datadir} \
    --infodir=%{_infodir} \
    --mandir=%{_mandir} \
    CC="%{__cc}" \
    CPPFLAGS="${CPPFLAGS}" \
    CFLAGS="${CFLAGS}" \
    LDFLAGS="${LDFLAGS}"
%make_build

%install
%make_install
rm -f %{buildroot}%{_infodir}/dir

%check
%make_build check

%files
%license COPYING doc/fdl.texi
%doc AUTHORS ChangeLog NEWS README
%{_bindir}/ed
%{_bindir}/red
%{_mandir}/man1/ed.1*
%{_mandir}/man1/red.1*
%{_infodir}/ed.info*

%changelog
* Tue Aug 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.22.5-1
- Initial openEuler RISC-V package from reviewed Fedora 44 and upstream evidence.
