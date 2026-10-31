# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 openEuler RISC-V package contributors
# Licensed under the Apache License, Version 2.0; full text is Source2.
# https://www.apache.org/licenses/LICENSE-2.0
# Distributed AS IS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND.
Name:           libnghttp3
Version:        1.18.0
Release:        1%{?dist}
Summary:        HTTP/3 and QPACK library written in C
License:        MIT AND GPL-3.0-or-later AND X11 AND LicenseRef-Portable-Snippets-CC0-Waiver AND Apache-2.0
URL:            https://nghttp2.org/nghttp3/
Source0:        https://github.com/ngtcp2/nghttp3/releases/download/v%{version}/nghttp3-%{version}.tar.gz
Source1:        https://www.gnu.org/licenses/gpl-3.0.txt#/GPL-3.0.txt
Source2:        https://www.apache.org/licenses/LICENSE-2.0.txt#/Apache-2.0.txt
BuildRequires:  bash
BuildRequires:  binutils
BuildRequires:  cmake >= 3.20
BuildRequires:  coreutils
BuildRequires:  diffutils
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  glibc-devel
BuildRequires:  gnupg2
BuildRequires:  grep
BuildRequires:  gzip
BuildRequires:  make
BuildRequires:  pkgconf-pkg-config
BuildRequires:  python3
BuildRequires:  tar
Requires:       bash
Requires:       binutils
Requires:       coreutils
Requires:       diffutils
Requires:       gcc
Requires:       glibc-devel
Requires:       grep
Requires:       pkgconf-pkg-config
Requires:       python3

%description
nghttp3 implements HTTP/3 and QPACK independently of a QUIC transport.
This single SDK package retains upstream shared and static libraries,
public headers, pkg-config and CMake exports. Original examples are built.
Installed QA compiles consumers; it does not establish network interoperability.
The compiled library is MIT licensed. Additional license terms inventory
bundled build/test helpers and downstream packaging, not a GPL library claim.

