# SPDX-License-Identifier: Apache-2.0
Name:           libabw
Version:        0.1.4
Release:        1%{?dist}
Summary:        AbiWord document import library and conversion tools
License:        MPL-2.0 AND GPL-3.0-or-later AND (GPL-2.0-or-later WITH Libtool-exception) AND FSFAP AND MIT AND X11
URL:            https://wiki.documentfoundation.org/DLP/Libraries/libabw
Source0:        libabw-0.1.4.tar.xz
Source1:        gpl-2.0.txt
Source2:        gpl-3.0.txt
Patch0:         0001-install-complete-generated-documentation.patch
BuildRequires:  bash
BuildRequires:  binutils
BuildRequires:  boost-devel
BuildRequires:  coreutils
BuildRequires:  diffutils
BuildRequires:  doxygen
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  glibc-devel
BuildRequires:  gperf
BuildRequires:  graphviz
BuildRequires:  grep
BuildRequires:  librevenge-devel
BuildRequires:  libxml2-devel
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  pkgconf-pkg-config
BuildRequires:  sed
BuildRequires:  tar
BuildRequires:  xz
BuildRequires:  zlib-devel
Requires:       bash
Requires:       coreutils
Requires:       grep

%description
An import library for AbiWord XML and compressed documents, with the original
text, HTML and raw conversion tools and generated API documentation.

%package devel
Summary:        Development headers for libabw
Requires:       %{name} = %{version}-%{release}

%description devel
Headers, linker symlink and pkg-config metadata for libabw.

%prep
%setup -q
# Preserve original bytes before the patch and configure helper refresh.
originals="$(find . -type f -printf '%%P\n' | LC_ALL=C sort)"
test "$(printf '%%s\n' "$originals" | wc -l)" -eq 97
mkdir license-notices
while IFS= read -r original; do
    mkdir -p "license-notices/$(dirname "$original")"
    cp -p -- "$original" "license-notices/$original.notice"
done <<EOF_ORIGINALS
$originals
EOF_ORIGINALS
cp -p %{SOURCE1} license-notices/GPL-2.0.txt
cp -p %{SOURCE2} license-notices/GPL-3.0.txt
(cd license-notices && find . -type f -print0 | LC_ALL=C sort -z | xargs -0 sha256sum) > notice-SHA256SUMS
test "$(wc -l < notice-SHA256SUMS)" -eq 99
mv notice-SHA256SUMS license-notices/SHA256SUMS
%autopatch -p1
# Keep paired input/output timestamps from triggering a needless autoreconf.
touch -r docs/doxygen/Makefile.in docs/doxygen/Makefile.am
cat > simple.abw <<'EOF_ABW'
<?xml version="1.0"?>
<abiword xmlns="http://www.abisource.com/awml.dtd"><section><p>libabw package streaming roundtrip</p></section></abiword>
EOF_ABW
cat > api-smoke.cpp <<'EOF_CPP'
// SPDX-License-Identifier: MIT
#include <cassert>
#include <cstdio>
#include <cstring>
#include <string>
#include <vector>
#include <libabw/libabw.h>
#include <librevenge-stream/librevenge-stream.h>
#include <librevenge-generators/librevenge-generators.h>
#include <zlib.h>
static bool supported(const std::string &bytes, bool moved = false)
{
    librevenge::RVNGStringStream input(
        reinterpret_cast<const unsigned char *>(bytes.data()), bytes.size());
    if (moved) assert(input.seek(3, librevenge::RVNG_SEEK_SET) == 0);
    return libabw::AbiDocument::isFileFormatSupported(&input);
}
static bool parse(const std::string &bytes, librevenge::RVNGString &text)
{
    librevenge::RVNGStringStream input(
        reinterpret_cast<const unsigned char *>(bytes.data()), bytes.size());
    librevenge::RVNGTextTextGenerator output(text, false);
    return libabw::AbiDocument::parse(&input, &output);
}
int main()
{
    const std::string xml =
        "<?xml version=\"1.0\"?><abiword xmlns=\"http://www.abisource.com/awml.dtd\">"
        "<section><p>libabw package streaming roundtrip</p></section></abiword>";
    librevenge::RVNGString empty;
    librevenge::RVNGTextTextGenerator output(empty, false);
    assert(!libabw::AbiDocument::isFileFormatSupported(nullptr));
    assert(!libabw::AbiDocument::parse(nullptr, &output));
    std::puts("PASS: null input rejected");
    assert(supported(xml, true));
    assert(supported("<abiword><section><p>plain</p></section></abiword>"));
    assert(supported("<awml xmlns=\"http://www.abisource.com/awml.dtd\"/>"));
    std::puts("PASS: recognized roots namespace and stream reset");
    assert(!supported("<notabiword/>"));
    assert(!supported("<abiword xmlns=\"urn:not-abiword\"/>"));
    std::puts("PASS: wrong root and namespace rejected");
    librevenge::RVNGString text;
    assert(parse(xml, text));
    assert(std::string(text.cstr()).find("libabw package streaming roundtrip") != std::string::npos);
    std::puts("PASS: plain XML streamed into text generator");
    z_stream stream{};
    assert(deflateInit2(&stream, Z_DEFAULT_COMPRESSION, Z_DEFLATED,
                        MAX_WBITS + 16, 8, Z_DEFAULT_STRATEGY) == Z_OK);
    std::vector<unsigned char> compressed(deflateBound(&stream, xml.size()));
    stream.next_in = reinterpret_cast<Bytef *>(const_cast<char *>(xml.data()));
    stream.avail_in = static_cast<uInt>(xml.size());
    stream.next_out = compressed.data();
    stream.avail_out = static_cast<uInt>(compressed.size());
    assert(deflate(&stream, Z_FINISH) == Z_STREAM_END);
    const std::string gzip(reinterpret_cast<const char *>(compressed.data()), stream.total_out);
    assert(deflateEnd(&stream) == Z_OK);
    librevenge::RVNGString gzip_text;
    assert(supported(gzip) && parse(gzip, gzip_text));
    assert(std::string(gzip_text.cstr()) == std::string(text.cstr()));
    std::puts("PASS: gzip document produces identical text");
    librevenge::RVNGString bad;
    // The original reader enables XML_PARSE_RECOVER. Do not assume every
    // truncated document fails; this input has no recoverable element at all.
    assert(!parse("<", bad));
    std::puts("PASS: invalid XML opener rejected");
    return 0;
}
EOF_CPP

