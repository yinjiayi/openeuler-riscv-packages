# SPDX-License-Identifier: Apache-2.0
%define opensc_module "OpenSC PKCS #11 Module"
%define nssdb %{_sysconfdir}/pki/nssdb

Name:            opensc
Version:         0.23.0
Release:         8
License:         LGPL-2.1-or-later AND Apache-2.0 AND MIT AND ISC AND BSD-3-Clause AND LicenseRef-OpenSC-pkcs11-header AND LicenseRef-OpenSC-Windows-icon-unresolved
Summary:         Smart card library and applications
URL:             https://github.com/OpenSC/OpenSC/wiki
Source0:         https://github.com/OpenSC/OpenSC/releases/download/%{version}/%{name}-%{version}.tar.gz
# SOURCE-RIGHTS-HOLD: the source archive includes win32/DDORes.dll_14_2302.ico.
# Immutable upstream c57c9c36bf40c9dd6fee645e83fdc044f54051a4 identifies it as
# extracted from DDORes.dll; independent redistribution permission is unverified.
# The LicenseRef records an evidence gap, not a legal infringement determination.
Patch0:          0001-correct_left_length_calculation_to_fix_buffer.patch
Patch1:          0002-Prevent_stack_buffer_overflow_when_empty_ACL_is_returned.patch
# PATCH-FIX-UPSTREAM: CVE-2023-40660: PIN bypass when card tracks its own login state
Patch2:         0003-opensc-CVE-2023-40660-1of2.patch
Patch3:         0004-opensc-CVE-2023-40660-2of2.patch
# PATCH-FIX-UPSTREAM: CVE-2023-4535: out-of-bounds read in MyEID driver handling encryption using symmetric keys
Patch4:         0005-opensc-NULL_pointer_fix.patch
Patch5:         0006-opensc-CVE-2023-4535.patch
# PATCH-FIX-UPSTREAM: CVE-2023-40661: multiple memory issues with pkcs15-init (enrollment tool)
Patch6:         0007-opensc-CVE-2023-40661-1of12.patch
Patch7:         0008-opensc-CVE-2023-40661-2of12.patch
Patch8:         0009-opensc-CVE-2023-40661-3of12.patch
Patch9:         0010-opensc-CVE-2023-40661-4of12.patch
Patch10:        0011-opensc-CVE-2023-40661-5of12.patch
Patch11:        0012-opensc-CVE-2023-40661-6of12.patch
Patch12:        0013-opensc-CVE-2023-40661-7of12.patch
Patch13:        0014-opensc-CVE-2023-40661-8of12.patch
Patch14:        0015-opensc-CVE-2023-40661-9of12.patch
Patch15:        0016-opensc-CVE-2023-40661-10of12.patch
Patch16:        0017-opensc-CVE-2023-40661-11of12.patch
Patch17:        0018-opensc-CVE-2023-40661-12of12.patch
#CVE-2023-5992 constant-time-pkcs1.5.patch
# https://github.com/OpenSC/OpenSC/pull/2948
# https://github.com/OpenSC/OpenSC/pull/3016
Patch18:        0019-opensc-CVE-2023-5992.patch
Patch19:        0020-backport-avoid-calling-functions-without-prototype.patch
Patch20:        0021-opensc-CVE-2024-45615.patch
Patch21:        0022-opensc-CVE-2024-45616.patch
Patch22:        0023-opensc-CVE-2024-45617.patch
Patch23:        0024-opensc-CVE-2024-45618.patch
Patch24:        0025-opensc-CVE-2024-45619.patch
Patch25:        0026-opensc-CVE-2024-45620.patch
Patch26:        0027-opensc-CVE-2024-8443.patch

Patch27:         0028-upstream-rsa-private-import.patch
Patch28:         0029-upstream-rsa-import-followup.patch
Patch29:         0030-restore-openssl-constant-time-license.patch
Patch30:         0031-rsa-import-regression.patch

BuildRequires:   libcmocka-devel softhsm zlib-devel findutils binutils gawk grep sed coreutils diffutils
BuildRequires:   openssl-devel pcsc-lite-devel bash-completion docbook-style-xsl readline-devel
BuildRequires:   desktop-file-utils /usr/bin/xsltproc autoconf automake libtool gcc
BuildRequires:	 glib2-devel
Requires:        pcsc-lite
Obsoletes:       coolkey <= 1.1.0-36
Obsoletes:       mozilla-opensc-signer < 0.12.0
Obsoletes:       opensc-devel < 0.12.0