%prep
%setup -q -n nghttp3-%{version}
test ! -e packaging-qa
test ! -e packaging-notices
mkdir packaging-qa packaging-notices
cat > packaging-qa/original.sha256 <<'ORIGINAL_SHA256'
b6f7c5345d9b294a9fd3d8aee84afcef4ff68f6a96be51e18a7aba189a4a71a9  AUTHORS
cf1a74de7623724c1309438bc4919bda86a45d6b1698b0c28e51d12c326d8a35  CMakeLists.txt
b4b16ac7e8230f560294277744babd782b7dbe62339f8ea15b19f7add532d990  CMakeOptions.txt
58cc3fc8c6d6cb2485ab35eb5918e849b5bf1e56522974e106d7a39a88d61dcd  COPYING
2619ce951c847102e10818419d3b0a3996df393655e700a7f18d659eb0e5b1fc  ChangeLog
edebc46c7d07258a20170050d9595ce4e630f5d584a4eb00220bb90c8997a31b  INSTALL
8934fa66f9f257b795b48b6f33bdf271e09a97cf2bb044bea7448266d52c8678  Makefile.am
cdd89467137c6b4d0d7550c3a59f138cacf2c4e876fbbbf7d0eee88294f06ac5  Makefile.in
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  NEWS
f3c22082da5ff8b5313d36e2b8a1a83d28ff1d379a9dfd3f18582ce933b9159c  README
8dbe7d64bd7b70dded18965ce117240d90b68ff00713acb9344466884582e41a  README.rst
ff97aebff01e4e3c090ad4d03c5cf23b8a8d2d117029dc064646aae83c8a3e51  aclocal.m4
0b771050a00413ee596f4a2fe2f04244c57343a16d5566fa08bcbc8e2c3fe3e2  cmake/PickyWarningsC.cmake
9f90b6bb7eeb478ccc7ba365f9659fb9389713805bb9b9264f009118037ff1d9  cmake/PickyWarningsCXX.cmake
f6c4cf4eea346e01a2456d749b543d5be161f5f5706763c7c8ea641ada3afd19  cmake/Version.cmake
76e8d915234fe31c8b054a26f224b828464cebd6d1ba87a9a6670050fee4f093  cmakeconfig.h.in
c207b390aac6323062b982214a6c63448e53e6911107993abe96f35fe7a30a18  compile
cf610daf8afdedbf2110abd79bdd4121d59080cab5ec46deaf67f97273bb6bda  config.guess
528ac9273d1e684a86006e4803686994d6e3f5a023a0d28ae0e04d7e5da30969  config.h.in
deb02c26f43b2ea64276c9ede77ec0f53d08e6256710f3c0a12275712085c348  config.sub
8e0d2b6813e30b16016f79c61245d1ab32f44f6c2426195f1610395b8797d279  configure
5eacda86f252f3e9e467b50e678ca4702f62589a6de2d69ab479a6c26e3afbea  configure.ac
e44b49f71b265788187993090027193a6cd2b4718f9aa7be34412f537bce6873  depcomp
e45ef243b36a99fd7c949d447d1c2df47e85c4319be9f1b281db13113936d976  doc/Makefile.am
4f6508c966e693e961678644fcff480d8ef07a242e70ea1400129b792573a46f  doc/Makefile.in
2df707f4b612ced15b4d445c2f85f907d2f5f96ab404da58ebcaa73e28fcadbb  doc/source/conf.py.in
4b5085e5c631dc0fe3d3daa440a68627928bc10dad0de73ac665aff7b7d0ae31  examples/CMakeLists.txt
ffefb2d9091dbc6ed47b6983521d5df4d8446c94b749d6eb200915cede93f2b6  examples/Makefile.am
f0463d6a7e20a83099fe3a18809b37b92eb03d095508b036201f3278b560ed37  examples/Makefile.in
9993a7efeda7badae15219b0480c5b26d0ae7598572b303a70620bb883c3cefa  examples/qpack.cc
e3b58ad87a83adc3ff8eaa076a073e88ce6ae0d4d438b06592fae2fc2f968e0d  examples/qpack.h
820da93f26b7d40a3ab252e50c6298678dd712b8f74def66e7e65d636ac3976a  examples/qpack_decode.cc
10ca6d1bfb303e3e61570ecc3dbc722dc053cecbc16d2b8cc4c16c2fc70ef1ba  examples/qpack_decode.h
3fc2028d927ca333afe72e01953467bb54d3d1d090bc9786ce67ace692747f5d  examples/qpack_encode.cc
44f237544036eba496f6af92e88a9e8aae841c99ef7326b758bb54629237c98e  examples/qpack_encode.h
a705e50b10b373489d41f5026452be580caa3818f7d833df6a76fa881bf62005  examples/template.h
86a530ec1a285c4db5f4cebc8d8c7a5779f6785d6c08fc90772b164a948ede3f  examples/util.cc
d6de9ae7c13c2f1522d06b80002c4b97982c73723dfa1b55566b7c616936eb11  examples/util.h
3d7488bebd0cfc9b5c440c55d5b44f1c6e2e3d3e19894821bae4a27f9307f1d2  install-sh
c2dd64a1fc218521d36c4234a73f4d9ff078e9ea71da1e7791e97617422e6f72  lib/CMakeLists.txt
92a332f2c5aeeaff027b8a68402c7825eaadaa463e2eb3cc82cdd740c7e28dfd  lib/Makefile.am
adaff81f1de0891a5d63b716f0c4e09cc5b2f69df6195f97410ac8ee4ee84c89  lib/Makefile.in
4d5af5e901a515470fb7e403b7abdd8852f8997dfda407683b60a481f3c1b3f0  lib/config.cmake.in
e101d08562b1d78cb7b9b8a0c28c11a0971653459992617536b7b99b7f892597  lib/includes/CMakeLists.txt
76052a92cb3b778b9afc953dcebb57d32ad1cb9e0507508cbd1b6ba7b2beb6d9  lib/includes/Makefile.am
6d09d251dfece5e5f1c0ad553dde033c2828bd8f47682a41c57d551f9b030bca  lib/includes/Makefile.in
4cf23df44bb91cda59eb72bd7e13a24eb9388cab8acc0b8e74cd85f2a2a5c72a  lib/includes/nghttp3/nghttp3.h
e38cfa0c119426eba8267dfb0ec2f7c3e1e89c18c3c2ca2e6757e3d7a0510491  lib/includes/nghttp3/version.h
c397818c75087a2f796457629956cddf653fdd994f3b4253256b86e082334467  lib/includes/nghttp3/version.h.in
49b441c7a5cae8a554f93cd0e41e3a24fe7fd88810d1e44dcba3d10ef0f16ba9  lib/libnghttp3.pc.in
068e663b6a48c6b66743b715260985759640a5748ac7332ea9065bb2e4ed6d51  lib/nghttp3_balloc.c
8379399d379e76300e9128b3ecd484e83ca07589deda1bbe91eca6f18f12693b  lib/nghttp3_balloc.h
39ef86ae73532cff8b843a160f54be6517db03fa783ec58cd2c683d941acfde9  lib/nghttp3_buf.c
1336e3c71945dca7a8f04103175a16e9247e66f8cd488750c0e175d7c18df125  lib/nghttp3_buf.h
f0b81a238af8c01600ecc4342e5cc01e78c8aa07d84cf4816b8e6140f37d71ef  lib/nghttp3_callbacks.c
b54dafa86e5b951b5757836bfbe16a56e1ef031c582f891033198d099939f986  lib/nghttp3_callbacks.h
332de5870a6bc8862a261b45add6ccf756c95597114ab78711251014006b01a1  lib/nghttp3_conn.c
9834a7ea77cfe4f2df51ce88c06c23ab71717bf96b5e75277afc7b608367732b  lib/nghttp3_conn.h
c4db10fa1f345091575feed39f88dd1c2c44c5b5b357e27bfdb807dd4275d7f6  lib/nghttp3_conv.c
ba1061635e6a6821416f1332a44dd3e6459e34aaa3f9a17f867a1d82859a235b  lib/nghttp3_conv.h
4556bd7bf54e08f28f1c4e27e95b9abb0ec1d411e2726e0e6b833070ba1edcae  lib/nghttp3_debug.c
65d8da2a15ea16bd93555db18dacfcbed247e2de2de7968af433efb6fc36564e  lib/nghttp3_debug.h
0400686eb8c1683c58caad9645f20e9e35f9e0f7301c1355b477b23764329520  lib/nghttp3_err.c
245f91d219212018ca58fde31e3317b41999ca8d952d1031d245f7dfc537a0ad  lib/nghttp3_err.h
973e9d78c20fea7d1c31cdf815cf27f069f213e8635bb3300216b14b606416d9  lib/nghttp3_frame.c
0deca600b11d1b8201927dc795d57c5c56270b9abff277e9c46cf02c7b141e10  lib/nghttp3_frame.h
210e3e88adc2cc79bc4df7b794e8006e873c2190067acfef4b7a626ec47e9ba1  lib/nghttp3_gaptr.c
1416dafc0606e167e4cf7e65b344cf577fe8e442019060c21fd16fac288db779  lib/nghttp3_gaptr.h
4a4c49d0e03dc3e0a8f1cf48f2e021c576ea80c8a3b8f26f634d913315ec625e  lib/nghttp3_http.c
8bf7fee31cd245832b0bef25a5d425412924b4603d0413319265535f569af61e  lib/nghttp3_http.h
f6c83e3be22d756ee7b94f89790375c13358dbad76d9e86b56c19faad9352121  lib/nghttp3_idtr.c
0e052faf43f43ff3e2fe7d11c5446949f505a90f92db9cc3f8ad9945a9e59ecb  lib/nghttp3_idtr.h
2373231218c3f15912e5eee475c3f21a02b911740251b366331af334db6b8cb3  lib/nghttp3_ksl.c
7cb7b8ad5200035ec98f3d12b00b49de6d569b098bf56b730feaa148670424ba  lib/nghttp3_ksl.h
ff097ddd8448e7858b192f259e30d3a1fdc1f43cdb95f8bcbb1fd746bcc12366  lib/nghttp3_macro.h
2b65525852dd5a0781bd07b6b012f8ee2355e091642a8f26c17ac1093e3d8ce6  lib/nghttp3_map.c
c1b3fbad5a33196a23292a79c5b739b6469a73aceca46000d78d089689e95595  lib/nghttp3_map.h
3f4f76d940ba44f33801dd371e89527b5a7d8485c5f0c2ab5d748a3a996dc2ea  lib/nghttp3_mem.c
e453fa1bda766af58c2f09c82ec73d0f437e9ce79d3952e34d09243f961da1f3  lib/nghttp3_mem.h
8cc3c6fc09394b799336bc30e563c185e5711526e8a74ebece7461de3bbb8c88  lib/nghttp3_objalloc.c
43b079bf720bc242f5f8c78c7e3563cd91ad76c5a062b44cdc663998e3390884  lib/nghttp3_objalloc.h
388f7981a9bfc7b73cd335326a14bfa4d33e622b3e8e071f568392aa1811922c  lib/nghttp3_opl.c
267acd7a7d03604bf88981ddb3ebd1b2107d146a785bb236a489dce5c44f8465  lib/nghttp3_opl.h
49404d6b8e8a73d95ffda2a325d66dfc32d980faf43daaef2dd21b6bd9d76411  lib/nghttp3_pq.c
012d49ec466f54cd64ec38f5c0684be7fbc0db470df8a6c0d7e52a82580cae61  lib/nghttp3_pq.h
097688816b0615d1662572b784b62b83da09fa7246bc262781c8eb494cfa3d25  lib/nghttp3_qpack.c
d81de76bd31ee35bc64a6ea856126155bb145881864309f8ccf5688cd53465bd  lib/nghttp3_qpack.h
4563b2b54036122db8ab57d1a8cfdd0386f9890e47f0ef754c88f2b433ef7f43  lib/nghttp3_qpack_huffman.c
7f91b5e7c6caa0b11879f8701e53fd7e25b4227926ab948acdfa8a89088aa641  lib/nghttp3_qpack_huffman.h
55e1e8ac9ea15b482cb2d5a8d835ead8cdb7cd06b7e191429ba04b4046921ed0  lib/nghttp3_qpack_huffman_data.c
06a4d9464f84dadf86662d42a5800cad0a7322bbd3f3c4cc3a380648625acd72  lib/nghttp3_range.c
6a8298780d5b9ba6c61a71346d641eefea932f674a3372a06827ca0ca7ac4979  lib/nghttp3_range.h
7afeb7f320cec9e848bab418b78e6acb73a7d4210a145b0a6bccbf075b23216b  lib/nghttp3_ratelim.c
c95030bb42818dfcc5626f673cdb6acb8548c3d61bc3f2fbbecdedaf5e511377  lib/nghttp3_ratelim.h
6bac705f68ab813c4d2b149de0a5581999be316955280c6dd4ae3e83d75e6d9e  lib/nghttp3_rcbuf.c
189b1e1a578230598f1700e6ce08300f575edc42059989677669c52fa38a0b9a  lib/nghttp3_rcbuf.h
de456a4dcef5479c437025d267d0e43f94f29f09f69572b9c77cdd489ef0316b  lib/nghttp3_ringbuf.c
8dd504e3867e724a2652b98f03cd999cc9be0999513a9fe8d0a24dea2e3ac1dc  lib/nghttp3_ringbuf.h
d6b8c91338dba5ff210d6aaf440d972285057111b6f423aa8c62670fce4afbe9  lib/nghttp3_settings.c
47e5ca6b9462c3ace43688be11eea8fed9638a3859eb4734eadc92fc2f23ca78  lib/nghttp3_settings.h
0308581640626a30c3fe434d08bdd548def920712532436f9ff33e1dc1028dd1  lib/nghttp3_str.c
8ab3db3acc983055b5d81b965d81af5da6b8db0c89dd477fdf499bb381a2a91c  lib/nghttp3_str.h
eb53a6ef1414a1e22b052e0e09c7f5132a3b0a180b7f9fbceb0e52a4601277f7  lib/nghttp3_stream.c
28b0b7a70bf91a6bf8c4f55aa3f409e5a8dca1790bd61679996ef57ed081cc8c  lib/nghttp3_stream.h
2b7e77ca037e746238f2a44cebb72dab679ec5a848066735ee15b928f115c9b3  lib/nghttp3_tnode.c
b7e1496e4c04fb3e71e5871469ad367875d3307822301632240e366cce602d96  lib/nghttp3_tnode.h
8630a37d531ad613d8b6cec1c424c39ed61e318f2ed78a1dba37fea901690ce9  lib/nghttp3_unreachable.c
2753dee192f41f265bcd81aba01ce84a8588d10f02806033dc8cfca466488c5b  lib/nghttp3_unreachable.h
eb4a232045ffa53340ada8be6d1f8adc184301ecc66dc925500dbfe815f60282  lib/nghttp3_vec.c
c2a1d3b323b0d41cbd6f9e27538e253550893c709e5ae3d1212fb800719268a7  lib/nghttp3_vec.h
95870bf0d35dffc4b841696f0dcd0546d378238db1dee8ca99f50d5292f16e9f  lib/nghttp3_version.c
cd6d5feeacf9406fe915d3c23b85a6bf86deecfa1661396b63d2d2188b90beda  lib/sfparse/COPYING
90c8f4627a0cf41d421bf2b186d9c9061f5087b23c8015021853788fc529d4c7  lib/sfparse/sfparse.c
fa99f26ea080137b0f79c3f8799e7513aa1a97fb4c9a4fb1cc42869c17bfac5d  lib/sfparse/sfparse.h
579a1445e6a9a8b0809a44aa9f908387d4a43a2a440c9b84ea979f2b4f17816c  ltmain.sh
75f03045fde15ef1e901f17246812fcc751c1a5b070f7f88d482ef336435da87  m4/ax_check_compile_flag.m4
be43ad785f2ef13bc929e45684faf5bbc5c2f4bf778155a27c216e5dbb03e5b3  m4/ax_cxx_compile_stdcxx.m4
38a99c1d5072c1e0e1f45da415d39143d529b1052b73a60477e1bd6badf7e99f  m4/libtool.m4
f3d4ed0426501308028dd7690cf343cb280479d637a2ebee6c289ec2e708df3b  m4/ltoptions.m4
0896f153a5a40546566028a4272642ae291532f3e65c25fcae950c8812b8c265  m4/ltsugar.m4
2a6baf40b64f34234e0b76c7ff62b01a1f6bbf60089f4f74506b49f800ffaf9e  m4/ltversion.m4
8533006830e1ea9625fc5e4c060e653eedf9d5464a9b2f5f494244ee272e2e2f  m4/lt~obsolete.m4
a9865db4f39574ff128c0312c367f070d20f81847817021ecce95fd70a610c9d  missing
08ff8986c3a0ce8bf32d25ec7e4752ffbce9c89589f018836c97a08b6573ac2c  test-driver
215aaf2770745d059926f1ff6d961004ee12643674f3182923bd8e906918d4d2  tests/CMakeLists.txt
25918569d7e7e09991c1cea53a75775402e0db6c803e5b2dc7f09f9c7fed08de  tests/Makefile.am
6fc0227cf20d844a1e1cd5c57b1b8305515e3125150633e39eb62ea93e5dbfd5  tests/Makefile.in
94e3097b700b386fd2c177159c244e7d76cf508ab85b5de4f00b92c25a47cc73  tests/main.c
551a04ab9278e48e3d4ef8b0381ad54e54e84fac1a225c50247fa3669dfdef75  tests/munit/COPYING
6e3cbde845a9201640bfb9f756164169d249adc7f243e5a594c80e24d1cde8c4  tests/munit/munit.c
e46806c645f12710b1b5f3db40998d5d4446ddff40d55817ebd45935a61e54f3  tests/munit/munit.h
6462427a7e9b7a7acbd8a47ca1c7e1ce23c7ddf1d4d15b0c8f8243a2f737caaa  tests/nghttp3_callbacks_test.c
051394188feeb2113e0e578284bb83c9c7aeae834f697b433e34a3ccd86adc8c  tests/nghttp3_callbacks_test.h
5519cd0caa2636a5f0537e948ca86cbe4a46a27d81637bbef2d34653615f0c43  tests/nghttp3_conn_test.c
c6a27dd24e7505a4e32a7b9bd790d0965fed1e4f5f90b014402f15c027e6cf77  tests/nghttp3_conn_test.h
7e64edd261229580dc2a943a974ce8ecfee02679ce8dee46fbd19d6e28b46019  tests/nghttp3_conv_test.c
d09b80d51ae39104e781e96c0c8af65555457b041871f9948c97a87066889595  tests/nghttp3_conv_test.h
00dddfc020e1ed7798311c78eec4e5a44072c19c935be01e413a3e2a0a93a917  tests/nghttp3_http_test.c
82374510d78efc8258fcadcc13a95ac28ff3bfa8da342b1b0ebf43f0973b87d6  tests/nghttp3_http_test.h
a97f3f7028480015892c3e572369221de54562604eea2c338401a93463ac9a66  tests/nghttp3_qpack_test.c
9712b7a1e1d9dd22f64033774f4c424fc80efebf561124b5530a882d25104418  tests/nghttp3_qpack_test.h
71d54d3f650bc843b0943291463f56714cf4859b3754ceb448ac6123d28a8207  tests/nghttp3_settings_test.c
98a1e4d316909a9d6e0123c615b30fac805bca5c692639862ae17d9e18b5d0b7  tests/nghttp3_settings_test.h
799853423e288b21799bad6730f98538f625d401f03b094f5f5f1667a4142def  tests/nghttp3_str_test.c
3e14c0c0acde3b58e8f3a29168343e9610b5493d8e0570a14a039a7ec2a30120  tests/nghttp3_str_test.h
2005b0b6d9659f62724c8742e214882b7a25d850b2589fff949320262dba795f  tests/nghttp3_stream_test.c
ea2a2316ec76ad8772be2b560b9bbfa4efdd544a5cc45ca34d235b57931e27c0  tests/nghttp3_stream_test.h
72b6578d6a0fc02ae33440b4419c8a8e29d23d7a5a0f4dfb4d959a6ec64a7f8e  tests/nghttp3_test_helper.c
ec5ae5c61db13697cea65e5863ca01e7bffd0d1e8aac32071e054580de807987  tests/nghttp3_test_helper.h
2577f82c14d296a68049a9f848f86f7fbb838312a8be254dc89cf55e47cbe930  tests/nghttp3_tnode_test.c
c43c760ad1702b5de207a8e8c0f879c1cee2742b6a8fed43bf53d9fd83dd3931  tests/nghttp3_tnode_test.h
ORIGINAL_SHA256
sha256sum -c packaging-qa/original.sha256
while read -r digest file; do
    mkdir -p "packaging-notices/$(dirname "$file")"
    cp -p "$file" "packaging-notices/$file.notice"
    printf '%%s  %%s.notice
