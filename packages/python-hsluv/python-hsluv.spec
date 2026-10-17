# SPDX-License-Identifier: Apache-2.0
Name:           python-hsluv
Version:        5.0.4
Release:        1%{?dist}
Summary:        Human-friendly HSLuv and HPLuv color conversion
License:        MIT
URL:            https://github.com/hsluv/hsluv-python
Source0:        hsluv-5.0.4-official.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel >= 3.11
BuildRequires:  python3-setuptools >= 38.6.0
BuildRequires:  python3-wheel
BuildRequires:  python3-pip
%description
Pure Python implementation of HSLuv revision 4 and HPLuv color conversions,
with bidirectional RGB, XYZ, CIELUV, LCH and hexadecimal representations.

%package -n python3-hsluv
Summary:        Human-friendly HSLuv and HPLuv color conversion
Requires:       python3 >= 3.11

%description -n python3-hsluv
HSLuv and HPLuv color conversions with the complete original snapshot suite.

%prep
%autosetup -n hsluv-python-50a60aa6357fd5f743e39d8e29b771a645a83b4a

%build
# ZIP wheel timestamps have a 1980 lower bound. Preserve later RPM epochs.
source_date_epoch=${SOURCE_DATE_EPOCH-0}
case "$source_date_epoch" in
  ''|*[!0-9]*)
    printf '%s\n' 'SOURCE_DATE_EPOCH must be a nonnegative decimal integer' >&2
    exit 1
    ;;
esac
epoch_compare=$source_date_epoch
while [ "${epoch_compare#0}" != "$epoch_compare" ]; do
  epoch_compare=${epoch_compare#0}
done
epoch_compare=${epoch_compare:-0}
if [ "${#epoch_compare}" -lt 9 ] || \
   { [ "${#epoch_compare}" -eq 9 ] && [ "$epoch_compare" -lt 315532800 ]; }; then
  SOURCE_DATE_EPOCH=315532800
else
  SOURCE_DATE_EPOCH=$source_date_epoch
fi
export SOURCE_DATE_EPOCH
export PIP_NO_INDEX=1 PIP_DISABLE_PIP_VERSION_CHECK=1 PYTHONNOUSERSITE=1
%{__python3} setup.py sdist bdist_wheel

%install
export PIP_NO_INDEX=1 PIP_DISABLE_PIP_VERSION_CHECK=1 PYTHONNOUSERSITE=1
%{__python3} -m pip install --no-index --no-deps --ignore-installed --no-compile \
    --root %{buildroot} --prefix %{_prefix} dist/hsluv-%{version}-py2.py3-none-any.whl
# Installed CI reruns the same full tests against the RPM module, not sources.
install -d %{buildroot}%{_datadir}/python-hsluv/tests
install -m 0644 tests/__init__.py tests/test_hsluv.py tests/snapshot-rev4.json \
    %{buildroot}%{_datadir}/python-hsluv/tests/

%check
export PIP_NO_INDEX=1 PIP_DISABLE_PIP_VERSION_CHECK=1 PYTHONNOUSERSITE=1
# Exactly preserve upstream CI's sdist round-trip and setup.py test entrypoint.
install -d rpm-check-sdist
tar -xzf dist/hsluv-%{version}.tar.gz -C rpm-check-sdist
cd rpm-check-sdist/hsluv-%{version}
%{__python3} - <<'PY'
import json
import unittest
suite = unittest.defaultTestLoader.loadTestsFromName('tests.test_hsluv')
assert suite.countTestCases() == 2, ('incomplete original suite', suite.countTestCases())
with open('tests/snapshot-rev4.json') as stream:
    assert len(json.load(stream)) == 4096, 'incomplete original snapshot'
PY
%{__python3} setup.py test

%files -n python3-hsluv
%license LICENSE.txt
%doc README.md
%{python3_sitelib}/hsluv.py
%{python3_sitelib}/__pycache__/hsluv.*.pyc
%{python3_sitelib}/hsluv-%{version}.dist-info/
%{_datadir}/python-hsluv/

%changelog
* Sat Oct 10 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 5.0.4-1
- Onboard verified official release and preserve complete original sdist tests.
