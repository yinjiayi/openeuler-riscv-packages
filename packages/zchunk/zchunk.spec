# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 openEuler RISC-V package contributors
Name:           zchunk
Version:        1.5.5
Release:        1%{?dist}
Summary:        Independent-chunk compression tools and public C SDK
License:        BSD-2-Clause AND BSD-1-Clause AND BSD-3-Clause AND MIT AND LicenseRef-Public-Domain AND MPL-2.0 AND Apache-2.0
URL:            https://github.com/zchunk/zchunk
# Official signed-tag Git archive; signature proof is separate from archive SHA.
# https://api.github.com/repos/zchunk/zchunk/tarball/refs/tags/1.5.5
Source0:        zchunk-1.5.5-Git.tar.gz
# Official owned-QA legal text: https://www.apache.org/licenses/LICENSE-2.0.txt
Source1:        Apache-2.0.txt
BuildRequires:  bash
BuildRequires:  binutils
BuildRequires:  coreutils
BuildRequires:  diffutils
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  glibc-devel
BuildRequires:  grep
BuildRequires:  gzip
BuildRequires:  libcurl-devel
BuildRequires:  meson >= 0.54.0
BuildRequires:  ninja-build
BuildRequires:  openssl-devel
BuildRequires:  pkgconf
BuildRequires:  python3
BuildRequires:  tar
BuildRequires:  zstd-devel
Requires:       bash
Requires:       binutils
Requires:       coreutils
Requires:       gcc
Requires:       glibc-devel
Requires:       pkgconf
Requires:       python3
Requires:       zstd

%description
Zchunk stores compressed independent chunks for efficient delta-aware transfers.
This deliberate single SDK package includes the shared C library/header/pkgconfig,
six utilities and supplied manuals. No source patch or native/performance claim.