' "$digest" "$file"
done < packaging-qa/original.sha256 > packaging-notices/SHA256SUMS
(cd packaging-notices; sha256sum -c SHA256SUMS)
test "$(wc -l < packaging-notices/SHA256SUMS)" -eq 151
cat > packaging-qa/consumer.c <<'CONSUMER_C'
/* SPDX-License-Identifier: Apache-2.0
 * Copyright 2026 openEuler RISC-V package contributors
 * Licensed under the Apache License, Version 2.0. You may obtain a copy at
 * https://www.apache.org/licenses/LICENSE-2.0
 * Unless required by applicable law or agreed to in writing, software is
 * distributed on an AS IS BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND.
 * See the License for permissions and limitations. Full text ships in package.
 */
#include <nghttp3/nghttp3.h>
#include <nghttp3/version.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#ifdef NDEBUG
#error Packaging consumer must not be built with NDEBUG
#endif
#define REQUIRE(x) do { if (!(x)) { fprintf(stderr, "failed line %%d: %%s\n", __LINE__, #x); return 1; } } while (0)

int main(void) {
  const nghttp3_info *info = nghttp3_version(0);
  const uint8_t binary[] = {0, 0x80, 0xff, 'x'};
  nghttp3_vec vec[] = {{(uint8_t *)binary, 3}, {(uint8_t *)binary + 3, 1}};
  uint8_t encoded[8], expected[8];
  uint64_t decoded;
  static const struct { uint64_t n; size_t len; } numbers[] = {
    {0, 1}, {63, 1}, {64, 2}, {16383, 2}, {16384, 4},
    {1073741823, 4}, {1073741824, 8}, {UINT64_C(4611686018427387903), 8}
  };
  REQUIRE(info && info->version_num == 0x011200 && NGHTTP3_VERSION_NUM == 0x011200);
  REQUIRE(strcmp(info->version_str, "1.18.0") == 0);
  REQUIRE(nghttp3_version(0x011200) == info && nghttp3_version(0x011201) == NULL);
  puts("libnghttp3 case01 version: PASS");
  REQUIRE(strcmp(nghttp3_strerror(NGHTTP3_ERR_INVALID_ARGUMENT), "ERR_INVALID_ARGUMENT") == 0);
  REQUIRE(strcmp(nghttp3_strerror(0), "(unknown)") == 0);
  REQUIRE(!nghttp3_err_is_fatal(NGHTTP3_ERR_INVALID_ARGUMENT));
  REQUIRE(nghttp3_err_is_fatal(NGHTTP3_ERR_NOMEM));
  REQUIRE(nghttp3_err_infer_quic_app_error_code(0) == NGHTTP3_H3_NO_ERROR);
  REQUIRE(nghttp3_err_infer_quic_app_error_code(NGHTTP3_ERR_QPACK_DECOMPRESSION_FAILED) == NGHTTP3_QPACK_DECOMPRESSION_FAILED);
  puts("libnghttp3 case02 errors: PASS");
  REQUIRE(nghttp3_vec_len(vec, 2) == 4 && nghttp3_vec_len(vec, 0) == 0);
  REQUIRE(memcmp(binary, "\0\200\377x", sizeof(binary)) == 0);
  puts("libnghttp3 case03 binary-vectors: PASS");
  REQUIRE(nghttp3_check_header_name((const uint8_t *)"content-type", 12));
  REQUIRE(nghttp3_check_header_name((const uint8_t *)":method", 7));
  REQUIRE(!nghttp3_check_header_name((const uint8_t *)"Content-Type", 12));
  REQUIRE(!nghttp3_check_header_name((const uint8_t *)"a b", 3));
  REQUIRE(!nghttp3_check_header_name((const uint8_t *)":", 1));
  REQUIRE(!nghttp3_check_header_name(binary, 0));
  puts("libnghttp3 case04 header-names: PASS");
  REQUIRE(nghttp3_check_header_value((const uint8_t *)"ok\tvalue", 8));
  REQUIRE(nghttp3_check_header_value(binary + 1, 2));
  REQUIRE(nghttp3_check_header_value(binary, 0));
  REQUIRE(!nghttp3_check_header_value((const uint8_t *)" leading", 8));
  REQUIRE(!nghttp3_check_header_value((const uint8_t *)"tail ", 5));
  REQUIRE(!nghttp3_check_header_value((const uint8_t *)"a\r\nb", 4));
  REQUIRE(!nghttp3_check_header_value(binary, 4));
  puts("libnghttp3 case05 header-values: PASS");
  for (size_t i = 0; i < sizeof(numbers) / sizeof(numbers[0]); ++i) {
    memset(encoded, 0xa5, sizeof(encoded));
    REQUIRE(nghttp3_put_uvarintlen(numbers[i].n) == numbers[i].len);
    REQUIRE(nghttp3_put_uvarint(encoded, numbers[i].n) == encoded + numbers[i].len);
    REQUIRE(nghttp3_get_uvarintlen(encoded) == numbers[i].len);
    REQUIRE(nghttp3_get_uvarint(&decoded, encoded) == encoded + numbers[i].len);
    REQUIRE(decoded == numbers[i].n);
    for (size_t j = numbers[i].len; j < sizeof(encoded); ++j) REQUIRE(encoded[j] == 0xa5);
  }
  memset(expected, 0xff, sizeof(expected));
  REQUIRE(memcmp(encoded, expected, sizeof(encoded)) == 0);
  puts("libnghttp3 case06 varint-boundaries: PASS");
  puts("libnghttp3 strict public API: 6 cases PASS");
  return 0;
}
CONSUMER_C
cat > packaging-qa/run-qa.sh <<'RUN_QA'
#!/usr/bin/bash
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 openEuler RISC-V package contributors
# Licensed under the Apache License, Version 2.0; full text ships in package.
# https://www.apache.org/licenses/LICENSE-2.0
# Distributed AS IS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND.
set -euo pipefail
export LC_ALL=C LANG=C PATH=/usr/bin:/bin
unset LD_LIBRARY_PATH LD_PRELOAD LD_AUDIT
test "$#" -eq 5
mode=$1
include=$2
shared=$(readlink -f "$3")
archive=$(readlink -f "$4")
qa=$(readlink -f "$5")
test "$mode" = build || test "$mode" = installed
test -f "$include/nghttp3/nghttp3.h" && test -f "$include/nghttp3/version.h"
test -f "$shared" && test -f "$archive" && test -f "$qa/consumer.c"
work=$(mktemp -d /tmp/libnghttp3-qa.XXXXXXXX)
finish() {
    status=$?
    trap - EXIT
    set +e
    for raw in "$work"/*.stdout "$work"/*.stderr "$work"/*.map "$work"/*.sha256 "$work"/*.json "$work"/*.txt; do
        test -f "$raw" || continue
        printf '\nNGHTTP3_QA_RAW_BEGIN %%s\n' "${raw##*/}" || status=1
        sha256sum "$raw" || status=1
        cat "$raw" || status=1
        printf '\nNGHTTP3_QA_RAW_END %%s\n' "${raw##*/}" || status=1
    done
    exit "$status"
}
trap finish EXIT
printf '%%s\n' "$mode" "$include" "$shared" "$archive" "$qa" "$work" > "$work/inputs.txt"
sha256sum "$shared" "$archive" "$include/nghttp3/nghttp3.h" "$include/nghttp3/version.h" "$qa/consumer.c" "$qa/run-qa.sh" "$qa/expected.stdout" > "$work/inputs-before.sha256"
flags=(-std=c11 -O2 -Wall -Wextra -Werror -UNDEBUG -I"$include")
libs=("$shared")
if test "$mode" = installed; then
    test "$include/nghttp3/nghttp3.h" -ef /usr/include/nghttp3/nghttp3.h
    test "$include/nghttp3/version.h" -ef /usr/include/nghttp3/version.h
    test "$shared" -ef /usr/lib64/libnghttp3.so.9.9.0
    test "$archive" -ef /usr/lib64/libnghttp3.a
    (cd /; sha256sum -c "$qa/SHA256SUMS") > "$work/installed-manifest-before.stdout" 2> "$work/installed-manifest-before.stderr"
    test ! -s "$work/installed-manifest-before.stderr"
    pkg-config --modversion libnghttp3 > "$work/pkg-version.stdout" 2> "$work/pkg-version.stderr"
    printf '1.18.0\n' > "$work/pkg-version-expected.txt"
    cmp "$work/pkg-version-expected.txt" "$work/pkg-version.stdout"
    test ! -s "$work/pkg-version.stderr"
    pkg-config --cflags libnghttp3 > "$work/pkg-cflags.stdout" 2> "$work/pkg-cflags.stderr"
    pkg-config --libs libnghttp3 > "$work/pkg-libs.stdout" 2> "$work/pkg-libs.stderr"
    test ! -s "$work/pkg-cflags.stderr" && test ! -s "$work/pkg-libs.stderr"
    read -r -a pcflags < "$work/pkg-cflags.stdout" || test ! -s "$work/pkg-cflags.stdout"
    read -r -a libs < "$work/pkg-libs.stdout"
    flags=(-std=c11 -O2 -Wall -Wextra -Werror -UNDEBUG "${pcflags[@]}")
