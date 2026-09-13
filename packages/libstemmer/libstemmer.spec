# SPDX-License-Identifier: Apache-2.0
Name:           libstemmer
Version:        3.1.1
Release:        1%{?dist}
Summary:        Stemming library supporting many human languages
License:        BSD-3-Clause
URL:            https://snowballstem.org/
Source0:        libstemmer_c-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make

%description
libstemmer provides the Snowball stemming algorithms through a small C API.
Stemming maps inflected word forms to a common form for text search.

%package devel
Summary:        Development files for libstemmer
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Header and unversioned shared-library link for developing applications with
libstemmer.

%prep
%autosetup -p1 -n libstemmer_c-%{version}

%build
%make_build \
  CC=%{__cc} \
  CFLAGS="%{optflags} -fPIC" \
  CPPFLAGS="-Iinclude"
%{__cc} -shared %{build_ldflags} \
  -Wl,-soname,libstemmer.so.0 \
  -o libstemmer.so.0.0.0 \
  $(find libstemmer runtime src_c -type f -name '*.o' -print)
ln -s libstemmer.so.0.0.0 libstemmer.so.0
ln -s libstemmer.so.0 libstemmer.so

%install
install -Dpm0755 stemwords %{buildroot}%{_bindir}/stemwords
install -Dpm0755 libstemmer.so.0.0.0 %{buildroot}%{_libdir}/libstemmer.so.0.0.0
ln -s libstemmer.so.0.0.0 %{buildroot}%{_libdir}/libstemmer.so.0
ln -s libstemmer.so.0 %{buildroot}%{_libdir}/libstemmer.so
install -Dpm0644 include/libstemmer.h %{buildroot}%{_includedir}/libstemmer.h

%check
test "$(printf 'connections\n' | ./stemwords -l english)" = "connect"
cat > api-check.c <<'EOF'
#include <libstemmer.h>
#include <string.h>

int main(void) {
    struct sb_stemmer *stemmer = sb_stemmer_new("english", "UTF_8");
    const sb_symbol *word;
    int ok;
    if (stemmer == NULL)
        return 1;
    word = sb_stemmer_stem(stemmer, (const sb_symbol *)"connections", 11);
    ok = word != NULL && sb_stemmer_length(stemmer) == 7 &&
         memcmp(word, "connect", 7) == 0;
    sb_stemmer_delete(stemmer);
    return ok ? 0 : 2;
}
EOF
%{__cc} %{optflags} -Iinclude api-check.c -L. \
  -Wl,-rpath,"$PWD" -lstemmer -o api-check
./api-check

%files
%license COPYING
%doc NEWS README
%{_bindir}/stemwords
%{_libdir}/libstemmer.so.0*

%files devel
%license COPYING
%{_includedir}/libstemmer.h
%{_libdir}/libstemmer.so

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.1.1-1
- Initial openEuler RISC-V package from Fedora 44 and frozen cross-distribution evidence.