%prep
%setup -q -n zchunk-zchunk-84e9d1f
python3 - <<'PY_ORIGINALS'
import base64,hashlib,json,stat
from pathlib import Path
original = {'.dockerignore': {'sha256': 'a860299718356459603f80b29b4f640cc16fd1ab4ae6b29c8bc751815f73807c', 'bytes': 13, 'Git_mode': '100644', 'encoding': 'utf8'}, '.gitattributes': {'sha256': 'a3c6d518efc2ccfe6659f2db70a976bc11aa5e8962da42c8523cfceedeed6702', 'bytes': 76, 'Git_mode': '100644', 'encoding': 'utf8'}, '.github/environment.yml': {'sha256': '4f43e4f8ebeeea62774aacf50f299bb820ea962ff26b9b6f4340b68f95aaf00e', 'bytes': 175, 'Git_mode': '100644', 'encoding': 'utf8'}, '.github/workflows/linter.yml': {'sha256': '6a4caa43b4302f00e3fcdde7ca9b6d8bbfbc674f3acb240b6a31171c74773460', 'bytes': 570, 'Git_mode': '100644', 'encoding': 'utf8'}, '.github/workflows/main.yml': {'sha256': '708e55b45e4fa6474691e9bb3a59b36dd23ffe6a136336e56689bef566b10f36', 'bytes': 1929, 'Git_mode': '100644', 'encoding': 'utf8'}, '.gitignore': {'sha256': '4dc79804cea85d9289c97343aaeb1391b40548aadc2af4fe4e1b137e0f174b32', 'bytes': 99, 'Git_mode': '100644', 'encoding': 'utf8'}, '.pre-commit-config.yaml': {'sha256': '63e6ff7cf85212719cfa9199335e6f2bd714dfeeac8ec821d202dbe9b9f6429b', 'bytes': 162, 'Git_mode': '100644', 'encoding': 'utf8'}, 'DOCKER_TESTING.md': {'sha256': '776a0fd661e0ca302a349fb55ee8c16decf0fedfcca30d40adca30b450fd7983', 'bytes': 384, 'Git_mode': '100644', 'encoding': 'utf8'}, 'LICENSE': {'sha256': '3c6a4fd5a93cacec6bf694d0537246bc15a95a274f5c5301749754e56d27b797', 'bytes': 1334, 'Git_mode': '100644', 'encoding': 'utf8'}, 'README.md': {'sha256': '6f80c48418348b09acf3a380c0321d7fbb3a79b19adffe1eb9d941b9fb6c9531', 'bytes': 3371, 'Git_mode': '100644', 'encoding': 'utf8'}, 'autotest/alpine-edge/build.sh': {'sha256': '32acdf6f5f63558950741c418f877f6cbe8aecd09942777d5afe68bc809add3b', 'bytes': 367, 'Git_mode': '100755', 'encoding': 'utf8'}, 'autotest/alpine-edge/build/Dockerfile': {'sha256': '900069803aaec263851df67514028cf1e24a68ad952c9f5ffe2cc574fde23943', 'bytes': 167, 'Git_mode': '100644', 'encoding': 'utf8'}, 'autotest/alpine-edge/prep.sh': {'sha256': '8a5870922a23e456093813e0c35ab84b06f6169a0b3f88b50706d3d7ff6fdbdf', 'bytes': 228, 'Git_mode': '100755', 'encoding': 'utf8'}, 'autotest/alpine-edge/prep/Dockerfile': {'sha256': '86407a515f32daa73cbee666cb0374ce08f5fe05ffeb39a1be4186b1d7b8f65c', 'bytes': 95, 'Git_mode': '100644', 'encoding': 'utf8'}, 'autotest/alpine-edge/test.sh': {'sha256': '44280eff445c8f733b8fba5be5a062bc5bae3a99131acc0f305129ce15a8bff4', 'bytes': 469, 'Git_mode': '100755', 'encoding': 'utf8'}, 'autotest/centos-9-stream/build.sh': {'sha256': '30deb1671d6c4078c65c00958b44d99a31d5d38e52495a8643becba56c22f48a', 'bytes': 372, 'Git_mode': '100755', 'encoding': 'utf8'}, 'autotest/centos-9-stream/build/Dockerfile': {'sha256': '41a70c229b93d57afbd9448b505760dcd1b38185d897df393a31d0275bbc52d2', 'bytes': 156, 'Git_mode': '100644', 'encoding': 'utf8'}, 'autotest/centos-9-stream/prep.sh': {'sha256': '5f0ae45401daaedd8fbba258dc709a54ee202605e1f2b06d20c9a31367247d0d', 'bytes': 244, 'Git_mode': '100755', 'encoding': 'utf8'}, 'autotest/centos-9-stream/prep/Dockerfile': {'sha256': '4002e54f0bfcb62d3d1f5c4f8e65407dc1ee48a70b4be68af071ced68f5729f9', 'bytes': 243, 'Git_mode': '100644', 'encoding': 'utf8'}, 'autotest/centos-9-stream/test.sh': {'sha256': '84e27f043e4dd12ad622b400ba2c7e18049d6a42fba8ee0c6e4ed1bd3bdcd63e', 'bytes': 482, 'Git_mode': '100755', 'encoding': 'utf8'}, 'autotest/debian-latest/build.sh': {'sha256': '8acc6f83de92b8efe2caeff3cff3d14f27cc5789680cab5ac2834099b5a88cfc', 'bytes': 375, 'Git_mode': '100755', 'encoding': 'utf8'}, 'autotest/debian-latest/build/Dockerfile': {'sha256': '31c9b9d34daff23abd10ffce6f26a8d341e9e90d2b89eb23226789e3440f0cfb', 'bytes': 125, 'Git_mode': '100644', 'encoding': 'utf8'}, 'autotest/debian-latest/prep.sh': {'sha256': '033be96e4c179d5d762306b6288cb038f0c21c3b696dbbd6cb7f834c5f567f23', 'bytes': 236, 'Git_mode': '100755', 'encoding': 'utf8'}, 'autotest/debian-latest/prep/Dockerfile': {'sha256': '8166923047ad48f9134f19410fc1ef424dbdbc17dece3cccc9cec3835d2dd5dd', 'bytes': 205, 'Git_mode': '100644', 'encoding': 'utf8'}, 'autotest/debian-latest/test.sh': {'sha256': 'b65eb5774e4a4fa703b4b010be465e6d59a31dbcd2a5204b65c361e430c28421', 'bytes': 473, 'Git_mode': '100755', 'encoding': 'utf8'}, 'autotest/fedora-latest/build.sh': {'sha256': '241eb8f9b3cac0b387dc28ca332c324e48837cc83dc8034ec6a9a155bc927a18', 'bytes': 375, 'Git_mode': '100755', 'encoding': 'utf8'}, 'autotest/fedora-latest/build/Dockerfile': {'sha256': 'cfc09d79f4333ca1feb1d34cfbf75db39f13efef0c08fef5671cb99c280d4042', 'bytes': 125, 'Git_mode': '100644', 'encoding': 'utf8'}, 'autotest/fedora-latest/prep.sh': {'sha256': '3f3d5da14127bb2468fe697bb12399401918ab86cc98c4dc206fe027ee93987a', 'bytes': 236, 'Git_mode': '100755', 'encoding': 'utf8'}, 'autotest/fedora-latest/prep/Dockerfile': {'sha256': 'c8eed98b741ab4d45ad5eabe2913eb34d30735196abb302c51f34e2a7a4d6c3f', 'bytes': 136, 'Git_mode': '100644', 'encoding': 'utf8'}, 'autotest/fedora-latest/test.sh': {'sha256': 'd3be2ea07588c86d5a172b353116963f03e1a934522004ef7f9f3df4eb71e97d', 'bytes': 473, 'Git_mode': '100755', 'encoding': 'utf8'}, 'autotest/opensuse-leap/build.sh': {'sha256': '19bfcb9e845228504719c1898450972d3c37c7f0a4e47b997ff75ac3612bc90b', 'bytes': 383, 'Git_mode': '100755', 'encoding': 'utf8'}, 'autotest/opensuse-leap/build/Dockerfile': {'sha256': '6c43db3e32c6b36c400ed5d79e1e423f9eabe066f248329cb364c41ed8e4d628', 'bytes': 127, 'Git_mode': '100644', 'encoding': 'utf8'}, 'autotest/opensuse-leap/prep.sh': {'sha256': '7254059fdba3f997903ea17555061b7687a629d1fe30466b201c009396e85b08', 'bytes': 240, 'Git_mode': '100755', 'encoding': 'utf8'}, 'autotest/opensuse-leap/prep/Dockerfile': {'sha256': '280a914b9e1ed257c8aecd1ede406f99c1d63fcdc264d967dace103157eb25dc', 'bytes': 165, 'Git_mode': '100644', 'encoding': 'utf8'}, 'autotest/opensuse-leap/test.sh': {'sha256': 'b2535a2f117d61e929bbb9d928c785606c79356d7c8c54a456a2d355784d98c4', 'bytes': 487, 'Git_mode': '100755', 'encoding': 'utf8'}, 'autotest/rocky-8/build.sh': {'sha256': '7419e3a7718a03c639befe330c56dc41c408a83e79f1ea63f89eec6b1ab41090', 'bytes': 352, 'Git_mode': '100755', 'encoding': 'utf8'}, 'autotest/rocky-8/build/Dockerfile': {'sha256': '0389f0e098d0f174cd09b27281ee69253dc2bc9f22826666b0b9a72c4070f970', 'bytes': 155, 'Git_mode': '100644', 'encoding': 'utf8'}, 'autotest/rocky-8/prep.sh': {'sha256': 'aa0aff34857c01054aa0d12b43adb6ff7801eff2fb2adfab501e9f41055b0beb', 'bytes': 235, 'Git_mode': '100755', 'encoding': 'utf8'}, 'autotest/rocky-8/prep/Dockerfile': {'sha256': '244b80b3a6077555120d852588a9c1400a07c70db2fd3e5cf6c1408aa8264da3', 'bytes': 227, 'Git_mode': '100644', 'encoding': 'utf8'}, 'autotest/rocky-8/test.sh': {'sha256': '9e070e1b702425ea2ebd92f0fbaed616182a29d9c18dfd2111c9c8493a66c979', 'bytes': 467, 'Git_mode': '100755', 'encoding': 'utf8'}, 'autotest/ubuntu-lts/build.sh': {'sha256': '920574981de3d283319c856b8b79d95784752ec665f336a4fc2071df9317f947', 'bytes': 385, 'Git_mode': '100755', 'encoding': 'utf8'}, 'autotest/ubuntu-lts/build/Dockerfile': {'sha256': '0572a937b73321e028c469f5470e26ee08bd50898fda98d503d68441ddc12447', 'bytes': 129, 'Git_mode': '100644', 'encoding': 'utf8'}, 'autotest/ubuntu-lts/prep.sh': {'sha256': '2cfffcceb6b1c10b6d6d2b99bb832b34dcfd0f16296583dfd98c6deea5a1c036', 'bytes': 241, 'Git_mode': '100755', 'encoding': 'utf8'}, 'autotest/ubuntu-lts/prep/Dockerfile': {'sha256': 'ca625a5d90eb769d9ec560d980d9fef137c168cd34950f615ba8d270624dcce3', 'bytes': 182, 'Git_mode': '100644', 'encoding': 'utf8'}, 'autotest/ubuntu-lts/test.sh': {'sha256': '63cb50051dadda50d0c0b3643b4e49fe621feb0fe79d7ccbe898e522f67d44ac', 'bytes': 498, 'Git_mode': '100755', 'encoding': 'utf8'}, 'autotest/ubuntu-rolling/build.sh': {'sha256': 'fe1c4117d7392c6be602aef560a96cd9bc70bf1ed4d45efa41ba02b97ce5c749', 'bytes': 377, 'Git_mode': '100755', 'encoding': 'utf8'}, 'autotest/ubuntu-rolling/build/Dockerfile': {'sha256': 'b52428d000fce5e59096a742beee7c80cb965b50b40623787fb21008a72776d5', 'bytes': 125, 'Git_mode': '100644', 'encoding': 'utf8'}, 'autotest/ubuntu-rolling/prep.sh': {'sha256': '9f278e46f7dd7f4c9921ebe7340333067025e8da054afab95006f2f6a18723a4', 'bytes': 238, 'Git_mode': '100755', 'encoding': 'utf8'}, 'autotest/ubuntu-rolling/prep/Dockerfile': {'sha256': '01befbc1f2ac65b309b323d8b4c992366ac8f26397719eca0212b6f971d83763', 'bytes': 183, 'Git_mode': '100644', 'encoding': 'utf8'}, 'autotest/ubuntu-rolling/test.sh': {'sha256': 'e3f5c594e7461c523e78e10a5068fae26fa02fc00853a1a7938a77d3509d0eac', 'bytes': 474, 'Git_mode': '100755', 'encoding': 'utf8'}, 'contrib/gen_xml_dictionary': {'sha256': '1b733794164a2ded34d5034ae53efedcd714eadda86a4f27986791859bb0d411', 'bytes': 1643, 'Git_mode': '100755', 'encoding': 'utf8'}, 'doc/unzck.1': {'sha256': 'c8445645dd09e574e4f86eb557f878ad76f19277fa960ddb6fab0b1f2e6f2526', 'bytes': 2994, 'Git_mode': '100644', 'encoding': 'utf8'}, 'doc/zck.1': {'sha256': '310b71301e8350be439f6b6a8415b99c7f8c482b9f75e807122a0a54eb42583c', 'bytes': 3400, 'Git_mode': '100644', 'encoding': 'utf8'}, 'doc/zck_delta_size.1': {'sha256': 'c402d6216a020594d0907d43dfcca19784a13a33ddf12f981e7199b27ba68e68', 'bytes': 2798, 'Git_mode': '100644', 'encoding': 'utf8'}, 'doc/zck_gen_zdict.1': {'sha256': 'b48fa78d0bed15831dcc3eda1216fa7a6188ad1f1edec46ac1f600a4a91db8a5', 'bytes': 2976, 'Git_mode': '100644', 'encoding': 'utf8'}, 'doc/zck_read_header.1': {'sha256': '414459a2778207c484df6f9659ff2e240fb8afecc0c8b07b14943a2ef33470c2', 'bytes': 2822, 'Git_mode': '100644', 'encoding': 'utf8'}, 'doc/zckdl.1': {'sha256': '1dd0222fb59f11cf267eb316ade343f6cfeac67185cd23b1592904de39c1aa5d', 'bytes': 3015, 'Git_mode': '100644', 'encoding': 'utf8'}, 'include/meson.build': {'sha256': '96f70450367ad515396ea15539c50ff8712d895933d0388eaf86c109bd55f44d', 'bytes': 236, 'Git_mode': '100644', 'encoding': 'utf8'}, 'include/zck.h.in': {'sha256': '5347c8b51246c51a6c86290743d55cb4e92d3c7d87ff55eef571d80b16c4dc4e', 'bytes': 16995, 'Git_mode': '100644', 'encoding': 'utf8'}, 'meson.build': {'sha256': 'd772a7203a1aef13a53010aa164430561f55ef956cb564bfa10a5bd45d726452', 'bytes': 3188, 'Git_mode': '100644', 'encoding': 'utf8'}, 'meson_options.txt': {'sha256': '667e3b5eef27a6a020b8c34a24d7f80c2fe48bbed5fd2e73a20f1e40c70fa366', 'bytes': 312, 'Git_mode': '100644', 'encoding': 'utf8'}, 'src/lib/buzhash/LICENSE': {'sha256': 'baf1362c4cda2455ee07b583d4286de3d6a6d7bc61d2109f012d9acafca00f90', 'bytes': 1069, 'Git_mode': '100644', 'encoding': 'utf8'}, 'src/lib/buzhash/buzhash.c': {'sha256': '19aeac16ad6b2b90fc6b26bfe2351ea4711739d9ea72a26196a4711e4bc924c0', 'bytes': 5949, 'Git_mode': '100644', 'encoding': 'utf8'}, 'src/lib/buzhash/buzhash.h': {'sha256': '24b4f6309c824ce0c54730188aec8a4b13a246d1a51981c08d2e9c3349fb55fa', 'bytes': 392, 'Git_mode': '100644', 'encoding': 'utf8'}, 'src/lib/buzhash/meson.build': {'sha256': '8b1db5ab41e6b81d711b7779fe4176934149dad3d10d242bc38a35f03d351ea9', 'bytes': 34, 'Git_mode': '100644', 'encoding': 'utf8'}, 'src/lib/comp/comp.c': {'sha256': '94ff9cdf0c4625fdfc7b76967493d5223396df25c130f2da95b0bea62b7ba5ee', 'bytes': 25183, 'Git_mode': '100644', 'encoding': 'utf8'}, 'src/lib/comp/meson.build': {'sha256': '635c12d8f445152c2e5e062e13aadfada737678dda5bfff2f796f5642c3a06d4', 'bytes': 93, 'Git_mode': '100644', 'encoding': 'utf8'}, 'src/lib/comp/nocomp/meson.build': {'sha256': '51829eeb1e095565ae3b87c175dd490b09fffd0f9bf09edb1811295ed0adb875', 'bytes': 33, 'Git_mode': '100644', 'encoding': 'utf8'}, 'src/lib/comp/nocomp/nocomp.c': {'sha256': '2ee397039ff71a5fa0d81566f9cafb2eb0a8ea965fb22e7dab216d6751c22c36', 'bytes': 4075, 'Git_mode': '100644', 'encoding': 'utf8'}, 'src/lib/comp/nocomp/nocomp.h': {'sha256': 'cd9018a76120dccea71eed4a94ed4850cfe082781c30c2f6fb0908e67c52ebc8', 'bytes': 128, 'Git_mode': '100644', 'encoding': 'utf8'}, 'src/lib/comp/zstd/meson.build': {'sha256': '4b73530f7517e3baf8f85b043a1b16d2319f9d8d54fbc5a63b5ec0a324383025', 'bytes': 31, 'Git_mode': '100644', 'encoding': 'utf8'}, 'src/lib/comp/zstd/zstd.c': {'sha256': 'a3381207bc444969f30b0366e05280cf646a456dbffd6b372b39a4324bb6bb05', 'bytes': 10062, 'Git_mode': '100644', 'encoding': 'utf8'}, 'src/lib/comp/zstd/zstd.h': {'sha256': '11b91d25731f935ed0c8050f79c43a59736e17cb6cd05042047720c96e258b74', 'bytes': 122, 'Git_mode': '100644', 'encoding': 'utf8'}, 'src/lib/compint.c': {'sha256': 'b35bdc27c7256bb6207420f7543bd680bfae175b5a207738efbf484c1ea9634d', 'bytes': 3714, 'Git_mode': '100644', 'encoding': 'utf8'}, 'src/lib/dl/dl.c': {'sha256': '4a0db86ef48f5d25fefc4ef680b4134467de540ff45226155ea033d4bf1bcf8a', 'bytes': 13979, 'Git_mode': '100644', 'encoding': 'utf8'}, 'src/lib/dl/meson.build': {'sha256': '2e84246fd623581b610d6b7f0f4ba0f61f341e74ba05efa92831b3aacf913023', 'bytes': 57, 'Git_mode': '100644', 'encoding': 'utf8'}, 'src/lib/dl/multipart.c': {'sha256': '406795851bf88fe20bc555622ddb79deaf598aeea0e7999fe0ad75d13c8da9ab', 'bytes': 11080, 'Git_mode': '100644', 'encoding': 'utf8'}, 'src/lib/dl/range.c': {'sha256': '57cfbefd95f87f9b5e885d4785deed5a3e27d19e8185eb2fad6a44c4ba2c1a6e', 'bytes': 7260, 'Git_mode': '100644', 'encoding': 'utf8'}, 'src/lib/error.c': {'sha256': '501dc2e3c40782a593e641ae16ae24fa5cf9832d107694ed7a36ec3b84afe00e', 'bytes': 3177, 'Git_mode': '100644', 'encoding': 'utf8'}, 'src/lib/hash/bundled/libsha.c': {'sha256': 'ae15e62ecbbe686395de15fb736d8089fd88809c15253d05dab0f0b0e38e7079', 'bytes': 5395, 'Git_mode': '100644', 'encoding': 'utf8'}, 'src/lib/hash/bundled/libsha.h': {'sha256': 'aec19ce157efbd283d6566278f4b7cc2215ddbc52b2dac77d93a53c5567adfb9', 'bytes': 549, 'Git_mode': '100644', 'encoding': 'utf8'}, 'src/lib/hash/bundled/meson.build': {'sha256': 'fb0b21c73aaae681baa591f4b3f11eb18e0e5806c7319c4d5d39795a20519e92', 'bytes': 63, 'Git_mode': '100644', 'encoding': 'utf8'}, 'src/lib/hash/bundled/sha1/meson.build': {'sha256': '345706948422170e198b913bae7dcefe6a49dfa2d5b636a87bc3308ec8d69792', 'bytes': 31, 'Git_mode': '100644', 'encoding': 'utf8'}, 'src/lib/hash/bundled/sha1/sha1.c': {'sha256': '88631d3616166f9d995691fb353d68b31ebf3acd6bec9b856c34509a4e75ded4', 'bytes': 6643, 'Git_mode': '100644', 'encoding': 'utf8'}, 'src/lib/hash/bundled/sha1/sha1.h': {'sha256': '3284d2aa6471312e50d8b8087abc3c7600e2532d48a97829ba4c66a5677d92b8', 'bytes': 2201, 'Git_mode': '100644', 'encoding': 'utf8'}, 'src/lib/hash/bundled/sha2/meson.build': {'sha256': '807e4e6ffa70c19d1f07bb48294ea272cfd217f0581754e1603dd27bc24552b8', 'bytes': 31, 'Git_mode': '100644', 'encoding': 'utf8'}, 'src/lib/hash/bundled/sha2/sha2.c': {'sha256': '87c0ad814b23f184b861fc42363fb44cd920253eb7b55dbd874e5cdec6d9b004', 'bytes': 32950, 'Git_mode': '100644', 'encoding': 'utf8'}, 'src/lib/hash/bundled/sha2/sha2.h': {'sha256': '14dc93b268bef4c221a40a9e81e522fe85471e780bffda60d6b4bbcbe0984ffd', 'bytes': 3804, 'Git_mode': '100644', 'encoding': 'utf8'}, 'src/lib/hash/hash.c': {'sha256': 'ed4155b1acedf1bbbe48a6c9bcd1be681122b88f77a2f9ac3f9781350c747c5d', 'bytes': 15778, 'Git_mode': '100644', 'encoding': 'utf8'}, 'src/lib/hash/meson.build': {'sha256': '675e48676a58010f8a5e3406ba69b7a5765c5f7558c196f8027ee5d017476f44', 'bytes': 109, 'Git_mode': '100644', 'encoding': 'utf8'}, 'src/lib/hash/openssl/meson.build': {'sha256': '43753e7d26f16c9cfa5381bacadd521efe0b696618463e2cf28bbefe35101e7f', 'bytes': 34, 'Git_mode': '100644', 'encoding': 'utf8'}, 'src/lib/hash/openssl/openssl.c': {'sha256': 'a8e89c682a11dc387eac0a7860ec528f19681713520c587d2a01fa5140fa922f', 'bytes': 9504, 'Git_mode': '100644', 'encoding': 'utf8'}, 'src/lib/hash/openssl/openssl.h': {'sha256': '792ce2dbef6af80672db37f2b46f67799777deb107bedfa8a41d14794d05ff50', 'bytes': 772, 'Git_mode': '100644', 'encoding': 'utf8'}, 'src/lib/header.c': {'sha256': 'cdfe0fd6c3848d3efb88e527c73ec114945ddd0392fef82cf0462bb4978f53fb', 'bytes': 22003, 'Git_mode': '100644', 'encoding': 'utf8'}, 'src/lib/index/index_common.c': {'sha256': 'cb73b73158b0a52f92832222caaeb081335b5f22ac88b86f29750032a5740f1a', 'bytes': 3030, 'Git_mode': '100644', 'encoding': 'utf8'}, 'src/lib/index/index_create.c': {'sha256': 'f64c9c2f6c2f13180aae70a9f1ce1c4deab6f999e9c5164ee9e20eabebaca319', 'bytes': 8821, 'Git_mode': '100644', 'encoding': 'utf8'}, 'src/lib/index/index_read.c': {'sha256': 'dc6fa7879847adc887e26497ae7d432af630207000a556b96bae1db226c01abe', 'bytes': 11596, 'Git_mode': '100644', 'encoding': 'utf8'}, 'src/lib/index/meson.build': {'sha256': '2e4dc7a3ac1ba008b15a6191b0921aa1af96297501fbb53adf186f4f2d82bc70', 'bytes': 75, 'Git_mode': '100644', 'encoding': 'utf8'}, 'src/lib/io.c': {'sha256': '30fe712e74472d9eb77d96822411f19a1bef044d319ae98c4b3d0c41f93513d0', 'bytes': 4321, 'Git_mode': '100644', 'encoding': 'utf8'}, 'src/lib/log.c': {'sha256': 'bd9918f6f1288ebc78cdef824feb0e880a8d9dd3b521017dadbf6d8fad2ef12d', 'bytes': 2960, 'Git_mode': '100644', 'encoding': 'utf8'}, 'src/lib/meson.build': {'sha256': '01a51c1316de29bb191e2e4359c2e039da3808c0b615f57b230ed7f3a2b1c83e', 'bytes': 1041, 'Git_mode': '100644', 'encoding': 'utf8'}, 'src/lib/uthash.h': {'sha256': 'ba9af0e8c902108cc40be8e742ff4fcbb0e93062d91aefd6070b70d4e067c2ac', 'bytes': 78453, 'Git_mode': '100644', 'encoding': 'utf8'}, 'src/lib/win32/LICENSE': {'sha256': '2c4814fe63fb26c0409517b0d5c287e97a58fb593d22c35cce06457b1237a162', 'bytes': 3352, 'Git_mode': '100644', 'encoding': 'utf8'}, 'src/lib/win32/basename.c': {'sha256': '006d671dcb2080d714587b95e6446eb1c5b2e4ebca50c9ca95834857e4fb2a8f', 'bytes': 304, 'Git_mode': '100644', 'encoding': 'utf8'}, 'src/lib/win32/dirent.h': {'sha256': 'fd3ea80528f24e0faaa41a0b9fb228beeaad6bbbf55968383354682ddf66a185', 'bytes': 22889, 'Git_mode': '100644', 'encoding': 'utf8'}, 'src/lib/win32/ftruncate.c': {'sha256': '49c1204ae77ae2e977bf9dd77d68d621f8397a812f9c6b819c3a41bfd59de944', 'bytes': 418, 'Git_mode': '100644', 'encoding': 'utf8'}, 'src/lib/win32/regcomp.c': {'sha256': 'f933d81a60da516d01bcc7d4a71e0f4aa6294f8e93d917a7896e6e07cc4bdb38', 'bytes': 76222, 'Git_mode': '100644', 'encoding': 'utf8'}, 'src/lib/win32/regerror.c': {'sha256': '174f9a336b9674e51ed2e6f7c3dae3e44ae50df0e66cbacbda82ec2e9823915d', 'bytes': 994, 'Git_mode': '100644', 'encoding': 'utf8'}, 'src/lib/win32/regex.h': {'sha256': '21a094409109a27cc5492cfd64ebe56c1f81052bf8fe763542638b482a8b9fbd', 'bytes': 1339, 'Git_mode': '100644', 'encoding': 'utf8'}, 'src/lib/win32/regexec.c': {'sha256': '66d5e648052caf54a837aceda871e0e0777b660ea2d043efed6cd3c2d428ba9a', 'bytes': 30169, 'Git_mode': '100644', 'encoding': 'utf8'}, 'src/lib/win32/tre-mem.c': {'sha256': 'bcb0d5149530c907a915525fadba49b64c529cc251484a6fc48fd9f7307126e5', 'bytes': 4109, 'Git_mode': '100644', 'encoding': 'utf8'}, 'src/lib/win32/tre.h': {'sha256': 'a01aef1a6d0b22ed8134ffddf4b96ac24efb3d6fa71f5b392123177688635ca1', 'bytes': 7021, 'Git_mode': '100644', 'encoding': 'utf8'}, 'src/lib/win32/unistd.h': {'sha256': 'e261f23ae9ac28b1c6ff009244b3a3e1bada22936451703c9373be1d92a6eef1', 'bytes': 44, 'Git_mode': '100644', 'encoding': 'utf8'}, 'src/lib/zck.c': {'sha256': 'e7b530ecd8952642e954f093254e4adaa40c91c1e4e2b17ec7503f69cbd08006', 'bytes': 14520, 'Git_mode': '100644', 'encoding': 'utf8'}, 'src/lib/zck_private.h': {'sha256': 'd7d7056c7932ca2d3e0e4ec1053b389368d2491c31c88ddabe98d171ce6bf10e', 'bytes': 12704, 'Git_mode': '100644', 'encoding': 'utf8'}, 'src/memmem.c': {'sha256': 'cfc3a9ba8d5bf09cca39a21d49b9002d886282427a50496001544e79c5f14622', 'bytes': 2462, 'Git_mode': '100644', 'encoding': 'utf8'}, 'src/memmem.h': {'sha256': '7157dd0ebb961aecaa2eae40a4b378668d810e62593f5f4ada1c3bd172ae6e12', 'bytes': 117, 'Git_mode': '100644', 'encoding': 'utf8'}, 'src/meson.build': {'sha256': '2de02ef23f78ecd7965cc1ca071ccbec150fdd7a3fc839be9db288cb25e6a79a', 'bytes': 1712, 'Git_mode': '100644', 'encoding': 'utf8'}, 'src/unzck.c': {'sha256': 'cacfb3a033e9f223d1d69da0a3548b56d01a19d07c5d35371d36e08503a7e380', 'bytes': 10036, 'Git_mode': '100644', 'encoding': 'utf8'}, 'src/util_common.c': {'sha256': '53aa763f34f959b7c498cf3b81186fa5831a8969ab79f97019771a4659497ef4', 'bytes': 1606, 'Git_mode': '100644', 'encoding': 'utf8'}, 'src/util_common.h': {'sha256': '5b39b060de551671f2915eb50272f0613d5373f6f3b74190327ac96ccca0cbde', 'bytes': 446, 'Git_mode': '100644', 'encoding': 'utf8'}, 'src/zck.c': {'sha256': '0365086af98e3bcf27f22421af4c8d4eb992f6076a854c9a04e5a07ea1d85e98', 'bytes': 11611, 'Git_mode': '100644', 'encoding': 'utf8'}, 'src/zck_delta_size.c': {'sha256': 'd2a2a0f7ed6de6fb27b467b02fb866563cd70f663e9e5b018ca8eb591b01be7d', 'bytes': 6596, 'Git_mode': '100644', 'encoding': 'utf8'}, 'src/zck_dl.c': {'sha256': '606208221f495d49f373a838a3c61204411bfc987c9111346629ccac325a00f4', 'bytes': 15193, 'Git_mode': '100644', 'encoding': 'utf8'}, 'src/zck_gen_zdict.c': {'sha256': '0af6d158a559dd322ff103388100937a04e10b85ae525ec0b0871aaee3ab555d', 'bytes': 10965, 'Git_mode': '100644', 'encoding': 'utf8'}, 'src/zck_read_header.c': {'sha256': '68a8f5fe3539b2195b6f6e0a5bb2d5be506c1776d333c1f82d4719d07e031a2f', 'bytes': 8397, 'Git_mode': '100644', 'encoding': 'utf8'}, 'subprojects/argp-standalone.wrap': {'sha256': '9fc467cb786b7efdec7ca7278ea58c1d821b14878b215e147572076fa6d25be2', 'bytes': 169, 'Git_mode': '100644', 'encoding': 'utf8'}, 'subprojects/zstd.wrap': {'sha256': '2acb9cecd19fbfd1339e62b3cc612402314508c27d3bc84e65d52a97f28455dc', 'bytes': 457, 'Git_mode': '100644', 'encoding': 'utf8'}, 'test/abi.sh': {'sha256': '6d00f400e25122374bfdb1522c21289b0d6c3f56bae7299bf0654f99bb4e649d', 'bytes': 970, 'Git_mode': '100755', 'encoding': 'utf8'}, 'test/abi/stable/libzck.so.1.5.5': {'sha256': 'ba94c27c18bbb3d2907cf3aeb1b645f6238c8540ec176af6681e56e3125a986d', 'bytes': 277840, 'Git_mode': '100755', 'encoding': 'base64'}, 'test/abi/stable/zck.h': {'sha256': '378ed06deeeacf3261eca1048de1177c0527fee57b42ef97813e5037b1901124', 'bytes': 16991, 'Git_mode': '100644', 'encoding': 'utf8'}, 'test/compat_reports/zchunk/1.5.4_to_1.5.5/compat_report.html': {'sha256': '04abafe862222ba11886f3b2dc7b8b87ab90a2f83524475cfb0bd964b0085d63', 'bytes': 14079, 'Git_mode': '100644', 'encoding': 'utf8'}, 'test/copy_chunks.c': {'sha256': '79f1799934397cc57207e41552f7703dfc044ef08cad3a8cfeaf4d513f224ec5', 'bytes': 4106, 'Git_mode': '100644', 'encoding': 'utf8'}, 'test/empty.c': {'sha256': '35ad9b29719df3a584c11866c499ffcc18d7b4d79e123530ddcb84b39ff66e8d', 'bytes': 3613, 'Git_mode': '100644', 'encoding': 'utf8'}, 'test/exitcodecheck.c': {'sha256': 'aec70c60544c9ac6938e0a069490a1e85d001fd1a4b56fb2b3787c3e8b589c73', 'bytes': 3459, 'Git_mode': '100644', 'encoding': 'utf8'}, 'test/files/LICENSE.dict': {'sha256': 'b20064d89c3beb8605d99c994ff45304f308abd840c0981475dd2faca6ec854b', 'bytes': 4096, 'Git_mode': '100644', 'encoding': 'base64'}, 'test/files/LICENSE.dict.fodt.zck': {'sha256': 'e9b5bcee24965ed6bf8e60c3537c2e1558912bd851cfe0b6e47a44d12bd54cf5', 'bytes': 125874, 'Git_mode': '100644', 'encoding': 'base64'}, 'test/files/LICENSE.fodt': {'sha256': '394ed6c2fc4ac47e5ee111a46f2a35b8010a56c7747748216f52105e868d5a3e', 'bytes': 948788, 'Git_mode': '100644', 'encoding': 'utf8'}, 'test/files/LICENSE.header.new.nodict.fodt.zck': {'sha256': 'fc70f226cba7a253a575a8f778c923ff1f28f9837e9783b50b3ab7105a76eac7', 'bytes': 432, 'Git_mode': '100644', 'encoding': 'base64'}, 'test/files/LICENSE.manual.dict.fodt.zck': {'sha256': '035a58cb3b46c0326f91b193f3e040b9cc9f031c09477b79fd80d7ffbe75e9c4', 'bytes': 442761, 'Git_mode': '100644', 'encoding': 'base64'}, 'test/files/LICENSE.manual.nodict.fodt.zck': {'sha256': '53205d490819bbb681224e21acf0b85ec44c62c5c1f46e59bd084ac471ed534c', 'bytes': 786977, 'Git_mode': '100644', 'encoding': 'base64'}, 'test/files/LICENSE.nocomp.fodt.zck': {'sha256': '8d06d7a8badc83b2f47b4a827013cb1897407cad3fd9ff62fa4c6630de8f813b', 'bytes': 949231, 'Git_mode': '100644', 'encoding': 'base64'}, 'test/files/LICENSE.nodict.fodt.zck': {'sha256': '45e48c11fea129d2c434ffcec7d8fbc1720f30f33d438654cd117616121c218e', 'bytes': 131073, 'Git_mode': '100644', 'encoding': 'base64'}, 'test/files/compressed_int_too_large1.zck': {'sha256': 'd927c944a999b6e66dac1d5ea4aeb83e3409d6f073a1f02bed28fdc4dedd06e7', 'bytes': 60, 'Git_mode': '100644', 'encoding': 'base64'}, 'test/files/compressed_int_too_large2.zck': {'sha256': 'e93a7f40e6c93b42558ca19640db886f50cee8e6a514ec2dbda74b780518c52e', 'bytes': 36, 'Git_mode': '100644', 'encoding': 'base64'}, 'test/files/compressed_int_too_large3.zck': {'sha256': '465db76aeeea1a6a6bb5d984fa3afe21ead314075006fef7528d63b2da1f16b7', 'bytes': 82, 'Git_mode': '100644', 'encoding': 'base64'}, 'test/files/compressed_int_too_large4.zck': {'sha256': 'eaa98d3fd104f009de5030c557060b0fff348e310a6ea905f216a8d231b482d0', 'bytes': 36, 'Git_mode': '100644', 'encoding': 'base64'}, 'test/files/compressed_int_too_large5.zck': {'sha256': '3c54c5e489292fa2398a5323c5df168d51c911469eb18b1fabba6cf07100ff74', 'bytes': 46, 'Git_mode': '100644', 'encoding': 'base64'}, 'test/files/empty.optelems.zck': {'sha256': 'ebd7ef40ad9f8baa89ef7c0ab72386bc8cb015278977cbd1818b1613c5a6307a', 'bytes': 146, 'Git_mode': '100644', 'encoding': 'base64'}, 'test/files/integer_overflow_header.zck': {'sha256': 'e12a14def7d9fbbf4881232373eae607ca7f807df1b7b0dde618b0ff9b4d9425', 'bytes': 1097, 'Git_mode': '100644', 'encoding': 'base64'}, 'test/files/zerolen.zck': {'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'bytes': 0, 'Git_mode': '100644', 'encoding': 'utf8'}, 'test/invalid_input_checksum.c': {'sha256': 'be56253eeff8dd8cc571e54969994f72a21e2957aa7c5a18ae5afb978c161ee5', 'bytes': 2510, 'Git_mode': '100644', 'encoding': 'utf8'}, 'test/lib/meson.build': {'sha256': 'a901a18afe1929f10d2dd6f1d5d058c14b2d11f81e639d30707c82ba58241004', 'bytes': 60, 'Git_mode': '100644', 'encoding': 'utf8'}, 'test/lib/util.c': {'sha256': 'eeea629bcbb7d39ed261eb8721cf84119930fe08b23e4555e6e1680c53a59c6d', 'bytes': 2085, 'Git_mode': '100644', 'encoding': 'utf8'}, 'test/lib/util.h': {'sha256': '04059e60c6c2ff8d9232f09740fd4edfb184d941d35dea18e670d187b99711bc', 'bytes': 1835, 'Git_mode': '100644', 'encoding': 'utf8'}, 'test/meson.build': {'sha256': '043849941c03de7e4e4180f0c8f3a49b696c487ef6d4251d366289fc1aa2d003', 'bytes': 17183, 'Git_mode': '100644', 'encoding': 'utf8'}, 'test/multipart.c': {'sha256': '8eec07bc49fead3af7be58e9236cd0c41940a26889b3c3891aed79ff11c07507', 'bytes': 4178, 'Git_mode': '100644', 'encoding': 'utf8'}, 'test/new_abi.sh': {'sha256': '412c89970ec14e574267be856e90702482620487922b9e47e2c3b98a2cbc26a0', 'bytes': 387, 'Git_mode': '100755', 'encoding': 'utf8'}, 'test/optelems.c': {'sha256': 'd9dda346f3a30824572a579216ee9c93d9cb999290a4d4e3336d47e62cb47062', 'bytes': 2515, 'Git_mode': '100644', 'encoding': 'utf8'}, 'test/read_header_bounds.c': {'sha256': '32c4c05160c888975efc243dabd16cdfd7316309a74279f1631d947534061972', 'bytes': 6549, 'Git_mode': '100644', 'encoding': 'utf8'}, 'test/read_limits.c': {'sha256': '129513f14fae78ca2dfe4cfa605f12b58b93f16bb93dcef6122589c1366e6e0b', 'bytes': 4687, 'Git_mode': '100644', 'encoding': 'utf8'}, 'test/read_single_chunk.c': {'sha256': '7b977e32d2610b715b7ff22428ce19646d7944962eb2348b3136fd7743492f49', 'bytes': 3779, 'Git_mode': '100644', 'encoding': 'utf8'}, 'test/read_single_comp_chunk.c': {'sha256': 'fab12e33f05c27b22abb9d7a3f30f1133a6c9ee9cee651f8cbcfedd915620e16', 'bytes': 3506, 'Git_mode': '100644', 'encoding': 'utf8'}, 'test/shacheck.c': {'sha256': 'ea77802b45dd5a4b67f7921efe5ffff39068c08e185874ec00bba316487662b8', 'bytes': 4063, 'Git_mode': '100644', 'encoding': 'utf8'}, 'test/zck_cmp_uncomp.c': {'sha256': '9c5ce4a1af8a4cf578a9c65e189d0ffbf1471dba68c0f5031c9a436627e77863', 'bytes': 7000, 'Git_mode': '100644', 'encoding': 'utf8'}, 'zchunk_format.txt': {'sha256': 'cfc34b57c2238424bc32d265b27cb3f5758a46a17fe302a280b2efe2154b17c2', 'bytes': 9939, 'Git_mode': '100644', 'encoding': 'utf8'}}
assert len(original)==166 and not Path('.packaging-qa').exists() and not Path('.packaging-source-records').exists()
qa=Path('.packaging-qa');qa.mkdir();records=Path('.packaging-source-records/source-notices');records.mkdir(parents=True)
for name,row in original.items():
    p=Path(name);b=p.read_bytes();assert p.is_file() and not p.is_symlink() and len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'] and bool(p.stat().st_mode&0o111)==(row['Git_mode']=='100755'),name
    q=records/(name+'.notice');q.parent.mkdir(parents=True,exist_ok=True)
    if row['encoding']=='utf8':
        b.decode('utf8');q.write_bytes(b)
    else:
        q.write_text(json.dumps(dict(source_path=name,original_sha256=row['sha256'],original_bytes=row['bytes'],original_Git_mode=row['Git_mode'],encoding='base64',data=base64.b64encode(b).decode()),sort_keys=True)+chr(10))
(records/'original-manifest.json').write_text(json.dumps(original,sort_keys=True)+chr(10))
lines=[hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(records).as_posix()+chr(10) for p in sorted(records.rglob('*')) if p.is_file()]
(records/'SHA256SUMS').write_text(''.join(lines))

PY_ORIGINALS
cat > .packaging-qa/consumer.c <<'EOF_CONSUMER'
/* SPDX-License-Identifier: Apache-2.0
 * Copyright 2026 The openEuler RISC-V package contributors
 * Owned additive public-API functional QA; not upstream or native ABI proof.
 */
#define _GNU_SOURCE
#include <zck.h>
#include <dlfcn.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#define NEED(x) do { if (!(x)) { fprintf(stderr,"QA failure line %%d\n",__LINE__); return 1; } } while (0)
static int roundtrip(int mode, const char *name) {
    static const char original[] = "zchunk public API\n\0binary\377payload\n";
    char output[sizeof(original)+1];
    int fd=open(name,O_RDWR|O_CREAT|O_EXCL,0600); NEED(fd>=0);
    zckCtx *w=zck_create(); NEED(w!=NULL);
    NEED(zck_init_write(w,fd));
    NEED(zck_set_ioption(w,ZCK_COMP_TYPE,mode));
    NEED(zck_write(w,original,sizeof(original))==(ssize_t)sizeof(original));
    /* zck_close closes only its temp_fd; zck_free clears fd without closing it.
       The caller owns fd (src/lib/zck.c405-438, zck_clear80-89). */
    NEED(zck_close(w)); NEED(fcntl(fd,F_GETFD)>=0); zck_free(&w); NEED(w==NULL); NEED(fcntl(fd,F_GETFD)>=0);
    NEED(lseek(fd,0,SEEK_SET)==0);
    zckCtx *r=zck_create(); NEED(r!=NULL); NEED(zck_init_read(r,fd));
    ssize_t n=zck_read(r,output,sizeof(output));
    NEED(n==(ssize_t)sizeof(original)); NEED(memcmp(original,output,sizeof(original))==0);
    NEED(zck_read(r,output,sizeof(output))==0);
    NEED(zck_close(r)); NEED(fcntl(fd,F_GETFD)>=0); zck_free(&r); NEED(r==NULL); NEED(fcntl(fd,F_GETFD)>=0); NEED(close(fd)==0);
    return 0;
}
int main(void) {
    Dl_info origin; NEED(dladdr((void *)zck_create,&origin)!=0 && origin.dli_fname!=NULL);
    printf("LIBRARY=%%s\n",origin.dli_fname);
    NEED(strcmp(ZCK_VERSION,"1.5.5")==0);
    NEED(roundtrip(ZCK_COMP_NONE,"api-none.zck")==0);
    NEED(roundtrip(ZCK_COMP_ZSTD,"api-zstd.zck")==0);
    puts("public-api nocomp+zstd exact binary roundtrips PASS");
    return 0;
}
EOF_CONSUMER
cat > .packaging-qa/run-qa.py <<'EOF_RUNNER'
#!/usr/bin/python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 The openEuler RISC-V package contributors
"""TARGET ONLY additive QA. Full evidence goes to JSON-marked CI stdout."""
import argparse,base64,hashlib,json,os,re,shlex,stat,subprocess
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--root',default='/');ap.add_argument('--output',required=True);a=ap.parse_args()
root=Path(a.root).resolve();out=Path(a.output).resolve();assert not out.exists();out.mkdir(mode=0o700)
qa=root/'usr/share/zchunk-tests';lib=root/'usr/lib64/libzck.so.1.5.5';binaries={p:root/'usr/bin'/p for p in ['zck','unzck','zck_gen_zdict','zck_read_header','zck_delta_size','zckdl']}
self=Path(__file__).resolve();assert os.path.samefile(self,qa/'run-qa.py')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def model(p):
 s=p.lstat();return dict(path=str(p),realpath=str(p.resolve(strict=True)),mode=oct(stat.S_IMODE(s.st_mode)),symlink=p.is_symlink(),symlink_target=os.readlink(p) if p.is_symlink() else None,sha256=sha(p),bytes=p.stat().st_size)
def elf(p):
 b=p.read_bytes();assert b[:6]==b'\x7fELF\x02\x01' and int.from_bytes(b[18:20],'little')==243;return dict(path=str(p),class_bits=64,little_endian=True,machine=243,sha256=sha(p))
entries={}
for line in (qa/'SHA256SUMS').read_text().splitlines():
 h,name=line.split('  ',1);assert re.fullmatch('[0-9a-f]{64}',h) and name in ['consumer.c','run-qa.py'] and name not in entries;entries[name]=h
assert set(entries)=={'consumer.c','run-qa.py'} and all(sha(qa/p)==h for p,h in entries.items())
symlinks=[root/'usr/lib64/libzck.so',root/'usr/lib64/libzck.so.1'];assert all(p.is_symlink() and os.path.samefile(p,lib) for p in symlinks)
production=list(binaries.values())+[root/'usr/include/zck.h',root/'usr/lib64/pkgconfig/zck.pc',lib]+symlinks+[root/'usr/share/man/man1'/(p+'.1') for p in binaries]
production=[p if p.exists() else p.with_name(p.name+'.gz') for p in production];assert len(production)==17 and all(p.is_file() for p in production)
paths=production+[qa/'consumer.c',qa/'run-qa.py',qa/'SHA256SUMS'];before=[model(p) for p in paths];self_before=sha(self)
work=out/'work';work.mkdir();(work/'home').mkdir()
# Construct a closed target tool environment: no inherited compiler/link flags,
# preload/audit hooks, pkg-config sysroot, host include paths or credential vars.
env=dict(PATH='/usr/bin:/bin',HOME=str(work/'home'),TMPDIR=str(work),LC_ALL='C',LANG='C',PKG_CONFIG_LIBDIR=str(root/'usr/lib64/pkgconfig'),PKG_CONFIG_PATH='',LD_LIBRARY_PATH=str(root/'usr/lib64'))
for key in ['QEMU_CPU','QEMU_LD_PREFIX']:
 if key in os.environ:env[key]=os.environ[key]  # Retain only explicit target-harness routing, recorded below.
commands=[]
def packed(b):return dict(bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),base64=base64.b64encode(b).decode())
def run(label,argv,expected=0):
 p=subprocess.run([str(x) for x in argv],cwd=work,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=120)
 for k,b in [('stdout',p.stdout),('stderr',p.stderr)]:(out/(label+'.'+k)).write_bytes(b)
 commands.append(dict(label=label,argv=[str(x) for x in argv],cwd=str(work),environment=dict(env),status=p.returncode,stdout=packed(p.stdout),stderr=packed(p.stderr)))
 assert p.returncode==expected,(label,p.returncode,expected)
 return p
version=b'zchunk 1.5.5\nCopyright (c) 2021 Jonathan Dieter\n'
for name,p in binaries.items():
 v=run('version-'+name,[p,'-V']);assert v.stdout==version and v.stderr==b'';elf(p)
payload=bytes(range(256))*40+b'\x00zchunk owned binary roundtrip\xff\n';(work/'input.bin').write_bytes(payload)
for fmt in ['zstd','none']:
 run('compress-'+fmt,[binaries['zck'],'--compression-format='+fmt,'-o',fmt+'.zck','input.bin'])
 run('decompress-'+fmt,[binaries['unzck'],fmt+'.zck']);assert (work/fmt).read_bytes()==payload
(work/'invalid.zck').write_bytes(b'not a zchunk file\n')
# src/unzck.c178-181 -> error2, good_exit false -> unlink output and exit1.
run('invalid-input',[binaries['unzck'],'invalid.zck'],1);assert not (work/'invalid').exists()
flags=shlex.split(run('pkgconfig-cflags',['pkg-config','--define-variable=prefix='+str(root/'usr'),'--cflags','zck']).stdout.decode())
libs=shlex.split(run('pkgconfig-libs',['pkg-config','--define-variable=prefix='+str(root/'usr'),'--libs','zck']).stdout.decode())
consumer=work/'consumer';mapfile=work/'consumer.map';common=['gcc','-std=c11','-Wall','-Wextra','-Werror']+flags+[str(qa/'consumer.c')]
trace=run('compile-public-api',common+['-o',str(consumer),'-Wl,-t','-Wl,-Map,'+str(mapfile)]+libs+['-ldl'])
linked=[x.strip() for x in (trace.stdout+trace.stderr).decode().splitlines() if x.strip()]
assert any(Path(p).exists() and os.path.samefile(p,lib) for p in linked)
mapbytes=mapfile.read_bytes();loads=[x.strip().split(None,1)[1] for x in mapbytes.decode().splitlines() if x.strip().startswith('LOAD ')]
assert any(Path(p).exists() and os.path.samefile(p,lib) for p in loads)
unlinked=work/'unlinked';negative=run('negative-no-library',common+['-o',str(unlinked),'-ldl'],1)
anchors=sorted(set(re.findall(r'\b(zck_[a-z_]+)\s*\(', (qa/'consumer.c').read_text())))
assert len(anchors)==8 and b'undefined reference' in negative.stderr and all(x.encode() in negative.stderr for x in anchors) and not unlinked.exists()
elf(consumer);api=run('public-api-consumer',[consumer]);lines=api.stdout.decode().splitlines();assert len(lines)==2 and lines[0].startswith('LIBRARY=') and os.path.samefile(lines[0][8:],lib) and lines[1]=='public-api nocomp+zstd exact binary roundtrips PASS' and api.stderr==b''
dynamic={};elfmodels=[]
for label,p in [('library',lib),('consumer',consumer)]+list(binaries.items()):
 h=run('readelf-'+label+'-header',['readelf','-W','-h',p]);d=run('readelf-'+label+'-dynamic',['readelf','-W','-d',p]);elfmodels.append(elf(p));dynamic[label]=re.findall(r'\(NEEDED\).*?Shared library: \[([^]]+)\]',d.stdout.decode());assert b'ELF64' in h.stdout and b'RISC-V' in h.stdout
 if label!='library':assert 'libzck.so.1' in dynamic[label]
assert 'libcurl.so.4' in dynamic['zckdl']
after=[model(p) for p in paths];assert before==after and self_before==sha(self) and all(sha(qa/p)==h for p,h in entries.items())
report=dict(groups=['six exact CLI versions','default zstd binary CLI roundtrip','nocomp binary CLI roundtrip','invalid input exactexit1/outputabsent','public C API two compression roundtrips + exact installed DSO','sameflags no-library negative link control'],group_count=6,commands=commands,production_and_QA_inputs_before=before,production_and_QA_inputs_after=after,SHA256SUMS_entries=entries,all_recorded_inputs_unchanged=True,helper_sha256=self_before,public_consumer=elf(consumer),all_ELF_models=elfmodels,DT_NEEDED=dynamic,linker_map=packed(mapbytes),linker_map_file=str(mapfile),negative_undefined_anchors=anchors,installed_same_file_DSO_binding=True,linker_trace_and_map_same_file=True,original_Meson_tests_not_replaced=True,native_ABI_performance_or_HTTP_download_correctness_claim=False)
(out/'receipt.json').write_text(json.dumps(report,indent=2)+'\n')
print('BEGIN_ZCHUNK_ADDITIVE_QA_JSON');print(json.dumps(report,sort_keys=True));print('END_ZCHUNK_ADDITIVE_QA_JSON')
print('zchunk additive QA: six groups PASS')
EOF_RUNNER
chmod 0755 .packaging-qa/run-qa.py
(cd .packaging-qa && sha256sum consumer.c run-qa.py > SHA256SUMS)
python3 - <<'PY_UNCHANGED_PREP'
import base64,hashlib,json,stat
from pathlib import Path
base=Path('.packaging-source-records/source-notices');original=json.loads((base/'original-manifest.json').read_text());assert len(original)==166
for name,row in original.items():
    p=Path(name);b=p.read_bytes();assert p.is_file() and not p.is_symlink() and len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'] and bool(p.stat().st_mode&0o111)==(row['Git_mode']=='100755'),name
    notice=(base/(name+'.notice')).read_bytes()
    if row['encoding']=='base64':
        v=json.loads(notice);assert v['encoding']=='base64' and v['original_sha256']==row['sha256'] and v['original_Git_mode']==row['Git_mode'];notice=base64.b64decode(v['data'],validate=True)
    assert notice==b,name
print('all166 original source bytes/modes and reversible notices unchanged')
PY_UNCHANGED_PREP

%build
# Packaging buildtype plain consumes RPM optimization/debug flags. It does not
# disable original assertions or alter production feature/default-library options.
export CFLAGS="%{optflags} -g -UNDEBUG"
export LDFLAGS="%{?build_ldflags}"
meson setup build --prefix=%{_prefix} --libdir=%{_lib} --buildtype=plain --wrap-mode=nodownload
python3 - <<'PY_OPTIONS'
import json
from pathlib import Path
options={r['name']:r['value'] for r in json.loads(Path('build/meson-info/intro-buildoptions.json').read_text())}
for key,value in {'with-zstd':'auto','with-openssl':'auto','with-curl':'auto','coverity':False,'docs':True,'tests':True,'default_library':'shared','c_std':'gnu11'}.items():assert options[key]==value,(key,options[key])
deps=json.loads(Path('build/meson-info/intro-dependencies.json').read_text());assert all(any(r['name']==name for r in deps) for name in ['libzstd','libcurl','openssl'])
PY_OPTIONS
meson compile -C build

%install
DESTDIR=%{buildroot} meson install -C build --no-rebuild
install -d %{buildroot}%{_datadir}/zchunk-tests %{buildroot}%{_licensedir}/%{name}
install -m 0644 .packaging-qa/consumer.c .packaging-qa/SHA256SUMS %{buildroot}%{_datadir}/zchunk-tests/
install -m 0755 .packaging-qa/run-qa.py %{buildroot}%{_datadir}/zchunk-tests/
install -m 0644 LICENSE %{buildroot}%{_licensedir}/%{name}/LICENSE
install -m 0644 %{SOURCE1} %{buildroot}%{_licensedir}/%{name}/Apache-2.0.txt
cp -a .packaging-source-records/source-notices %{buildroot}%{_licensedir}/%{name}/

%check
export LC_ALL=C LANG=C
python3 - <<'PY_UNCHANGED_CHECK'
import base64,hashlib,json,stat
from pathlib import Path
base=Path('.packaging-source-records/source-notices');original=json.loads((base/'original-manifest.json').read_text());assert len(original)==166
for name,row in original.items():
    p=Path(name);b=p.read_bytes();assert p.is_file() and not p.is_symlink() and len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'] and bool(p.stat().st_mode&0o111)==(row['Git_mode']=='100755'),name
    notice=(base/(name+'.notice')).read_bytes()
    if row['encoding']=='base64':
        v=json.loads(notice);assert v['encoding']=='base64' and v['original_sha256']==row['sha256'] and v['original_Git_mode']==row['Git_mode'];notice=base64.b64decode(v['data'],validate=True)
    assert notice==b,name
print('all166 original source bytes/modes and reversible notices unchanged')
PY_UNCHANGED_CHECK
set +e
meson test -C build --no-rebuild --print-errorlogs -v > .packaging-qa/original-tests.log 2>&1
test_status=$?
set -e
cat .packaging-qa/original-tests.log
test "$test_status" -eq 0
python3 - <<'PY_ORIGINAL_TESTS'
import json
from pathlib import Path
expected = ['create and validate empty zchunk file', 'rejects malicious multipart responses', 'rejects out-of-range values when reading', 'rejects truncated preface without over-reading', 'check version info in zck', 'check version info in unzck', 'check version info in zckdl', 'check version info in zck_read_header', 'check version info in zck_delta_size', 'check opening file with optional flags', 'checksum with non-hex character', 'read single chunk', 'read single compressed chunk', 'check verbosity in unzck', 'check verbosity in zck', 'check verbosity in zckdl', 'check verbosity in zck_read_header', 'check verbosity in zck_delta_size', 'copy chunks from source', 'decompress previously generated auto-chunked file - nocomp', 'decompress previously generated auto-chunked file - no dict', 'decompress previously generated auto-chunked file - dict', 'decompress previously generated manual file - no dict', 'decompress previously generated manual file - dict', 'decompress dict from previously generated auto-chunked file', 'compress auto-chunked file - no dict', 'decompress auto-chunked file - no dict', 'compress auto-chunked file - dict', 'decompress auto-chunked file - dict', 'compress manual file - no dict', 'decompress manual file - no dict', 'compress manual file - dict', 'decompress manual file - dict', 'handles integer overflow in header', 'handles empty file', "handles compressed int that's too large - variant 1", "handles compressed int that's too large - variant 2", "handles compressed int that's too large - variant 3", "handles compressed int that's too large - variant 4", "handles compressed int that's too large - variant 5"]
rows=[json.loads(line) for line in Path('build/meson-logs/testlog.json').read_text().splitlines() if line.strip()]
assert len(rows)==40 and len({r['name'] for r in rows})==40
for name in expected:
    found=[r for r in rows if r['name'] in [name,'zck / '+name]];assert len(found)==1,(name,[r['name'] for r in rows]);r=found[0]
    if name=='rejects truncated preface without over-reading' and r['result']=='SKIP':
        assert r['returncode']==77 and r['stdout']=='Skipping: needs valgrind or AddressSanitizer\n',r
    else:assert r['result']==('EXPECTEDFAIL' if name=='check verbosity in zckdl' else 'OK'),r
print('ZCHUNK_NORMAL_40_COMPLETE_MEMORY_GATE_ONLY_DECLARED_SKIP')
raw=Path('build/meson-logs/testlog.json').read_bytes()
import base64,hashlib
print('ZCHUNK_NORMAL_TESTLOG_JSON '+json.dumps(dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),base64=base64.b64encode(raw).decode()),sort_keys=True))
PY_ORIGINAL_TESTS
# Keep the production/default tree unchanged. The upstream memory regression
# intentionally returns77 without a memory checker; execute its full original
# suite again in a separate genuinely AddressSanitizer-instrumented tree.
python3 - <<'PY_ASAN_ENV'
import os
assert not any(os.environ.get(k) for k in ['ASAN_OPTIONS','LSAN_OPTIONS','LD_PRELOAD']), 'No sanitizer disable/preload override is permitted'
PY_ASAN_ENV
asan_build=.packaging-qa/asan-build
test ! -e "$asan_build"
CFLAGS="%{optflags} -g -UNDEBUG" LDFLAGS="%{?build_ldflags}" meson setup "$asan_build" . --prefix=%{_prefix} --libdir=%{_lib} --buildtype=plain --wrap-mode=nodownload -Db_sanitize=address
python3 - <<'PY_ASAN_OPTIONS'
import json,shlex
from pathlib import Path
p=Path('.packaging-qa/asan-build');options={r['name']:r['value'] for r in json.loads((p/'meson-info/intro-buildoptions.json').read_text())}
for key,value in {'with-zstd':'auto','with-openssl':'auto','with-curl':'auto','coverity':False,'docs':True,'tests':True,'default_library':'shared','c_std':'gnu11','b_sanitize':'address'}.items():assert options[key]==value,(key,options[key])
rows=json.loads((p/'compile_commands.json').read_text());assert rows
for row in rows:
    args=row.get('arguments') or shlex.split(row['command'])
    assert '-fsanitize=address' in args and not any(v.startswith(('-fno-sanitize','-D__SANITIZE_ADDRESS__')) for v in args),row
