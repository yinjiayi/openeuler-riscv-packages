# SPDX-License-Identifier: Apache-2.0
Name:           hp2xx
Version:        3.4.4
Release:        1%{?dist}
Summary:        Converts HP-GL Plotter Language into a Variety of Formats
License:        GPL-2.0-or-later
URL:            https://www.gnu.org/software/hp2xx/
Source0:        hp2xx-3.4.4.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  libX11-devel
BuildRequires:  libpng-devel
BuildRequires:  libtiff-devel
BuildRequires:  texinfo


%description
Converts HP-GL Plotter Language into a Variety of Formats

%prep
%autosetup -p1
# GCC 14 rejects upstream strings passed directly as printf formats.
sed -i 's/fprintf(md, poly_end);/fprintf(md, "%s", poly_end);/g; s/fprintf(md, exit_cmd);/fprintf(md, "%s", exit_cmd);/' sources/to_vec.c

%build
%make_build -C sources \
  CFLAGS="%{optflags}" \
  LFLAGS="%{build_ldflags}" \
  hp2xx hp2xx.info

%install
install -Dpm0755 sources/hp2xx %{buildroot}%{_bindir}/hp2xx
install -Dpm0644 sources/hp2xx.info %{buildroot}%{_infodir}/hp2xx.info
install -Dpm0644 doc/hp2xx.1 %{buildroot}%{_mandir}/man1/hp2xx.1

%check
%make_build -C sources check

%files
%license copying
%doc AUTHORS
%doc CHANGES
%doc README
%{_bindir}/*
%{_infodir}/hp2xx.info*
%{_mandir}/man1/hp2xx.1*

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.4.4-1
- Initial openEuler RISC-V package from the full package inventory.
