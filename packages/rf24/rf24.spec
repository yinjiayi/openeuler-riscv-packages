# SPDX-License-Identifier: Apache-2.0
Name:           rf24
Version:        1.5.0
Release:        2%{?dist}
Summary:        Linux support for RF24 radio modules
License:        GPL-2.0-or-later
URL:            https://github.com/nRF24/RF24
Source0:        rf24-1.5.0.tar.gz
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Linux support for RF24 radio modules

%prep
%autosetup -n RF24-%{version} -p1

%build
%configure --driver=SPIDEV --ldconfig=
%make_build

%install
install -d %{buildroot}%{_libdir}
install -pm0755 librf24.so.%{version} \
  %{buildroot}%{_libdir}/librf24.so.%{version}
ln -s librf24.so.%{version} %{buildroot}%{_libdir}/librf24.so.1.5
ln -s librf24.so.1.5 %{buildroot}%{_libdir}/librf24.so.1
ln -s librf24.so.1 %{buildroot}%{_libdir}/librf24.so
ln -s librf24.so %{buildroot}%{_libdir}/librf24-bcm.so

install -d %{buildroot}%{_includedir}/RF24/utility/SPIDEV
install -pm0644 RF24.h RF24_config.h nRF24L01.h printf.h \
  %{buildroot}%{_includedir}/RF24/
install -pm0644 utility/includes.h \
  %{buildroot}%{_includedir}/RF24/utility/
install -pm0644 utility/SPIDEV/*.h \
  %{buildroot}%{_includedir}/RF24/utility/SPIDEV/
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
test -s %{buildroot}%{_libdir}/librf24.so.%{version}
test "$(readlink %{buildroot}%{_libdir}/librf24.so.1)" = "librf24.so.1.5"
test -s %{buildroot}%{_includedir}/RF24/RF24.h

%files -f %{name}.files
%license LICENSE
%doc README.md

%changelog
* Mon Aug 31 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.5.0-2
- Use the verified upstream archive root and deterministic SPIDEV configuration.
- Install the versioned library, ABI links, and public headers without invoking ldconfig.
- Validate the real packaged payload because upstream provides no automated test suite.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.5.0-1
- Initial openEuler RISC-V package from the full package inventory.