assert any(Path(r['file']).name=='read_header_bounds.c' for r in rows)
print('ZCHUNK_ASAN_COMPILE_COMMANDS '+json.dumps(rows,sort_keys=True))
PY_ASAN_OPTIONS
meson compile -C "$asan_build"
python3 - <<'PY_ASAN_ELF'
import hashlib,json,subprocess
from pathlib import Path
p=Path('.packaging-qa/asan-build');proof=[]
for rel in ['src/lib/libzck.so.1.5.5','test/read_header_bounds']:
    q=p/rel;b=q.read_bytes();assert b[:6]==b'\x7fELF\x02\x01' and int.from_bytes(b[18:20],'little')==243
    v=subprocess.run(['readelf','-W','-d',str(q)],check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    assert v.stderr==b'' and b'Shared library: [libasan.so.8]' in v.stdout
    proof.append(dict(path=str(q),sha256=hashlib.sha256(b).hexdigest(),DT_NEEDED_raw=v.stdout.decode()))
print('ZCHUNK_ASAN_ELF_INSTRUMENTATION '+json.dumps(proof,sort_keys=True))
PY_ASAN_ELF
set +e
meson test -C "$asan_build" --no-rebuild --print-errorlogs -v > .packaging-qa/asan-tests.log 2>&1
asan_status=$?
set -e
cat .packaging-qa/asan-tests.log
test "$asan_status" -eq 0
python3 - <<'PY_ASAN_TESTS'
import base64,hashlib,json
from pathlib import Path
expected = ['create and validate empty zchunk file', 'rejects malicious multipart responses', 'rejects out-of-range values when reading', 'rejects truncated preface without over-reading', 'check version info in zck', 'check version info in unzck', 'check version info in zckdl', 'check version info in zck_read_header', 'check version info in zck_delta_size', 'check opening file with optional flags', 'checksum with non-hex character', 'read single chunk', 'read single compressed chunk', 'check verbosity in unzck', 'check verbosity in zck', 'check verbosity in zckdl', 'check verbosity in zck_read_header', 'check verbosity in zck_delta_size', 'copy chunks from source', 'decompress previously generated auto-chunked file - nocomp', 'decompress previously generated auto-chunked file - no dict', 'decompress previously generated auto-chunked file - dict', 'decompress previously generated manual file - no dict', 'decompress previously generated manual file - dict', 'decompress dict from previously generated auto-chunked file', 'compress auto-chunked file - no dict', 'decompress auto-chunked file - no dict', 'compress auto-chunked file - dict', 'decompress auto-chunked file - dict', 'compress manual file - no dict', 'decompress manual file - no dict', 'compress manual file - dict', 'decompress manual file - dict', 'handles integer overflow in header', 'handles empty file', "handles compressed int that's too large - variant 1", "handles compressed int that's too large - variant 2", "handles compressed int that's too large - variant 3", "handles compressed int that's too large - variant 4", "handles compressed int that's too large - variant 5"]
p=Path('.packaging-qa/asan-build/meson-logs/testlog.json');raw=p.read_bytes();rows=[json.loads(line) for line in raw.decode().splitlines() if line.strip()]
assert len(rows)==40 and len({r['name'] for r in rows})==40
for name in expected:
    found=[r for r in rows if r['name'] in [name,'zck / '+name]];assert len(found)==1,(name,[r['name'] for r in rows]);r=found[0]
    assert r['result']==('EXPECTEDFAIL' if name=='check verbosity in zckdl' else 'OK'),r
    if name=='check verbosity in zckdl':assert r['returncode']==10,r
    assert not any(token in (r.get('stdout','')+r.get('stderr','')) for token in ['AddressSanitizer','LeakSanitizer','Sanitizer CHECK failed']),r
whole=Path('.packaging-qa/asan-tests.log').read_text()
assert not any(token in whole for token in ['AddressSanitizer','LeakSanitizer','Sanitizer CHECK failed']), 'Sanitizer diagnostic must not hide behind an expected failure'
print('ZCHUNK_ASAN_40_COMPLETE_39_OK_1_XFAIL_0_SKIP')
print('ZCHUNK_ASAN_TESTLOG_JSON '+json.dumps(dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),base64=base64.b64encode(raw).decode()),sort_keys=True))
PY_ASAN_TESTS
python3 - <<'PY_ASAN_UNCHANGED'
import base64,hashlib,json,stat
from pathlib import Path
base=Path('.packaging-source-records/source-notices');original=json.loads((base/'original-manifest.json').read_text());assert len(original)==166
for name,row in original.items():
    p=Path(name);b=p.read_bytes();assert p.is_file() and not p.is_symlink() and len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'] and bool(p.stat().st_mode&0o111)==(row['Git_mode']=='100755'),name
    notice=(base/(name+'.notice')).read_bytes()
    if row['encoding']=='base64':
        v=json.loads(notice);assert v['encoding']=='base64' and v['original_sha256']==row['sha256'] and v['original_Git_mode']==row['Git_mode'];notice=base64.b64decode(v['data'],validate=True)
    assert notice==b,name