%description
OpenSC provides a set of libraries and utilities to work with smart cards.
Its main focus is on cards that support cryptographic operations, and
facilitate their use in security applications such as authentication,
mail encryption and digital signatures. OpenSC implements the standard
APIs to smart cards, e.g. PKCS#11 API, Windows’ Smart Card Minidriver
and macOS Tokend.

%package help
Summary:	Development documents and examples for opensc
Provides:	opensc-doc
%description help
Development documents and examples for opensc.

%prep
%autosetup -n %{name}-%{version} -p1

sed -i -e 's|/usr/local/towitoko/lib/|/usr/lib/ctapi/|' etc/opensc.conf.example.in
cp -p src/pkcs15init/README ./README.pkcs15init
cp -p src/scconf/README.scconf .

%build
%if "%toolchain" == "clang"
  CFLAGS="$CFLAGS -Wno-error=unused-command-line-argument -Wno-error=unused-but-set-variable"
%endif
autoreconf -fvi
sed -i -e 's/opensc.conf/opensc-%{_arch}.conf/g' src/libopensc/Makefile.in
sed -i -e 's|"/lib /usr/lib\b|"/%{_lib} %{_libdir}|' configure # lib64 rpaths
%configure  --disable-static \
  --disable-assert \
  --enable-tests \
  --enable-cmocka \
  --enable-zlib \
  --enable-openssl \
  --enable-readline \
  --enable-sm \
  --enable-pcsc \
  --with-pcsc-provider=libpcsclite.so.1
%make_build

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/opensc.conf
install -Dpm 644 etc/opensc.conf $RPM_BUILD_ROOT%{_sysconfdir}/opensc-%{_arch}.conf
touch -r NEWS $RPM_BUILD_ROOT%{_sysconfdir}/opensc-%{_arch}.conf
find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.la" | xargs rm
rm -rf %{buildroot}%{_mandir}/man1/npa-tool.1*
rm -f $RPM_BUILD_ROOT%{_libdir}/libsmm-local.so
rm -rf %{buildroot}%{_bindir}/npa-tool
rm -f $RPM_BUILD_ROOT%{_libdir}/libopensc.so
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/opensc
rm -rf %{buildroot}%{_bindir}/pkcs11-register
rm -rf %{buildroot}%{_mandir}/man1/pkcs11-register.1*
rm -rf %{buildroot}%{_sysconfdir}/xdg/autostart/pkcs11-register.desktop

desktop-file-validate %{buildroot}/%{_datadir}/applications/org.opensc.notify.desktop

