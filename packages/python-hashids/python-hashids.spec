# SPDX-License-Identifier: Apache-2.0
Name:           python-hashids
Version:        1.3.1
Release:        1%{?dist}
Summary:        Generate reversible short identifiers from integers
License:        MIT
URL:            https://github.com/davidaurelio/hashids-python
Source0:        hashids-1.3.1-official.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel >= 3.11
BuildRequires:  python3-flit-core >= 2
BuildRequires:  python3-flit-core < 4
BuildRequires:  python3-pip
BuildRequires:  python3-pytest >= 2.1.0

%description
Hashids encodes one or more nonnegative integers as reversible short identifiers
with configurable salts, alphabets and minimum lengths. This is not encryption.

%package -n python3-hashids
Summary:        Generate reversible short identifiers from integers
Requires:       python3 >= 3.11
Requires:       python3-pytest >= 2.1.0

%description -n python3-hashids
Pure Python identifier conversion with both modern and legacy APIs and the
complete original test suite for installed-package acceptance.

%prep
%autosetup -n hashids-python-138a12e85d09e7e76eebc1d0e059b2e28ba488e6

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
# Original flit_core backend and bounds; no dependency fetch/build isolation.
%{__python3} -m pip wheel --no-index --no-deps --no-build-isolation \
    --wheel-dir dist .

%install
export PIP_NO_INDEX=1 PIP_DISABLE_PIP_VERSION_CHECK=1 PYTHONNOUSERSITE=1
%{__python3} -m pip install --no-index --no-deps --ignore-installed --no-compile \
    --root %{buildroot} --prefix %{_prefix} dist/hashids-%{version}-py2.py3-none-any.whl
install -d %{buildroot}%{_datadir}/python-hashids/test
install -m 0644 test/test_hashids.py test/test_legacy.py \
    %{buildroot}%{_datadir}/python-hashids/test/

%check
export PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1
# Upstream .travis.yml's default entrypoint, no selection, exclusions or ignores.
# The reporting option does not change collection or test behavior.
%{__python3} -m pytest --junitxml=rpm-check-results.xml
%{__python3} - <<'PY'
import xml.etree.ElementTree as ET
suites = ET.parse('rpm-check-results.xml').getroot().findall('testsuite')
assert sum(int(s.attrib['tests']) for s in suites) == 60, 'incomplete original suite'
for key in ('failures', 'errors', 'skipped'):
    assert sum(int(s.attrib[key]) for s in suites) == 0, key
PY

%files -n python3-hashids
%license LICENSE
%doc README.rst CHANGELOG.md
%{python3_sitelib}/hashids.py
%{python3_sitelib}/__pycache__/hashids.*.pyc
%{python3_sitelib}/hashids-%{version}.dist-info/
%{_datadir}/python-hashids/

%changelog
* Sat Oct 10 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.3.1-1
- Onboard fixed official stable source and retain all 60 original API tests.