print('all166 original source bytes/modes and reversible notices unchanged')
PY_ASAN_UNCHANGED
(cd %{buildroot}%{_datadir}/zchunk-tests && sha256sum -c SHA256SUMS)
python3 %{buildroot}%{_datadir}/zchunk-tests/run-qa.py --root %{buildroot} --output "$PWD/.packaging-qa/build-qa-results"

%files
%license %{_licensedir}/%{name}
%doc README.md zchunk_format.txt
%{_bindir}/zck
%{_bindir}/unzck
%{_bindir}/zck_gen_zdict
%{_bindir}/zck_read_header
%{_bindir}/zck_delta_size
%{_bindir}/zckdl
%{_libdir}/libzck.so*
%{_includedir}/zck.h
%{_libdir}/pkgconfig/zck.pc
%{_mandir}/man1/zck.1*
%{_mandir}/man1/unzck.1*
%{_mandir}/man1/zck_gen_zdict.1*
%{_mandir}/man1/zck_read_header.1*
%{_mandir}/man1/zck_delta_size.1*
%{_mandir}/man1/zckdl.1*
%{_datadir}/zchunk-tests

%changelog
* Wed Oct 28 2026 openEuler package contributors - 1.5.5-1
- Import signed stable tag; retain all40 default tests, features and normal debug policy.