fi
set +e
gcc "${flags[@]}" "$qa/consumer.c" -o "$work/negative" > "$work/negative.stdout" 2> "$work/negative.stderr"
negative_status=$?
set -e
printf '%%s\n' "$negative_status" > "$work/negative-status.txt"
test "$negative_status" -ne 0 && test ! -e "$work/negative" && test ! -s "$work/negative.stdout"
grep -Eq 'undefined reference.*nghttp3_(version|put_uvarint)' "$work/negative.stderr"
gcc "${flags[@]}" "$qa/consumer.c" "${libs[@]}" -Wl,-t,-Map,"$work/shared.map" -o "$work/shared-consumer" > "$work/shared-link.stdout" 2> "$work/shared-link.stderr"
test ! -s "$work/shared-link.stderr"
gcc "${flags[@]}" "$qa/consumer.c" "$archive" -Wl,-t,-Map,"$work/static.map" -o "$work/static-consumer" > "$work/static-link.stdout" 2> "$work/static-link.stderr"
test ! -s "$work/static-link.stderr"
for kind in shared static; do
    readelf -h "$work/$kind-consumer" > "$work/$kind-elf.stdout" 2> "$work/$kind-elf.stderr"
    readelf -d "$work/$kind-consumer" > "$work/$kind-dynamic.stdout" 2> "$work/$kind-dynamic.stderr"
    test ! -s "$work/$kind-elf.stderr" && test ! -s "$work/$kind-dynamic.stderr"
    grep -Eq 'Class:[[:space:]]+ELF64' "$work/$kind-elf.stdout"
    grep -Eq 'Machine:[[:space:]]+RISC-V' "$work/$kind-elf.stdout"
    if grep -Eq '\((RPATH|RUNPATH)\)' "$work/$kind-dynamic.stdout"; then exit 1; else test "$?" -eq 1; fi
