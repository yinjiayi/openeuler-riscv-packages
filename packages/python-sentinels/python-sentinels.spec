# SPDX-License-Identifier: Apache-2.0
Name:           python-sentinels
Version:        1.1.1
Release:        1%{?dist}
Summary:        Singleton sentinel objects for special Python values
License:        BSD-3-Clause
URL:            https://github.com/vmalloc/sentinels
Source0:        sentinels-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-wheel
BuildRequires:  python3-hatchling
BuildRequires:  python3-hatch-vcs
BuildRequires:  python3-pytest
BuildRequires:  python3-pylint

%description
Sentinels provides named singleton objects for special Python values. Copying
and pickling preserve their identity, allowing defaults distinct from None.

%package -n python3-sentinels
Summary:        Singleton sentinel objects for special Python values
Requires:       python3 >= 3.9

%description -n python3-sentinels
Sentinels provides named singleton objects for special Python values.

%prep
%autosetup -n sentinels-%{version}

%build
# The pinned sdist includes PKG-INFO for hatch-vcs version resolution.
# Wheel ZIP timestamps cannot precede 1980-01-01 UTC. Use a deterministic floor
# only for unset/earlier epochs; retain later caller-supplied epochs verbatim.
source_date_epoch=${SOURCE_DATE_EPOCH-0}
case "$source_date_epoch" in
  ''|*[!0-9]*)
    printf '%s\n' 'SOURCE_DATE_EPOCH must be a nonnegative decimal integer' >&2
    exit 1
    ;;
esac
# Strip leading zeroes only for comparison; avoid overflowing shell integers.
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
printf '%s\n' "Wheel build SOURCE_DATE_EPOCH=$SOURCE_DATE_EPOCH"
export PIP_NO_INDEX=1 PIP_DISABLE_PIP_VERSION_CHECK=1
%{__python3} -m pip wheel --no-build-isolation --no-deps --wheel-dir dist .

%install
export PIP_NO_INDEX=1 PIP_DISABLE_PIP_VERSION_CHECK=1
%{__python3} -m pip install --no-index --no-deps --ignore-installed --no-compile \
    --root %{buildroot} --prefix %{_prefix} dist/sentinels-%{version}-py3-none-any.whl

%check
# Preserve both commands from upstream ci.yml, without test filtering/skips.
# The module resolves __version__ from installed distribution metadata.
export PYTHONPATH=%{buildroot}%{python3_sitelib}:$PWD
%{__python3} -m pytest -v tests
%{__python3} -m pylint --rcfile=.pylintrc sentinels tests

%files -n python3-sentinels
%license LICENSE
%doc README.md
%{python3_sitelib}/sentinels/
%{python3_sitelib}/sentinels-%{version}.dist-info/

%changelog
* Fri Oct 09 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.1.1-1
- Onboard the verified official sdist with full upstream test and lint commands.