%check
make check

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files help
%{_mandir}/man1/cardos-tool.1*
%{_mandir}/man1/cryptoflex-tool.1*
%{_mandir}/man1/dnie-tool.1*
%{_mandir}/man1/egk-tool.1*
%{_mandir}/man1/eidenv.1*
%{_mandir}/man1/gids-tool.1*
%{_mandir}/man1/goid-tool.1*
%{_mandir}/man1/iasecc-tool.1*
%{_mandir}/man1/netkey-tool.1*
%{_mandir}/man1/openpgp-tool.1*
%{_mandir}/man1/opensc-explorer.*
%{_mandir}/man1/opensc-tool.1*
%{_mandir}/man1/opensc-asn1.1*
%{_mandir}/man1/opensc-notify.1*
%{_mandir}/man1/piv-tool.1*
%{_mandir}/man1/pkcs11-tool.1*
%{_mandir}/man1/pkcs15-crypt.1*
%{_mandir}/man1/pkcs15-init.1*
%{_mandir}/man1/pkcs15-tool.1*
%{_mandir}/man1/sc-hsm-tool.1*
%{_mandir}/man1/westcos-tool.1*
%{_mandir}/man5/*.5*

%files
%license COPYING OpenSSL-LICENSE.txt src/common/LICENSE.compat_getopt
%doc NEWS README*
%{_datadir}/bash-completion/*
%config(noreplace) %{_sysconfdir}/opensc-%{_arch}.conf
%{_bindir}/cardos-tool
%{_bindir}/cryptoflex-tool
%{_bindir}/dnie-tool
%{_bindir}/egk-tool
%{_bindir}/eidenv
%{_bindir}/iasecc-tool
%{_bindir}/gids-tool
%{_bindir}/goid-tool
%{_bindir}/netkey-tool
%{_bindir}/openpgp-tool
%{_bindir}/opensc-explorer
%{_bindir}/opensc-tool
%{_bindir}/opensc-asn1
%{_bindir}/opensc-notify
%{_bindir}/piv-tool
%{_bindir}/pkcs11-tool
%{_bindir}/pkcs15-crypt
%{_bindir}/pkcs15-init
%{_bindir}/pkcs15-tool
%{_bindir}/sc-hsm-tool
%{_bindir}/westcos-tool
%{_libdir}/lib*.so.*
%{_libdir}/opensc-pkcs11.so
%{_libdir}/onepin-opensc-pkcs11.so
%{_libdir}/pkcs11-spy.so
%{_libdir}/pkgconfig/*.pc
%{_libdir}/pkcs11/opensc-pkcs11.so
%{_libdir}/pkcs11/onepin-opensc-pkcs11.so
%{_libdir}/pkcs11/pkcs11-spy.so
%dir %{_libdir}/pkcs11
%{_datadir}/applications/org.opensc.notify.desktop
%{_datadir}/opensc/

%changelog
* Sat Oct 03 2026 Codex <codex@localhost> - 0.23.0-8
- Preserve SP3 release 7 security patches and features; repair OpenSSL 3 RSA import.
- Enable original tests and add private-key import/signature regression.
- Restore Apache-2.0 attribution for the baseline constant-time helpers.

* Mon Oct 07 2024 Funda Wang <fundawang@yeah.net> - 0.23.0-7
- fix CVE-2024-8443, CVE-2024-45615, CVE-2024-45616,
  CVE-2024-45617, CVE-2024-45618, CVE-2024-45619, CVE-2024-45620

* Sun Sep 1 2024 yuanchao <1050706328@qq.com> - 0.23.0-6
- backport:avoid calling functions without prototype,and add compiler flags to support clang build

* Fri Jun 28 2024 dillon chen <dillon.chen@gmail.com> - 0.23.0-5
- fix CVE-2023-5992

* Fri Oct 20 2023 dillon chen <dillon.chen@gmail.com> - 0.23.0-4
- fix CVE-2023-40660  CVE-2023-4535  CVE-2023-40661

* Wed Sep 6 2023 Zhengxin Guo <guozhengxin@kylinos.cn> - 0.23.0-3
- fix CVE-2021-34193

* Tue Sep 5 2023 Zhengxin Guo <guozhengxin@kylinos.cn> - 0.23.0-2
- fix CVE-2023-2977

* Wed Feb 1 2023 wangjunqi <wangjunqi@kylinos.cn> - 0.23.0-1
- update version to 0.23.0

* Thu Aug 19 2021 zoulin <zoulin13@huawei.com> - 0.22.0-1
- Update version to 0.22.0

* Thu Mar 18 2021 Hugel <gengqihu1@huawei.com> - 0.21.0-2
- Remove unused file pkcs11-register.desktop

* Mon Jan 25 2021 zoulin <zoulin13@huawei.com> - 0.21.0-1
- Update to 0.21.0

* Sat Jan 23 2021 zoulin <zoulin13@huawei.com> - 0.20.0-6
- fix CVE-2020-26571

* Thu Dec 31 2020 yangzhuangzhuang <yangzhuangzhuang1@huawei.com> - 0.20.0-5
- fix CVE-2020-26570

* Mon Sep 21 2020 liquor <lirui130@huawei.com> - 0.20.0-4
- myeid: fixed memory leak

* Tue Aug 18 2020 liquor <lirui130@huawei.com> - 0.20.0-3
- rebuild for requirement package update

* Fri Feb 14 2020 openEuler Buildteam <buildteam@openeuler.org> - 0.20.0-2
- Make check after installation

* Sat Jan 11 2020 openEuler Buildteam <buildteam@openeuler.org> - 0.20.0-1
- Update to 0.20.0

* Mon Dec 16 2019 openEuler Buildteam <buildteam@openeuler.org> - 0.19.0-4
- Fix CVE-2019-6502

* Fri Sep 27 2019 openEuler Buildteam <buildteam@openeuler.org> - 0.19.0-3
- Adjust requires

* Fri Sep 27 2019 openEuler Buildteam <buildteam@openeuler.org> - 0.19.0-2
- Format patch

* Mon Aug 26 2019 openEuler Buildteam <buildteam@openeuler.org> - 0.19.0-1
- Package init