done
grep -Fq 'Shared library: [libnghttp3.so.9]' "$work/shared-dynamic.stdout"
if grep -Fq 'Shared library: [libnghttp3.so' "$work/static-dynamic.stdout"; then exit 1; else test "$?" -eq 1; fi
readelf -h "$shared" > "$work/library-elf.stdout" 2> "$work/library-elf.stderr"
readelf -d "$shared" > "$work/library-dynamic.stdout" 2> "$work/library-dynamic.stderr"
test ! -s "$work/library-elf.stderr" && test ! -s "$work/library-dynamic.stderr"
grep -Eq 'Class:[[:space:]]+ELF64' "$work/library-elf.stdout"
grep -Eq 'Machine:[[:space:]]+RISC-V' "$work/library-elf.stdout"
grep -Fq 'Library soname: [libnghttp3.so.9]' "$work/library-dynamic.stdout"
if test "$mode" = build; then export LD_LIBRARY_PATH="${shared%%/*}"; fi
"$work/shared-consumer" > "$work/shared.stdout" 2> "$work/shared.stderr"
"$work/static-consumer" > "$work/static.stdout" 2> "$work/static.stderr"
test ! -s "$work/shared.stderr" && test ! -s "$work/static.stderr"
cmp "$qa/expected.stdout" "$work/shared.stdout"
cmp "$qa/expected.stdout" "$work/static.stdout"
LD_DEBUG=bindings LD_BIND_NOW=1 "$work/shared-consumer" > "$work/debug.stdout" 2> "$work/debug.stderr"
cmp "$qa/expected.stdout" "$work/debug.stdout"
nm -g --defined-only "$archive" > "$work/archive-symbols.stdout" 2> "$work/archive-symbols.stderr"
test ! -s "$work/archive-symbols.stderr"
python3 - "$work" "$shared" "$archive" <<'PY'
import json, os, pathlib, re, sys
w, shared, archive = pathlib.Path(sys.argv[1]), sys.argv[2], sys.argv[3]
anchors = ['nghttp3_version', 'nghttp3_strerror', 'nghttp3_err_is_fatal',
           'nghttp3_err_infer_quic_app_error_code', 'nghttp3_vec_len',
           'nghttp3_check_header_name', 'nghttp3_check_header_value',
           'nghttp3_put_uvarint', 'nghttp3_put_uvarintlen',
           'nghttp3_get_uvarint', 'nghttp3_get_uvarintlen']