%build
# Original Unix defaults: shared yes, static no, tools yes, docs yes, fuzzers no.
%configure
%make_build

g++ %{optflags} -UNDEBUG -Iinc \
    $(pkg-config --cflags librevenge-0.0 librevenge-stream-0.0 librevenge-generators-0.0) \
    api-smoke.cpp -Lsrc/lib/.libs -labw-0.1 \
    $(pkg-config --libs librevenge-0.0 librevenge-stream-0.0 librevenge-generators-0.0) \
    -lz -o api-smoke

%check
(cd license-notices && sha256sum -c SHA256SUMS)
# Original check target registers zero runtime cases; retain it unchanged.
%make_build check
LD_LIBRARY_PATH="$PWD/src/lib/.libs" ./api-smoke > api-result.log
cat api-result.log
test "$(grep -c '^PASS:' api-result.log)" -eq 6
LD_LIBRARY_PATH="$PWD/src/lib/.libs" src/conv/text/.libs/abw2text simple.abw > cli-result.txt
grep -F 'libabw package streaming roundtrip' cli-result.txt
test -s docs/doxygen/html/index.html
# RPM install-post has already stripped the installed helper by this stage.
(cd %{buildroot}%{_libexecdir}/libabw-tests && sha256sum api-smoke api-smoke.cpp simple.abw > SHA256SUMS)

%install
%make_install
rm -f %{buildroot}%{_libdir}/libabw-0.1.la
install -D -m 0755 api-smoke %{buildroot}%{_libexecdir}/libabw-tests/api-smoke
install -m 0644 api-smoke.cpp simple.abw %{buildroot}%{_libexecdir}/libabw-tests/

%files
%license COPYING.MPL license-notices
%doc README NEWS CREDITS
%{_libdir}/libabw-0.1.so.1*
%{_bindir}/abw2text
%{_bindir}/abw2html
%{_bindir}/abw2raw
%{_libexecdir}/libabw-tests
%{_docdir}/libabw/html

%files devel
%{_includedir}/libabw-0.1
%{_libdir}/libabw-0.1.so
%{_libdir}/pkgconfig/libabw-0.1.pc

%changelog
* Sat Oct 24 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.1.4-1
- Package the fixed official release with original defaults and strict replay.