def trace_has(kind, target):
    candidates = (w / (kind + '-link.stdout')).read_text().splitlines()
    assert any(os.path.isfile(p) and os.path.samefile(p, target) for p in candidates), (kind, target)
    map_paths = re.findall(r'(?:^|\s)(/[^\s()]+)', (w / (kind + '.map')).read_text(), re.M)
    assert any(os.path.isfile(p) and os.path.samefile(p, target) for p in map_paths), (kind, target, map_paths)
trace_has('shared', shared)
trace_has('static', archive)
bindings = []
for line in (w / 'debug.stderr').read_text().splitlines():
    m = re.search(r"binding file (.+?) \[\d+\] to (.+?) \[\d+\]:.*symbol [`']([^'`]+)'", line)
    if m and m.group(3) in anchors and os.path.isfile(m.group(1)) and os.path.samefile(m.group(1), w / 'shared-consumer'):
        assert os.path.isfile(m.group(2)) and os.path.samefile(m.group(2), shared), line
        bindings.append({'caller': m.group(1), 'target': m.group(2), 'symbol': m.group(3), 'raw': line})
assert {r['symbol'] for r in bindings} == set(anchors), bindings
symbols = (w / 'archive-symbols.stdout').read_text()
for symbol in anchors:
    assert re.search(r'\bT\s+' + re.escape(symbol) + r'$', symbols, re.M), symbol
(w / 'linkage-proof.json').write_text(json.dumps({'anchors': anchors, 'same_file_bindings': bindings,
    'shared_link_trace_same_file': True, 'static_link_trace_same_file': True,
    'no_native_network_or_QUIC_session_claim': True}, indent=2) + '\n')
PY
sha256sum "$shared" "$archive" "$include/nghttp3/nghttp3.h" "$include/nghttp3/version.h" "$qa/consumer.c" "$qa/run-qa.sh" "$qa/expected.stdout" > "$work/inputs-after.sha256"
cmp "$work/inputs-before.sha256" "$work/inputs-after.sha256"
if test "$mode" = installed; then
    (cd /; sha256sum -c "$qa/SHA256SUMS") > "$work/installed-manifest-after.stdout" 2> "$work/installed-manifest-after.stderr"
    test ! -s "$work/installed-manifest-after.stderr"
    cmp "$work/installed-manifest-before.stdout" "$work/installed-manifest-after.stdout"
fi
printf 'libnghttp3 %%s shared+static strict API smoke: PASS\n' "$mode"
RUN_QA
cat > packaging-qa/expected.stdout <<'EXPECTED_STDOUT'
libnghttp3 case01 version: PASS
libnghttp3 case02 errors: PASS
libnghttp3 case03 binary-vectors: PASS
libnghttp3 case04 header-names: PASS
libnghttp3 case05 header-values: PASS
libnghttp3 case06 varint-boundaries: PASS
libnghttp3 strict public API: 6 cases PASS
EXPECTED_STDOUT
chmod 0755 packaging-qa/run-qa.sh
sha256sum -c packaging-qa/original.sha256

%build
export CFLAGS="%{optflags}"
export CXXFLAGS="%{optflags}"
export LDFLAGS="%{?build_ldflags}"
cmake -S . -B cmake-build \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DCMAKE_INSTALL_LIBDIR=%{_lib} \
    -DCMAKE_INSTALL_DOCDIR=%{_docdir}/%{name}
cmake --build cmake-build --parallel %{_smp_build_ncpus}
sha256sum -c packaging-qa/original.sha256

%install
DESTDIR=%{buildroot} cmake --install cmake-build
mkdir -p %{buildroot}%{_datadir}/%{name}-tests
install -m 0644 packaging-qa/consumer.c packaging-qa/expected.stdout %{buildroot}%{_datadir}/%{name}-tests/
install -m 0755 packaging-qa/run-qa.sh %{buildroot}%{_datadir}/%{name}-tests/
mkdir -p %{buildroot}%{_licensedir}/%{name}
cp -a packaging-notices %{buildroot}%{_licensedir}/%{name}/source-notices
install -m 0644 COPYING %{buildroot}%{_licensedir}/%{name}/COPYING
install -m 0644 tests/munit/COPYING %{buildroot}%{_licensedir}/%{name}/munit-COPYING
install -m 0644 lib/sfparse/COPYING %{buildroot}%{_licensedir}/%{name}/sfparse-COPYING
install -m 0644 %{SOURCE1} %{buildroot}%{_licensedir}/%{name}/GPL-3.0.txt
install -m 0644 %{SOURCE2} %{buildroot}%{_licensedir}/%{name}/Apache-2.0.txt

%check
export LC_ALL=C LANG=C
sha256sum -c packaging-qa/original.sha256
# Original check target = build main dependency followed by unfiltered CTest.
# Verbose reporting reveals all61 MUnit registrations without running twice.
cmake --build cmake-build --target main
set +e
ctest --test-dir cmake-build -V --output-on-failure > packaging-qa/original-ctest.stdout 2> packaging-qa/original-ctest.stderr
ctest_status=$?
set -e
cat packaging-qa/original-ctest.stdout packaging-qa/original-ctest.stderr
test "$ctest_status" -eq 0
test ! -s packaging-qa/original-ctest.stderr
grep -Fq "61 of 61 (100%%) tests successful, 0 (0%%) test skipped." packaging-qa/original-ctest.stdout
grep -Fq '100%% tests passed, 0 tests failed out of 1' packaging-qa/original-ctest.stdout
test -f cmake-build/examples/qpack
test -f cmake-build/lib/libnghttp3.a
test -f cmake-build/lib/libnghttp3.so.9.9.0
bash packaging-qa/run-qa.sh build "$PWD/lib/includes" "$PWD/cmake-build/lib/libnghttp3.so.9.9.0" "$PWD/cmake-build/lib/libnghttp3.a" "$PWD/packaging-qa"
sha256sum -c packaging-qa/original.sha256
python3 - "%{buildroot}" <<'INSTALL_MANIFEST'
import hashlib, pathlib, sys
root = pathlib.Path(sys.argv[1])
paths = sorted(p for folder in ['usr/include/nghttp3', 'usr/lib/cmake/nghttp3', 'usr/share/libnghttp3-tests', 'usr/share/licenses/libnghttp3', 'usr/share/doc/libnghttp3']
               for p in (root / folder).rglob('*') if p.is_file())
paths += [root / p for p in ['usr/lib64/libnghttp3.so.9.9.0', 'usr/lib64/libnghttp3.a', 'usr/lib64/pkgconfig/libnghttp3.pc']]
assert len(set(paths)) == len(paths)
for p in paths: assert p.is_file()
assert (root / 'usr/include/nghttp3/nghttp3.h').read_bytes() == pathlib.Path('lib/includes/nghttp3/nghttp3.h').read_bytes()
assert (root / 'usr/include/nghttp3/version.h').read_bytes() == pathlib.Path('lib/includes/nghttp3/version.h').read_bytes()
lines = [hashlib.sha256(p.read_bytes()).hexdigest() + '  /' + str(p.relative_to(root)) for p in paths]
(root / 'usr/share/libnghttp3-tests/SHA256SUMS').write_text('\n'.join(lines) + '\n')
INSTALL_MANIFEST

%files
%{_includedir}/nghttp3
%{_libdir}/libnghttp3.so*
%{_libdir}/libnghttp3.a
%{_libdir}/pkgconfig/libnghttp3.pc
%{_prefix}/lib/cmake/nghttp3
%{_datadir}/%{name}-tests
%doc %{_docdir}/%{name}
%license %{_licensedir}/%{name}

%changelog
* Tue Oct 27 2026 openEuler RISC-V package contributors - 1.18.0-1
- Package authenticated official release, preserving shared/static defaults and original test suite.
