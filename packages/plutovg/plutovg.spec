# SPDX-License-Identifier: Apache-2.0
# Native CMake installs a static archive, no ELF executable/DSO. This does not
# assert that the archive lacks DWARF; automatic empty debuginfo is not emitted.
%global debug_package %{nil}
Name:           plutovg
Version:        1.3.3
Release:        1
Summary:        Static C vector graphics SDK with additive consumer validation
License:        MIT AND FTL AND Apache-2.0
URL:            https://github.com/sammycage/plutovg
Source0:        plutovg-1.3.3-Git.tar.gz
Source1:        Apache-2.0.txt
Patch0:         0001-fix-UTF16-surrogate-lookahead.patch
BuildRequires:  bash
BuildRequires:  binutils
BuildRequires:  cmake >= 3.20
BuildRequires:  coreutils
BuildRequires:  dejavu-fonts = 2.37-3.oe2403sp3
BuildRequires:  gcc
BuildRequires:  glibc-devel
BuildRequires:  gzip
BuildRequires:  make
BuildRequires:  patch
BuildRequires:  pkgconf
BuildRequires:  python3 >= 3.9
BuildRequires:  tar
Requires:       bash
Requires:       binutils
Requires:       cmake >= 3.20
Requires:       coreutils
Requires:       dejavu-fonts = 2.37-3.oe2403sp3
Requires:       gcc
Requires:       glibc-devel
Requires:       make
Requires:       pkgconf
Requires:       python3 >= 3.9

%description
PlutoVG provides paths, transforms, colors, paints, raster surfaces and text.
The native CMake static default, original smiley example and font-cache loading
remain enabled. There is no original registered upstream test suite in this
fixed source. Packaging-owned target checks are additive, not a replacement.

%prep
%setup -q -n sammycage-plutovg-bbd91f0
mkdir -p .packaging-qa/assets
cat > .packaging-qa/assets/consumer.c <<'OWNED_PLUTOVG_ASSET_0'
/* SPDX-License-Identifier: Apache-2.0 */
/* Packaging-owned target-only SDK checks; never an upstream test replacement. */
#include <plutovg.h>
#include <math.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#ifndef PLUTOVG_BUILD_STATIC
#error "The native static SDK must propagate PLUTOVG_BUILD_STATIC"
#endif
#define CHECK(x) do { if(!(x)) { fprintf(stderr,"CHECK:%%d:%%s\n",__LINE__,#x); exit(1); } } while(0)
static int near(float x,float y) { return fabsf(x-y)<0.002f; }
void font_checks(const char*,const char*);
static void version_lifetime(void)
{
 CHECK(PLUTOVG_VERSION==10303 && plutovg_version()==PLUTOVG_VERSION);
 CHECK(!strcmp(plutovg_version_string(),"1.3.3"));
 plutovg_path_t* p=plutovg_path_create();CHECK(p && plutovg_path_get_reference_count(p)==1);
 CHECK(plutovg_path_reference(p)==p && plutovg_path_get_reference_count(p)==2);
 plutovg_path_destroy(p);CHECK(plutovg_path_get_reference_count(p)==1);plutovg_path_destroy(p);
 puts("PASS version-lifetime");
}
static void matrices(void)
{
 plutovg_matrix_t m,inv,bad;float x,y;
 CHECK(plutovg_matrix_parse(&m,"matrix(2 0 0 3 4 5)",-1));
 plutovg_matrix_map(&m,2,3,&x,&y);CHECK(near(x,8) && near(y,14));
 CHECK(plutovg_matrix_invert(&m,&inv));plutovg_matrix_map(&inv,x,y,&x,&y);CHECK(near(x,2)&&near(y,3));
 plutovg_matrix_init_scale(&bad,0,1);CHECK(!plutovg_matrix_invert(&bad,&inv));
 CHECK(!plutovg_matrix_parse(&m,"not-a-transform",-1));puts("PASS matrices");
}
static void paths(void)
{
 plutovg_path_t* p=plutovg_path_create();plutovg_rect_t r;
 CHECK(plutovg_path_parse(p,"M2 3H12V13H2Z",-1));
 CHECK(near(plutovg_path_extents(p,&r,true),40));CHECK(near(r.x,2)&&near(r.y,3)&&near(r.w,10)&&near(r.h,10));
 const plutovg_path_element_t* e=NULL;CHECK(plutovg_path_get_elements(p,&e)>0 && e);
 plutovg_path_t* q=plutovg_path_clone(p);CHECK(q && near(plutovg_path_length(q),40));
 plutovg_matrix_t t;plutovg_matrix_init_translate(&t,5,7);plutovg_path_transform(q,&t);
 plutovg_path_extents(q,&r,true);CHECK(near(r.x,7)&&near(r.y,10));plutovg_path_extents(p,&r,true);CHECK(near(r.x,2)&&near(r.y,3));
 plutovg_path_destroy(q);plutovg_path_destroy(p);puts("PASS paths");
}
static void colors(void)
{
 plutovg_color_t c;CHECK(plutovg_color_parse(&c,"#336699",-1)==7);CHECK(plutovg_color_to_rgba32(&c)==0x336699ffu);
 CHECK(plutovg_color_to_argb32(&c)==0xff336699u);CHECK(plutovg_color_parse(&c,"not-a-color",-1)==0);
 plutovg_paint_t* p=plutovg_paint_create_rgba(1,0,0,0.5f);CHECK(p && plutovg_paint_get_reference_count(p)==1);
 CHECK(plutovg_paint_reference(p)==p && plutovg_paint_get_reference_count(p)==2);plutovg_paint_destroy(p);plutovg_paint_destroy(p);puts("PASS colors-paints");
}
static void unicode(void)
{
 const unsigned short utf16[]={0x41,0x20ac,0xd83d,0xde00};const unsigned int want[]={0x41,0x20ac,0x1f600};
 const char utf8[]="A\xe2\x82\xac\xf0\x9f\x98\x80";plutovg_text_iterator_t it;unsigned i;
 plutovg_text_iterator_init(&it,utf8,-1,PLUTOVG_TEXT_ENCODING_UTF8);
 for(i=0;i<3;i++){CHECK(plutovg_text_iterator_has_next(&it));CHECK(plutovg_text_iterator_next(&it)==want[i]);}CHECK(!plutovg_text_iterator_has_next(&it));
 plutovg_text_iterator_init(&it,utf16,4,PLUTOVG_TEXT_ENCODING_UTF16);
 for(i=0;i<3;i++){CHECK(plutovg_text_iterator_has_next(&it));CHECK(plutovg_text_iterator_next(&it)==want[i]);}CHECK(!plutovg_text_iterator_has_next(&it));puts("PASS unicode");
}
static uint32_t pixel(plutovg_surface_t* s,int x,int y)
{ uint32_t v;memcpy(&v,plutovg_surface_get_data(s)+y*plutovg_surface_get_stride(s)+4*x,4);return v; }
static void draw(const char* output)
{
 plutovg_surface_t* s=plutovg_surface_create(16,16);CHECK(s);plutovg_canvas_t* c=plutovg_canvas_create(s);CHECK(c);
 CHECK(plutovg_canvas_get_surface(c)==s);plutovg_canvas_save(c);plutovg_canvas_clip_rect(c,4,4,8,8);
 plutovg_canvas_set_rgb(c,1,0,0);plutovg_canvas_paint(c);CHECK(pixel(s,8,8)==0xffff0000u && pixel(s,1,1)==0);
 CHECK(plutovg_canvas_clip_contains(c,8,8)&&!plutovg_canvas_clip_contains(c,1,1));plutovg_canvas_restore(c);
 plutovg_canvas_set_rgb(c,0,0,1);plutovg_canvas_fill_rect(c,0,0,2,2);CHECK(pixel(s,1,1)==0xff0000ffu);
 CHECK(plutovg_surface_write_to_png(s,output));plutovg_surface_t* q=plutovg_surface_load_from_image_file(output);CHECK(q);
 CHECK(plutovg_surface_get_width(q)==16&&plutovg_surface_get_height(q)==16&&pixel(q,8,8)==0xffff0000u&&pixel(q,1,1)==0xff0000ffu&&pixel(q,15,15)==0);
 unsigned char rgba[4]={100,50,20,255},argb[4],back[4];plutovg_convert_rgba_to_argb(argb,rgba,1,1,4);plutovg_convert_argb_to_rgba(back,argb,1,1,4);CHECK(!memcmp(rgba,back,4));
 plutovg_surface_destroy(q);plutovg_canvas_destroy(c);plutovg_surface_destroy(s);puts("PASS surfaces-clip-png");
}
int main(int argc,char**argv)
{
 CHECK(argc==4);version_lifetime();matrices();paths();colors();unicode();draw(argv[3]);font_checks(argv[1],argv[2]);puts("PASS all-seven-groups");return 0;
}
OWNED_PLUTOVG_ASSET_0
cat > .packaging-qa/assets/font.c <<'OWNED_PLUTOVG_ASSET_1'
/* SPDX-License-Identifier: Apache-2.0 */
#include <plutovg.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#ifndef PLUTOVG_BUILD_STATIC
#error "Static imported SDK definition missing in second translation unit"
#endif
#define CHECK(x) do { if(!(x)) { fprintf(stderr,"FONT:%%d:%%s\n",__LINE__,#x); exit(1); } } while(0)
void font_checks(const char* font,const char* fontdir)
{
 plutovg_font_face_t* f=plutovg_font_face_load_from_file(font,0);CHECK(f);CHECK(plutovg_font_face_get_reference_count(f)==1);
 CHECK(plutovg_font_face_reference(f)==f && plutovg_font_face_get_reference_count(f)==2);plutovg_font_face_destroy(f);
 float a,d,g,advance,bearing;plutovg_rect_t r;
 plutovg_font_face_get_metrics(f,24,&a,&d,&g,&r);CHECK(isfinite(a)&&a>0&&isfinite(d)&&d<0&&r.w>0&&r.h>0);
 plutovg_font_face_get_glyph_metrics(f,24,'A',&advance,&bearing,&r);CHECK(advance>0&&r.w>0&&r.h>0);
 plutovg_path_t* p=plutovg_path_create();CHECK(p);CHECK(plutovg_font_face_get_glyph_path(f,24,0,24,'A',p)>0&&plutovg_path_length(p)>0);plutovg_path_destroy(p);
 float text=plutovg_font_face_text_extents(f,24,"A\xe2\x82\xac",-1,PLUTOVG_TEXT_ENCODING_UTF8,&r);CHECK(text>advance&&r.w>0&&r.h>0);
 plutovg_font_face_cache_t* cache=plutovg_font_face_cache_create();CHECK(cache&&plutovg_font_face_cache_reference_count(cache)==1);
 CHECK(plutovg_font_face_cache_reference(cache)==cache&&plutovg_font_face_cache_reference_count(cache)==2);plutovg_font_face_cache_destroy(cache);
 plutovg_font_face_cache_add(cache,"Owned alias",false,false,f);CHECK(plutovg_font_face_cache_get(cache,"Owned alias",false,false)==f);
 CHECK(!plutovg_font_face_cache_get(cache,"Missing family",false,false));plutovg_font_face_cache_reset(cache);CHECK(!plutovg_font_face_cache_get(cache,"Owned alias",false,false));
 CHECK(plutovg_font_face_cache_add_file(cache,"File alias",false,false,font,0));CHECK(plutovg_font_face_cache_get(cache,"File alias",false,false));plutovg_font_face_cache_reset(cache);
 CHECK(plutovg_font_face_cache_load_file(cache,font)==1);CHECK(plutovg_font_face_cache_get(cache,"DejaVu Sans",false,false));plutovg_font_face_cache_reset(cache);
 CHECK(plutovg_font_face_cache_load_dir(cache,fontdir)==1);CHECK(plutovg_font_face_cache_get(cache,"DejaVu Sans",false,false));
 plutovg_surface_t* s=plutovg_surface_create(128,48);CHECK(s);plutovg_canvas_t* c=plutovg_canvas_create(s);CHECK(c);
 plutovg_canvas_set_font_face_cache(c,cache);CHECK(plutovg_canvas_get_font_face_cache(c)==cache);CHECK(plutovg_canvas_select_font_face(c,"DejaVu Sans",false,false));
 plutovg_canvas_set_font_size(c,24);CHECK(plutovg_canvas_get_font_size(c)==24&&plutovg_canvas_get_font_face(c));plutovg_canvas_set_rgb(c,0,1,0);
 CHECK(plutovg_canvas_fill_text(c,"A\xe2\x82\xac",-1,PLUTOVG_TEXT_ENCODING_UTF8,4,30)>0);
 unsigned pixels=0;for(int y=0;y<48;y++)for(int x=0;x<128;x++){uint32_t v;memcpy(&v,plutovg_surface_get_data(s)+y*plutovg_surface_get_stride(s)+4*x,4);if(v>>24)pixels++;}CHECK(pixels>20&&pixels<128*48);
 plutovg_canvas_destroy(c);plutovg_surface_destroy(s);plutovg_font_face_cache_destroy(cache);plutovg_font_face_destroy(f);puts("PASS fonts-text-cache-load");
}
OWNED_PLUTOVG_ASSET_1
cat > .packaging-qa/assets/CMakeLists.txt <<'OWNED_PLUTOVG_ASSET_2'
cmake_minimum_required(VERSION 3.20)
project(plutovg_owned_consumer C)
if(NOT SDK_PREFIX OR NOT OWNED_C_STANDARD MATCHES "^(99|11)$")
  message(FATAL_ERROR "exact SDK_PREFIX and C99/C11 required")
endif()
set(CMAKE_FIND_USE_PACKAGE_REGISTRY OFF)
set(CMAKE_FIND_USE_SYSTEM_PACKAGE_REGISTRY OFF)
find_package(plutovg 1.3.3 EXACT CONFIG REQUIRED PATHS "${SDK_PREFIX}/lib64/cmake/plutovg" NO_DEFAULT_PATH)
get_target_property(owned_type plutovg::plutovg TYPE)
if(NOT owned_type STREQUAL "STATIC_LIBRARY")
  message(FATAL_ERROR "native static target expected")
endif()
get_target_property(owned_configs plutovg::plutovg IMPORTED_CONFIGURATIONS)
if(NOT owned_configs)
  message(FATAL_ERROR "missing imported static configuration")
endif()
foreach(owned_config IN LISTS owned_configs)
  get_target_property(owned_path plutovg::plutovg "IMPORTED_LOCATION_${owned_config}")
  file(REAL_PATH "${owned_path}" owned_real)
  file(REAL_PATH "${SDK_PREFIX}/lib64/libplutovg.a" owned_want)
  if(NOT owned_real STREQUAL owned_want)
    message(FATAL_ERROR "foreign imported archive")
  endif()
endforeach()
add_executable(consumer consumer.c font.c)
set_target_properties(consumer PROPERTIES C_STANDARD ${OWNED_C_STANDARD} C_STANDARD_REQUIRED ON C_EXTENSIONS OFF)
target_compile_options(consumer PRIVATE -Wall -Wextra -Werror -UNDEBUG -H)
target_link_libraries(consumer PRIVATE plutovg::plutovg)
target_link_options(consumer PRIVATE "-Wl,-Map=${CMAKE_BINARY_DIR}/consumer.map" -Wl,-t)
OWNED_PLUTOVG_ASSET_2
cat > .packaging-qa/assets/run-qa.py <<'OWNED_PLUTOVG_ASSET_3'
#!/usr/bin/python3
# SPDX-License-Identifier: Apache-2.0
"""Target-only static SDK validation. No local execution is authorized by drafting this file."""
import argparse,base64,gzip,hashlib,json,os,pathlib,re,shlex,shutil,struct,subprocess,time,zlib
P=pathlib.Path
ap=argparse.ArgumentParser();ap.add_argument('--prefix',required=True);ap.add_argument('--phase',choices=['build','installed'],required=True);ap.add_argument('--output',required=True);ap.add_argument('--font-contract',required=True);ap.add_argument('--smiley');a=ap.parse_args()
assets=P(__file__).resolve().parent;prefix=P(a.prefix).resolve();out=P(a.output).absolute();out.mkdir(parents=True,exist_ok=False)
records=[];failure=None;start=time.time();env=os.environ.copy()
for key in list(env):
 if key in {'CC','CXX','CPP','CFLAGS','CPPFLAGS','CXXFLAGS','LDFLAGS','LIBS','CPATH','C_INCLUDE_PATH','CPLUS_INCLUDE_PATH','OBJC_INCLUDE_PATH','LIBRARY_PATH','GCC_EXEC_PREFIX','COMPILER_PATH','LD_LIBRARY_PATH','LD_PRELOAD','CMAKE_PREFIX_PATH','CMAKE_TOOLCHAIN_FILE','CMAKE_PROJECT_INCLUDE','CMAKE_PROJECT_INCLUDE_BEFORE','PKG_CONFIG_PATH','PKG_CONFIG_LIBDIR','PKG_CONFIG_SYSROOT_DIR','CONFIG_SITE','PYTHONPATH','PYTHONHOME'} or key.startswith('BASH_FUNC_'):env.pop(key,None)
env.update(PATH='/usr/bin:/bin',LC_ALL='C',LANG='C',TZ='UTC',HOME=str(out/'home'));(out/'home').mkdir()
def sha(p):return hashlib.sha256(P(p).read_bytes()).hexdigest()
def run(label,argv,cwd=None,extra=None,timeout=120,want=0):
 assert not any(r['label']==label for r in records);en=env.copy();en.update(extra or {});cwd=P(cwd or out);t=time.time()
 try:
  r=subprocess.run(argv,cwd=cwd,env=en,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=timeout,check=False);stdout,stderr,code,timed=r.stdout,r.stderr,r.returncode,False
 except subprocess.TimeoutExpired as ex:stdout,stderr,code,timed=ex.stdout or b'',ex.stderr or b'',124,True
 (out/(label+'.stdout')).write_bytes(stdout);(out/(label+'.stderr')).write_bytes(stderr);row=dict(label=label,argv=list(map(str,argv)),cwd=str(cwd),exit=code,timed_out=timed,elapsed=time.time()-t,stdout_sha256=hashlib.sha256(stdout).hexdigest(),stderr_sha256=hashlib.sha256(stderr).hexdigest(),stdout_bytes=len(stdout),stderr_bytes=len(stderr));records.append(row)
 assert code==want and not timed,(label,code,want);return stdout,stderr
def png(path):
 raw=P(path).read_bytes();assert raw[:8]==b'\x89PNG\r\n\x1a\n';pos=8;data=b'';ihdr=None;ended=False
 while pos<len(raw):
  n=struct.unpack_from('>I',raw,pos)[0];kind=raw[pos+4:pos+8];body=raw[pos+8:pos+8+n];assert n<=10_000_000 and len(body)==n and struct.unpack_from('>I',raw,pos+8+n)[0]==zlib.crc32(kind+body)&0xffffffff;pos+=12+n
  if kind==b'IHDR':assert ihdr is None;ihdr=struct.unpack('>IIBBBBB',body)
  elif kind==b'IDAT':data+=body
  elif kind==b'IEND':assert n==0;ended=True;break
  else:assert not (kind[0]&32)==0 or kind in {b'PLTE'}
 assert ended and pos==len(raw) and ihdr is not None;w,h,depth,color,comp,filt,interlace=ihdr;assert depth==8 and color==6 and comp==filt==interlace==0 and 0<w<=4096 and 0<h<=4096;stride=w*4;decoder=zlib.decompressobj();pixels=decoder.decompress(data,(stride+1)*h+1);assert decoder.eof and not decoder.unused_data and len(pixels)==(stride+1)*h;rows=[];prior=bytearray(stride)
 for y in range(h):
  f=pixels[y*(stride+1)];src=pixels[y*(stride+1)+1:(y+1)*(stride+1)];row=bytearray(stride);assert 0<=f<=4
  for x,v in enumerate(src):
   left=row[x-4] if x>=4 else 0;up=prior[x];corner=prior[x-4] if x>=4 else 0
   if f==0:predict=0
   elif f==1:predict=left
   elif f==2:predict=up
   elif f==3:predict=(left+up)//2
   else:
    p=left+up-corner;dl,du,dc=abs(p-left),abs(p-up),abs(p-corner);predict=left if dl<=du and dl<=dc else up if du<=dc else corner
   row[x]=(v+predict)&255
  rows.append(bytes(row));prior=row
 return w,h,lambda x,y:tuple(rows[y][4*x:4*x+4])
def smiley_pixels(path):
 w,h,p=png(path);assert (w,h)==(150,150)
 anchors={(0,0):(0,0,0,0),(149,149):(0,0,0,0),(75,30):(255,255,0,255),(75,75):(255,255,0,255),(50,55):(0,0,0,255),(100,55):(0,0,0,255),(75,124):(0,0,0,255)}
 assert all(p(x,y)==value for (x,y),value in anchors.items());return {'width':w,'height':h,'sha256':sha(path),'anchors':{str(k):v for k,v in anchors.items()}}
expected=b'PASS version-lifetime\nPASS matrices\nPASS paths\nPASS colors-paints\nPASS unicode\nPASS surfaces-clip-png\nPASS fonts-text-cache-load\nPASS all-seven-groups\n'
try:
 contract=json.loads(P(a.font_contract).read_text());font=P(contract['font_path']);assert contract['package']=='dejavu-fonts' and contract['version']=='2.37' and contract['release']=='3.oe2403sp3' and contract['arch']=='noarch' and contract['RPM_sha256']=='5480f8aaf5cad71bfe5e375f03109b7f88e8866467eeafd8cbedc3841eace6b2' and sha(font)==contract['font_sha256'] and font.stat().st_size==contract['font_bytes'];fontdir=out/'font-input';fontdir.mkdir();shutil.copyfile(font,fontdir/'DejaVuSans.ttf');assert sha(fontdir/'DejaVuSans.ttf')==sha(font)
 production=[prefix/'include/plutovg/plutovg.h',prefix/'lib64/libplutovg.a',prefix/'lib64/pkgconfig/plutovg.pc']+sorted((prefix/'lib64/cmake/plutovg').glob('*.cmake'));assert len(production)>=7 and all(p.is_file() and not p.is_symlink() for p in production);before={str(p.relative_to(prefix)):sha(p) for p in production};assert not list((prefix/'lib64').glob('libplutovg.so*'))
 for tool in ['gcc','cmake','pkgconf','ar','readelf']:run('version-'+tool,['/usr/bin/'+tool,'--version'])
 archive=prefix/'lib64/libplutovg.a';names=run('archive-members',['/usr/bin/ar','t',str(archive)])[0].decode().splitlines();assert len(names)==len(set(names))==11 and all('/' not in n and n.endswith('.o') for n in names);archive_members=[]
 for i,name in enumerate(names):
  b=run('archive-member-'+str(i),['/usr/bin/ar','p',str(archive),name])[0];path=out/('member-'+str(i)+'.o');path.write_bytes(b);header=run('archive-ELF-'+str(i),['/usr/bin/readelf','-W','-h',str(path)])[0].decode();assert 'ELF64' in header and 'little endian' in header and re.search(r'Type:\s+REL\b',header) and 'RISC-V' in header;archive_members.append(dict(name=name,sha256=sha(path),bytes=len(b)))
 relocated=out/'relocated-sdk';relocated.mkdir()
 for p in production:dest=relocated/p.relative_to(prefix);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dest);assert sha(dest)==sha(p)
 proofs=[]
 for layout,sdk in [('installed',prefix),('relocated',relocated)]:
  sdk=sdk.resolve();archive=(sdk/'lib64/libplutovg.a').resolve();header=(sdk/'include/plutovg/plutovg.h').resolve();pcenv={'PKG_CONFIG_LIBDIR':str(sdk/'lib64/pkgconfig'),'PKG_CONFIG_PATH':'','PKG_CONFIG_SYSROOT_DIR':''};assert run(layout+'-pc-version',['/usr/bin/pkgconf','--modversion','plutovg'],extra=pcenv)[0].strip()==b'1.3.3';pcdir=run(layout+'-pc-directory',['/usr/bin/pkgconf','--variable=pcfiledir','plutovg'],extra=pcenv)[0].decode().strip();assert P(pcdir).resolve()==sdk/'lib64/pkgconfig';flags=shlex.split(run(layout+'-pc-static-flags',['/usr/bin/pkgconf','--cflags','--libs','--static','plutovg'],extra=pcenv)[0].decode());assert '-DPLUTOVG_BUILD_STATIC' in flags and '-lplutovg' in flags
  for standard in ['99','11']:
   for route in ['pkgconf','cmake']:
    label=layout+'-c'+standard+'-'+route;build=out/label;build.mkdir();binary=build/'consumer';mapfile=build/'consumer.map'
    if route=='pkgconf':
     run(label+'-compile',['/usr/bin/gcc','-std=c'+standard,'-Wall','-Wextra','-Werror','-UNDEBUG','-H',str(assets/'consumer.c'),str(assets/'font.c'),'-o',str(binary),'-Wl,-Map='+str(mapfile),'-Wl,-t']+flags)
    else:
     run(label+'-configure',['/usr/bin/cmake','-S',str(assets),'-B',str(build),'-DCMAKE_C_COMPILER=/usr/bin/gcc','-DCMAKE_EXPORT_COMPILE_COMMANDS=ON','-DSDK_PREFIX='+str(sdk),'-DOWNED_C_STANDARD='+standard]);run(label+'-compile',['/usr/bin/cmake','--build',str(build),'--parallel','2','--verbose']);commands=json.loads((build/'compile_commands.json').read_text());assert len(commands)==2 and all('-DPLUTOVG_BUILD_STATIC' in c['command'] and '-std=c'+standard in c['command'] and str(sdk/'include/plutovg') in c['command'] for c in commands)
    trace=(out/(label+'-compile.stdout')).read_text()+(out/(label+'-compile.stderr')).read_text()
    maploads=re.findall(r'^LOAD (.+libplutovg[.]a)$',mapfile.read_text(),re.M)
    actual_archives=[line.strip() for line in trace.splitlines() if line.strip().endswith('/libplutovg.a') and not any(c in line.strip() for c in [' ','\t'])]
    assert len(maploads)==1 and actual_archives and all(P(p).is_file() and os.path.samefile(p,archive) for p in maploads+actual_archives)
    actual_headers=[m.group(1) for line in trace.splitlines() if (m:=re.match(r'^[.]+\s+(.+plutovg[.]h)$',line))]
    assert len(actual_headers)>=2 and all(P(p).is_file() and os.path.samefile(p,header) for p in actual_headers)
    dependencies=run(label+'-headers',['/usr/bin/gcc','-std=c'+standard,'-MM','-DPLUTOVG_BUILD_STATIC','-I'+str(sdk/'include/plutovg'),str(assets/'consumer.c'),str(assets/'font.c')])[0].decode();assert str(header) in dependencies
    elf=run(label+'-ELF',['/usr/bin/readelf','-W','-h','-d',str(binary)])[0].decode();assert 'ELF64' in elf and 'RISC-V' in elf and not re.search(r'NEEDED.*libplutovg',elf)
    image=build/'consumer.png';stdout,stderr=run(label+'-run',[str(binary),str(font),str(fontdir),str(image)],timeout=90);assert stdout==expected and stderr==b'';w,h,p=png(image);assert (w,h)==(16,16) and p(8,8)==(255,0,0,255) and p(1,1)==(0,0,255,255) and p(15,15)==(0,0,0,0);proofs.append(dict(layout=layout,standard=standard,route=route,binary_sha256=sha(binary),archive_path=str(archive),archive_sha256=sha(archive),header_sha256=sha(header),map_sha256=sha(mapfile),recorded_map_LOAD_paths=maploads,recorded_link_trace_paths=actual_archives,recorded_GCC_header_paths=actual_headers,target_samefile_archive_and_header=True,PNG_sha256=sha(image),groups=7,stdout_sha256=hashlib.sha256(stdout).hexdigest()))
  # A positive compile precedes each deliberate failure; no fallback SDK search.
  missing=out/(layout+'-missing-header.c');missing.write_text('#include <plutovg.h>\nint main(void){return plutovg_version()==0;}\n');neg=run(layout+'-negative-header',['/usr/bin/gcc','-std=c99','-c',str(missing),'-o',str(out/(layout+'-missing-header.o'))],want=1);assert b'plutovg.h' in neg[1] and b'No such file or directory' in neg[1]
  empty=out/(layout+'-empty.a');run(layout+'-empty-archive',['/usr/bin/ar','rc',str(empty)]);neg=run(layout+'-negative-library',['/usr/bin/gcc','-std=c99','-DPLUTOVG_BUILD_STATIC','-I'+str(sdk/'include/plutovg'),str(missing),str(empty),'-o',str(out/(layout+'-missing-library'))],want=1);assert b'undefined reference' in neg[1] and b'plutovg_version' in neg[1]
 # The original source is copied byte-for-byte to owned test data, not altered.
 original=assets/'smiley.c';assert sha(original)=='cfe4489d5d28dbd535d46e9603ea882a561d67fc311acadbc971e33342924d3e'
 smiley=out/'smiley';run('original-smiley-compile',['/usr/bin/gcc','-std=c11',str(original),'-o',str(smiley)]+flags);run('original-smiley-execute',[str(smiley)]);smiley_result=smiley_pixels(out/'smiley.png')
 if a.phase=='build':
  assert a.smiley;native=out/'native-smiley';native.mkdir();run('native-default-smiley',[str(P(a.smiley).resolve())],cwd=native);smiley_result['native_default']=smiley_pixels(native/'smiley.png')
 assert {str(p.relative_to(prefix)):sha(p) for p in production}==before;assert len(proofs)==8
except BaseException as ex:failure={'type':type(ex).__name__,'message':str(ex)};raise
finally:
 raw={p.name:base64.b64encode(p.read_bytes()).decode() for p in out.iterdir() if p.is_file() and p.suffix in {'.stdout','.stderr'}}
 maps={str(p.relative_to(out)):base64.b64encode(p.read_bytes()).decode() for p in out.rglob('*') if p.is_file() and p.name in {'consumer.map','compile_commands.json'}}
 result=dict(schema_version=1,phase=a.phase,prefix=str(prefix),failure=failure,commands=records,elapsed=time.time()-start,target_validation_only=True,positive_matrix=locals().get('proofs',[]),original_smiley=locals().get('smiley_result'),font_contract=locals().get('contract'),archive_members=locals().get('archive_members',[]),production_before=locals().get('before',{}),production_after={str(p.relative_to(prefix)):sha(p) for p in locals().get('production',[])},font_redistributed=False,raw_streams_base64=raw,link_maps_and_compile_commands_base64=maps)
 encoded=json.dumps(result,sort_keys=True,separators=(',',':')).encode();(out/'result.json').write_bytes(encoded+b'\n');print('PLUTOVG_OWNED_QA_GZIP_BASE64 '+base64.b64encode(gzip.compress(encoded,mtime=0)).decode(),flush=True)
OWNED_PLUTOVG_ASSET_3
cat > .packaging-qa/assets/source-check.py <<'OWNED_PLUTOVG_ASSET_4'
#!/usr/bin/python3
# SPDX-License-Identifier: Apache-2.0
"""Target byte preservation and cache/defaults validation, no source importing."""
import argparse,hashlib,json,pathlib
ap=argparse.ArgumentParser();ap.add_argument('root');ap.add_argument('manifest');ap.add_argument('--cache');a=ap.parse_args();root=pathlib.Path(a.root).resolve();expected=json.loads(pathlib.Path(a.manifest).read_text())['files'];actual={str(p.relative_to(root)):p for p in root.rglob('*') if p.is_file() and '.packaging-qa' not in p.relative_to(root).parts};assert set(actual)==set(expected)
for path,row in expected.items():
 p=actual[path];assert not p.is_symlink() and p.stat().st_size==row['bytes'] and hashlib.sha256(p.read_bytes()).hexdigest()==row['sha256']
if a.cache:
 cache={line.split('=',1)[0]:line.split('=',1)[1] for line in pathlib.Path(a.cache).read_text().splitlines() if '=' in line and not line.startswith(('#','//'))};assert cache['PLUTOVG_BUILD_EXAMPLES:BOOL']=='ON' and cache['PLUTOVG_DISABLE_FONT_FACE_CACHE_LOAD:BOOL']=='OFF' and cache.get('BUILD_SHARED_LIBS:BOOL','OFF') in {'OFF','FALSE','0'}
print(json.dumps({'source_files':len(expected),'source_snapshot':'original' if pathlib.Path(a.manifest).name=='source-manifest.json' else 'package-patched','all_source_files_match_manifest':True,'manifest_sha256':hashlib.sha256(pathlib.Path(a.manifest).read_bytes()).hexdigest(),'native_static_default':bool(a.cache),'font_cache_load_enabled':bool(a.cache),'original_example_enabled':bool(a.cache)}))
OWNED_PLUTOVG_ASSET_4
cat > .packaging-qa/assets/smiley.c <<'OWNED_PLUTOVG_ASSET_5'
#include <plutovg.h>

int main(void)
{
    const int width = 150;
    const int height = 150;

    const float center_x = width / 2.f;
    const float center_y = height / 2.f;
    const float face_radius = 70;
    const float mouth_radius = 50;
    const float eye_radius = 10;
    const float eye_offset_x = 25;
    const float eye_offset_y = 20;
    const float eye_x = center_x - eye_offset_x;
    const float eye_y = center_y - eye_offset_y;

    plutovg_surface_t* surface = plutovg_surface_create(width, height);
    plutovg_canvas_t* canvas = plutovg_canvas_create(surface);

    plutovg_canvas_save(canvas);
    plutovg_canvas_arc(canvas, center_x, center_y, face_radius, 0, PLUTOVG_TWO_PI, 0);
    plutovg_canvas_set_rgb(canvas, 1, 1, 0);
    plutovg_canvas_fill_preserve(canvas);
    plutovg_canvas_set_rgb(canvas, 0, 0, 0);
    plutovg_canvas_set_line_width(canvas, 5);
    plutovg_canvas_stroke(canvas);
    plutovg_canvas_restore(canvas);

    plutovg_canvas_save(canvas);
    plutovg_canvas_arc(canvas, eye_x, eye_y, eye_radius, 0, PLUTOVG_TWO_PI, 0);
    plutovg_canvas_arc(canvas, center_x + eye_offset_x, eye_y, eye_radius, 0, PLUTOVG_TWO_PI, 0);
    plutovg_canvas_set_rgb(canvas, 0, 0, 0);
    plutovg_canvas_fill(canvas);
    plutovg_canvas_restore(canvas);

    plutovg_canvas_save(canvas);
    plutovg_canvas_arc(canvas, center_x, center_y, mouth_radius, 0, PLUTOVG_PI, 0);
    plutovg_canvas_set_rgb(canvas, 0, 0, 0);
    plutovg_canvas_set_line_width(canvas, 5);
    plutovg_canvas_stroke(canvas);
    plutovg_canvas_restore(canvas);

    plutovg_surface_write_to_png(surface, "smiley.png");
    plutovg_canvas_destroy(canvas);
    plutovg_surface_destroy(surface);
    return 0;
}
OWNED_PLUTOVG_ASSET_5
cat > .packaging-qa/assets/source-manifest.json <<'OWNED_PLUTOVG_ASSET_6'
{
  "files": {
    ".github/FUNDING.yml": {
      "bytes": 65,
      "git_mode": "100644",
      "sha256": "ca5204e42a97ea7e42fd93c7b9c7534f4fb81a9b66b7ae9bedbf1f904d247f1a"
    },
    ".github/workflows/main.yml": {
      "bytes": 1190,
      "git_mode": "100644",
      "sha256": "bdb60185e933ea990a2bde7e74c17bcda3b07da9cc6925a5b1f2bacec948e4e7"
    },
    ".gitignore": {
      "bytes": 14,
      "git_mode": "100644",
      "sha256": "d93373b397a89e67d540c345c03ad326bada497e3048c74d08ff10427b93cb69"
    },
    "CMakeLists.txt": {
      "bytes": 4705,
      "git_mode": "100644",
      "sha256": "ce844bdd113855506dbda345617151b76018d32032adf8dff88958b482e7d11f"
    },
    "LICENSE": {
      "bytes": 1104,
      "git_mode": "100644",
      "sha256": "a55d1e78eaf75779c336b4ba061e74aae56a21195d234474fb24a398935d6ce1"
    },
    "README.md": {
      "bytes": 3086,
      "git_mode": "100644",
      "sha256": "4e084a4c54f05c3c555d444e9375e18da3f7f66612a9c300d81afffb977e856d"
    },
    "cmake/plutovgConfig.cmake.in": {
      "bytes": 134,
      "git_mode": "100644",
      "sha256": "a03263b5901fb32549448976e20a2867c0b4e117fb2fe6ca9ee4696fbf516e08"
    },
    "examples/CMakeLists.txt": {
      "bytes": 70,
      "git_mode": "100644",
      "sha256": "08f7a5606be40602a1c787258a09f135d3cd1943f8213d23a1c45e9bc3318413"
    },
    "examples/meson.build": {
      "bytes": 60,
      "git_mode": "100644",
      "sha256": "a3b172abccc96871fc040ee4bfe2b6a7f848a619ff9076a7e8ba430ba0372e0c"
    },
    "examples/smiley.c": {
      "bytes": 1706,
      "git_mode": "100644",
      "sha256": "cfe4489d5d28dbd535d46e9603ea882a561d67fc311acadbc971e33342924d3e"
    },
    "include/plutovg.h": {
      "bytes": 101310,
      "git_mode": "100644",
      "sha256": "a12290cb45a53a1b42a527f1c00f214c63f25d8dcc1f37bd9f7bf3c4d3a0e21f"
    },
    "meson.build": {
      "bytes": 2226,
      "git_mode": "100644",
      "sha256": "bc68c105b4fb336b3e03c6577787d6ac364800449f5b4203a8398d2bf9a3c6da"
    },
    "meson_options.txt": {
      "bytes": 257,
      "git_mode": "100644",
      "sha256": "93b68aa3bd0f4ba074fe762634d019a74998df9d9c5447706f3bb99d4dbb4fb5"
    },
    "smiley.png": {
      "bytes": 6392,
      "git_mode": "100644",
      "sha256": "5e3fd2ad55bf616a0718af2f4323ef9032a0cfc6236838bf1d4ba134c25497f7"
    },
    "source/FTL.TXT": {
      "bytes": 6718,
      "git_mode": "100644",
      "sha256": "e60d07dfb2c5264f9f405fa52bf0d4f85429dd9ae1bc2ffcff8af1924ef720d1"
    },
    "source/plutovg-blend.c": {
      "bytes": 38324,
      "git_mode": "100644",
      "sha256": "3da9df7f69631fd9a907b8066b4e102bf7e0b93f134197d1d746201a82c2aa5a"
    },
    "source/plutovg-canvas.c": {
      "bytes": 25303,
      "git_mode": "100644",
      "sha256": "ddada462dd66f9f856a85e6ed13fe5ab65838a2b84d6a4f6a14bd36896861061"
    },
    "source/plutovg-font.c": {
      "bytes": 35946,
      "git_mode": "100644",
      "sha256": "e121cbbb3930a1812d4c2a2ab2ee930003092064e79d869420dcb267979d93c9"
    },
    "source/plutovg-ft-math.c": {
      "bytes": 11731,
      "git_mode": "100644",
      "sha256": "02a1b5faf07a0ce6f4af2001fb6fa887a3682c2a2cbc9b2454894d8f930612e6"
    },
    "source/plutovg-ft-math.h": {
      "bytes": 14096,
      "git_mode": "100644",
      "sha256": "9d1b12c8e2cda360fc591d0dea879462e4fcf3628e27d31aa9ca223b6309414d"
    },
    "source/plutovg-ft-raster.c": {
      "bytes": 55979,
      "git_mode": "100644",
      "sha256": "258f9750abf096e3916a4678788a1310007733335ee3644a98b0f1bf3bef8271"
    },
    "source/plutovg-ft-raster.h": {
      "bytes": 27166,
      "git_mode": "100644",
      "sha256": "cb065904566f2313f61dbd64be817d4da2944fb5fff391a12bd9b3be3f19be4d"
    },
    "source/plutovg-ft-stroker.c": {
      "bytes": 61890,
      "git_mode": "100644",
      "sha256": "d6a4a5ef92b2395bd9e7a93441f2b5c438d632640d450ea84b2228f20ca9cc96"
    },
    "source/plutovg-ft-stroker.h": {
      "bytes": 9582,
      "git_mode": "100644",
      "sha256": "519c1487a65c3f515afd25ff752038e5ffbd3beee02038302fd61dc87c5e9695"
    },
    "source/plutovg-ft-types.h": {
      "bytes": 8973,
      "git_mode": "100644",
      "sha256": "801a879039ab7ffb5c6049eb3a4e364fdac03d1d22349d7f6f3bc9e35ae9732b"
    },
    "source/plutovg-matrix.c": {
      "bytes": 7576,
      "git_mode": "100644",
      "sha256": "d9ce4a5ef62ed3b01582d6e7d5fad2dbb895f98b1754a33575b66ef73ebd1126"
    },
    "source/plutovg-paint.c": {
      "bytes": 17701,
      "git_mode": "100644",
      "sha256": "fa9fbeb8e8bd4a438b0a32762a6af67fd4e5957c035ec8c5830942f96bbe2a88"
    },
    "source/plutovg-path.c": {
      "bytes": 31305,
      "git_mode": "100644",
      "sha256": "5d2eaec19062a1c2ba336bccfca1bdd20828dce7fa669a21882cbb0a0c5c7276"
    },
    "source/plutovg-private.h": {
      "bytes": 5147,
      "git_mode": "100644",
      "sha256": "536185040b85c07482d04a85d2d67c04cc228fa9ed6ed1351af2f8728db98ba1"
    },
    "source/plutovg-rasterize.c": {
      "bytes": 12997,
      "git_mode": "100644",
      "sha256": "49bf5959ad21930c7f9dc17d7fc9b662b4a53b78ece63c93b2ad1eea667ef4e3"
    },
    "source/plutovg-stb-image-write.h": {
      "bytes": 71221,
      "git_mode": "100644",
      "sha256": "fc1f2db67a6914bd34250f34fe64b776f08d6a19b9b97bcc25dafb5973546010"
    },
    "source/plutovg-stb-image.h": {
      "bytes": 282995,
      "git_mode": "100644",
      "sha256": "e3ce9e557d85e689bac5f8fcd1624da739508c661a84f7f6cda879b565854ff1"
    },
    "source/plutovg-stb-truetype.h": {
      "bytes": 199009,
      "git_mode": "100644",
      "sha256": "92dd46ffcbeccad84898fddeb0eff9ab5dccfc46a9f43e7809f743df4d19f93c"
    },
    "source/plutovg-surface.c": {
      "bytes": 10069,
      "git_mode": "100644",
      "sha256": "7a2f033daa045a126747eb8b96c242a72c37c1c833fe336c3d8443754371c698"
    },
    "source/plutovg-utils.h": {
      "bytes": 5809,
      "git_mode": "100644",
      "sha256": "3a6ecf3fb9211c0a8c235aaa23b3bf4fd58e7149ec47356353d0698ded7b5b84"
    }
  },
  "source_archive_sha256": "f9bb31ff305381b79bb920730017bd356e5043a215960dd83656c70036075a4e"
}
OWNED_PLUTOVG_ASSET_6
cat > .packaging-qa/assets/FreeType-acknowledgement.txt <<'OWNED_PLUTOVG_ASSET_7'
FreeType acknowledgement and downstream changes statement

This software is based in part on the work of the FreeType Team.
Portions of this software are copyright (C) 1996-2020 The FreeType
Project (www.freetype.org). All rights reserved.

The seven original plutovg-ft-*.c/h files retain their exact original
David Turner, Robert Wilhelm, and Werner Lemberg notices and years.
The unmodified original FTL.TXT is installed byte-for-byte, not transcoded.
This package changes only source/plutovg-font.c to fix generic UTF-16
surrogate lookahead. The seven FT-derived files and three STB headers
remain unchanged. All 35 original files are retained as source notices.
Packaging-owned SDK consumers and checks are additive, outside upstream.
No endorsement, personal warranty, or separate CERT permission is claimed.
The three STB headers are used under their explicit MIT alternative A;
both original offered alternatives and all embedded attributions remain.
The DejaVu font is an external runtime/build dependency, not redistributed
in this package. Its own package retains its Bitstream Vera/PD attribution.
OWNED_PLUTOVG_ASSET_7
cat > .packaging-qa/assets/rights-ledger.json <<'OWNED_PLUTOVG_ASSET_8'
{
  "binary_acknowledgement": "FreeType acknowledgement and downstream changes statement\n\nThis software is based in part on the work of the FreeType Team.\nPortions of this software are copyright (C) 1996-2020 The FreeType\nProject (www.freetype.org). All rights reserved.\n\nThe seven original plutovg-ft-*.c/h files retain their exact original\nDavid Turner, Robert Wilhelm, and Werner Lemberg notices and years.\nThe unmodified original FTL.TXT is installed byte-for-byte, not transcoded.\nThis package changes only source/plutovg-font.c to fix generic UTF-16\nsurrogate lookahead. The seven FT-derived files and three STB headers\nremain unchanged. All 35 original files are retained as source notices.\nPackaging-owned SDK consumers and checks are additive, outside upstream.\nNo endorsement, personal warranty, or separate CERT permission is claimed.\nThe three STB headers are used under their explicit MIT alternative A;\nboth original offered alternatives and all embedded attributions remain.\nThe DejaVu font is an external runtime/build dependency, not redistributed\nin this package. Its own package retains its Bitstream Vera/PD attribution.\n",
  "formal_rights_admission": false,
  "license_choices": "MIT AND FTL AND Apache-2.0",
  "per_file": [
    {
      "bytes": 65,
      "installed_notice_is_entire_original_file": true,
      "notice_clues": [],
      "notice_install": "source-notices/.github/FUNDING.yml.notice",
      "path": ".github/FUNDING.yml",
      "raw_sha256": "ca5204e42a97ea7e42fd93c7b9c7534f4fb81a9b66b7ae9bedbf1f904d247f1a",
      "selected_scope": "MIT (project LICENSE)"
    },
    {
      "bytes": 1190,
      "installed_notice_is_entire_original_file": true,
      "notice_clues": [],
      "notice_install": "source-notices/.github/workflows/main.yml.notice",
      "path": ".github/workflows/main.yml",
      "raw_sha256": "bdb60185e933ea990a2bde7e74c17bcda3b07da9cc6925a5b1f2bacec948e4e7",
      "selected_scope": "MIT (project LICENSE)"
    },
    {
      "bytes": 14,
      "installed_notice_is_entire_original_file": true,
      "notice_clues": [],
      "notice_install": "source-notices/.gitignore.notice",
      "path": ".gitignore",
      "raw_sha256": "d93373b397a89e67d540c345c03ad326bada497e3048c74d08ff10427b93cb69",
      "selected_scope": "MIT (project LICENSE)"
    },
    {
      "bytes": 4705,
      "installed_notice_is_entire_original_file": true,
      "notice_clues": [],
      "notice_install": "source-notices/CMakeLists.txt.notice",
      "path": "CMakeLists.txt",
      "raw_sha256": "ce844bdd113855506dbda345617151b76018d32032adf8dff88958b482e7d11f",
      "selected_scope": "MIT (project LICENSE)"
    },
    {
      "bytes": 1104,
      "installed_notice_is_entire_original_file": true,
      "notice_clues": [
        "Copyright (c) 2020-2026 Samuel Ugochukwu <sammycageagle@gmail.com>",
        "Permission is hereby granted, free of charge, to any person obtaining a copy",
        "The above copyright notice and this permission notice shall be included in all",
        "AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER"
      ],
      "notice_install": "source-notices/LICENSE.notice",
      "path": "LICENSE",
      "raw_sha256": "a55d1e78eaf75779c336b4ba061e74aae56a21195d234474fb24a398935d6ce1",
      "selected_scope": "MIT (project LICENSE)"
    },
    {
      "bytes": 3086,
      "installed_notice_is_entire_original_file": true,
      "notice_clues": [],
      "notice_install": "source-notices/README.md.notice",
      "path": "README.md",
      "raw_sha256": "4e084a4c54f05c3c555d444e9375e18da3f7f66612a9c300d81afffb977e856d",
      "selected_scope": "MIT (project LICENSE)"
    },
    {
      "bytes": 134,
      "installed_notice_is_entire_original_file": true,
      "notice_clues": [],
      "notice_install": "source-notices/cmake/plutovgConfig.cmake.in.notice",
      "path": "cmake/plutovgConfig.cmake.in",
      "raw_sha256": "a03263b5901fb32549448976e20a2867c0b4e117fb2fe6ca9ee4696fbf516e08",
      "selected_scope": "MIT (project LICENSE)"
    },
    {
      "bytes": 70,
      "installed_notice_is_entire_original_file": true,
      "notice_clues": [],
      "notice_install": "source-notices/examples/CMakeLists.txt.notice",
      "path": "examples/CMakeLists.txt",
      "raw_sha256": "08f7a5606be40602a1c787258a09f135d3cd1943f8213d23a1c45e9bc3318413",
      "selected_scope": "MIT (project LICENSE)"
    },
    {
      "bytes": 60,
      "installed_notice_is_entire_original_file": true,
      "notice_clues": [],
      "notice_install": "source-notices/examples/meson.build.notice",
      "path": "examples/meson.build",
      "raw_sha256": "a3b172abccc96871fc040ee4bfe2b6a7f848a619ff9076a7e8ba430ba0372e0c",
      "selected_scope": "MIT (project LICENSE)"
    },
    {
      "bytes": 1706,
      "installed_notice_is_entire_original_file": true,
      "notice_clues": [],
      "notice_install": "source-notices/examples/smiley.c.notice",
      "path": "examples/smiley.c",
      "raw_sha256": "cfe4489d5d28dbd535d46e9603ea882a561d67fc311acadbc971e33342924d3e",
      "selected_scope": "MIT (project LICENSE)"
    },
    {
      "bytes": 101310,
      "installed_notice_is_entire_original_file": true,
      "notice_clues": [
        " * Copyright (c) 2020-2026 Samuel Ugochukwu <sammycageagle@gmail.com>",
        " * Permission is hereby granted, free of charge, to any person obtaining a copy",
        " * The above copyright notice and this permission notice shall be included in all",
        " * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER"
      ],
      "notice_install": "source-notices/include/plutovg.h.notice",
      "path": "include/plutovg.h",
      "raw_sha256": "a12290cb45a53a1b42a527f1c00f214c63f25d8dcc1f37bd9f7bf3c4d3a0e21f",
      "selected_scope": "MIT (project LICENSE)"
    },
    {
      "bytes": 2226,
      "installed_notice_is_entire_original_file": true,
      "notice_clues": [],
      "notice_install": "source-notices/meson.build.notice",
      "path": "meson.build",
      "raw_sha256": "bc68c105b4fb336b3e03c6577787d6ac364800449f5b4203a8398d2bf9a3c6da",
      "selected_scope": "MIT (project LICENSE)"
    },
    {
      "bytes": 257,
      "installed_notice_is_entire_original_file": true,
      "notice_clues": [],
      "notice_install": "source-notices/meson_options.txt.notice",
      "path": "meson_options.txt",
      "raw_sha256": "93b68aa3bd0f4ba074fe762634d019a74998df9d9c5447706f3bb99d4dbb4fb5",
      "selected_scope": "MIT (project LICENSE)"
    },
    {
      "bytes": 6392,
      "installed_notice_is_entire_original_file": true,
      "notice_clues": [],
      "notice_install": "source-notices/smiley.png.notice",
      "path": "smiley.png",
      "raw_sha256": "5e3fd2ad55bf616a0718af2f4323ef9032a0cfc6236838bf1d4ba134c25497f7",
      "selected_scope": "MIT (project LICENSE)"
    },
    {
      "bytes": 6718,
      "installed_notice_is_entire_original_file": true,
      "notice_clues": [
        "                    The FreeType Project LICENSE",
        "                    Copyright 1996-2002, 2006 by",
        "  The FreeType  Project is distributed in  several archive packages;",
        "  some of them may contain, in addition to the FreeType font engine,",
        "  FreeType Project.",
        "  affects  thus  the  FreeType   font  engine,  the  test  programs,",
        "      FreeType code. (`credits')",
        "  We  disclaim  all warranties  covering  The  FreeType Project  and",
        "  assume no liability related to The FreeType Project.",
        "    Portions of this software are copyright \ufffd <year> The FreeType",
        "    Project (www.freetype.org).  All rights reserved.",
        "  Please replace <year> with the value from the FreeType version you",
        "  Throughout this license,  the terms `package', `FreeType Project',",
        "  and  `FreeType  archive' refer  to  the  set  of files  originally",
        "  Werner Lemberg) as the `FreeType Project', be they named as alpha,",
        "  This  program is  referred to  as  `a program  using the  FreeType",
        "  FreeType  Project,   including  all  source   code,  binaries  and",
        "  The FreeType  Project is copyright (C) 1996-2000  by David Turner,",
        "  THE FREETYPE PROJECT  IS PROVIDED `AS IS' WITHOUT  WARRANTY OF ANY",
        "  PURPOSE.  IN NO EVENT WILL ANY OF THE AUTHORS OR COPYRIGHT HOLDERS",
        "  USE, OF THE FREETYPE PROJECT.",
        "  sublicense the  FreeType Project (in  both source and  object code",
        "      documentation.   The  copyright   notices  of  the  unaltered,",
        "      FreeType Team,  in  the  distribution  documentation.  We also",
        "      encourage you to put an URL to the FreeType web page  in  your",
        "  the FreeType Project,  not just the unmodified files.   If you use",
        "  Neither the  FreeType authors and  contributors nor you  shall use",
        "  or advertising  materials: `FreeType Project',  `FreeType Engine',",
        "  `FreeType library', or `FreeType Distribution'.",
        "  accept  it.   However,  as  the FreeType  Project  is  copyrighted",
        "  Therefore,  by  using,  distributing,  or modifying  the  FreeType",
        "  There are two mailing lists related to FreeType:",
        "    o freetype@nongnu.org",
        "      Discusses general use and applications of FreeType, as well as",
        "    o freetype-devel@nongnu.org",
        "    http://www.freetype.org"
      ],
      "notice_install": "source-notices/source/FTL.TXT.notice",
      "path": "source/FTL.TXT",
      "raw_sha256": "e60d07dfb2c5264f9f405fa52bf0d4f85429dd9ae1bc2ffcff8af1924ef720d1",
      "selected_scope": "FTL"
    },
    {
      "bytes": 38324,
      "installed_notice_is_entire_original_file": true,
      "notice_clues": [],
      "notice_install": "source-notices/source/plutovg-blend.c.notice",
      "path": "source/plutovg-blend.c",
      "raw_sha256": "3da9df7f69631fd9a907b8066b4e102bf7e0b93f134197d1d746201a82c2aa5a",
      "selected_scope": "MIT (project LICENSE)"
    },
    {
      "bytes": 25303,
      "installed_notice_is_entire_original_file": true,
      "notice_clues": [],
      "notice_install": "source-notices/source/plutovg-canvas.c.notice",
      "path": "source/plutovg-canvas.c",
      "raw_sha256": "ddada462dd66f9f856a85e6ed13fe5ab65838a2b84d6a4f6a14bd36896861061",
      "selected_scope": "MIT (project LICENSE)"
    },
    {
      "bytes": 35946,
      "installed_notice_is_entire_original_file": true,
      "notice_clues": [],
      "notice_install": "source-notices/source/plutovg-font.c.notice",
      "path": "source/plutovg-font.c",
      "raw_sha256": "e121cbbb3930a1812d4c2a2ab2ee930003092064e79d869420dcb267979d93c9",
      "selected_scope": "MIT (project LICENSE)"
    },
    {
      "bytes": 11731,
      "installed_notice_is_entire_original_file": true,
      "notice_clues": [
        "/*    FreeType trigonometric functions (body).                             */",
        "/*  Copyright 2001-2005, 2012-2013 by                                      */",
        "/*  This file is part of the FreeType project, and may only be used,       */",
        "/*  modified, and distributed under the terms of the FreeType project      */"
      ],
      "notice_install": "source-notices/source/plutovg-ft-math.c.notice",
      "path": "source/plutovg-ft-math.c",
      "raw_sha256": "02a1b5faf07a0ce6f4af2001fb6fa887a3682c2a2cbc9b2454894d8f930612e6",
      "selected_scope": "FTL"
    },
    {
      "bytes": 14096,
      "installed_notice_is_entire_original_file": true,
      "notice_clues": [
        "/*    FreeType trigonometric functions (specification).                    */",
        "/*  Copyright 2001, 2003, 2005, 2007, 2013 by                              */",
        "/*  This file is part of the FreeType project, and may only be used,       */",
        "/*  modified, and distributed under the terms of the FreeType project      */",
        "/*    fractional pixels in FreeType, it resulted in noticeable speed     */",
        " *   This type is used to model angle values in FreeType.  Note that the"
      ],
      "notice_install": "source-notices/source/plutovg-ft-math.h.notice",
      "path": "source/plutovg-ft-math.h",
      "raw_sha256": "9d1b12c8e2cda360fc591d0dea879462e4fcf3628e27d31aa9ca223b6309414d",
      "selected_scope": "FTL"
    },
    {
      "bytes": 55979,
      "installed_notice_is_entire_original_file": true,
      "notice_clues": [
        "/*  Copyright 2000-2003, 2005-2014 by                                      */",
        "/*  This file is part of the FreeType project, and may only be used,       */",
        "/*  modified, and distributed under the terms of the FreeType project      */",
        "/* This is a new anti-aliasing scan-converter for FreeType 2.  The       */",
        "  /*  i.e., when building this component without the rest of FreeType.     */"
      ],
      "notice_install": "source-notices/source/plutovg-ft-raster.c.notice",
      "path": "source/plutovg-ft-raster.c",
      "raw_sha256": "258f9750abf096e3916a4678788a1310007733335ee3644a98b0f1bf3bef8271",
      "selected_scope": "FTL"
    },
    {
      "bytes": 27166,
      "installed_notice_is_entire_original_file": true,
      "notice_clues": [
        "/*    FreeType glyph image formats and default raster interface            */",
        "/*  Copyright 1996-2010, 2013 by                                           */",
        "/*  This file is part of the FreeType project, and may only be used,       */",
        "/*  modified, and distributed under the terms of the FreeType project      */",
        "/*    FreeType error code.  0~means success.                             */"
      ],
      "notice_install": "source-notices/source/plutovg-ft-raster.h.notice",
      "path": "source/plutovg-ft-raster.h",
      "raw_sha256": "cb065904566f2313f61dbd64be817d4da2944fb5fff391a12bd9b3be3f19be4d",
      "selected_scope": "FTL"
    },
    {
      "bytes": 61890,
      "installed_notice_is_entire_original_file": true,
      "notice_clues": [
        "/*    FreeType path stroker (body).                                        */",
        "/*  Copyright 2002-2006, 2008-2011, 2013 by                                */",
        "/*  This file is part of the FreeType project, and may only be used,       */",
        "/*  modified, and distributed under the terms of the FreeType project      */"
      ],
      "notice_install": "source-notices/source/plutovg-ft-stroker.c.notice",
      "path": "source/plutovg-ft-stroker.c",
      "raw_sha256": "d6a4a5ef92b2395bd9e7a93441f2b5c438d632640d450ea84b2228f20ca9cc96",
      "selected_scope": "FTL"
    },
    {
      "bytes": 9582,
      "installed_notice_is_entire_original_file": true,
      "notice_clues": [
        "/*    FreeType path stroker (specification).                               */",
        "/*  Copyright 2002-2006, 2008, 2009, 2011-2012 by                          */",
        "/*  This file is part of the FreeType project, and may only be used,       */",
        "/*  modified, and distributed under the terms of the FreeType project      */",
        " *     FreeType library handle.",
        " *    FreeType error code.  0~means success.",
        " *   FreeType error code.  0~means success.",
        " *   FreeType error code.  0~means success."
      ],
      "notice_install": "source-notices/source/plutovg-ft-stroker.h.notice",
      "path": "source/plutovg-ft-stroker.h",
      "raw_sha256": "519c1487a65c3f515afd25ff752038e5ffbd3beee02038302fd61dc87c5e9695",
      "selected_scope": "FTL"
    },
    {
      "bytes": 8973,
      "installed_notice_is_entire_original_file": true,
      "notice_clues": [
        " *   FreeType simple types definitions (specification only).",
        " * Copyright (C) 1996-2020 by",
        " * This file is part of the FreeType project, and may only be used,",
        " * modified, and distributed under the terms of the FreeType project",
        "/*    The FreeType error code type.  A value of~0 is always interpreted  */"
      ],
      "notice_install": "source-notices/source/plutovg-ft-types.h.notice",
      "path": "source/plutovg-ft-types.h",
      "raw_sha256": "801a879039ab7ffb5c6049eb3a4e364fdac03d1d22349d7f6f3bc9e35ae9732b",
      "selected_scope": "FTL"
    },
    {
      "bytes": 7576,
      "installed_notice_is_entire_original_file": true,
      "notice_clues": [],
      "notice_install": "source-notices/source/plutovg-matrix.c.notice",
      "path": "source/plutovg-matrix.c",
      "raw_sha256": "d9ce4a5ef62ed3b01582d6e7d5fad2dbb895f98b1754a33575b66ef73ebd1126",
      "selected_scope": "MIT (project LICENSE)"
    },
    {
      "bytes": 17701,
      "installed_notice_is_entire_original_file": true,
      "notice_clues": [],
      "notice_install": "source-notices/source/plutovg-paint.c.notice",
      "path": "source/plutovg-paint.c",
      "raw_sha256": "fa9fbeb8e8bd4a438b0a32762a6af67fd4e5957c035ec8c5830942f96bbe2a88",
      "selected_scope": "MIT (project LICENSE)"
    },
    {
      "bytes": 31305,
      "installed_notice_is_entire_original_file": true,
      "notice_clues": [],
      "notice_install": "source-notices/source/plutovg-path.c.notice",
      "path": "source/plutovg-path.c",
      "raw_sha256": "5d2eaec19062a1c2ba336bccfca1bdd20828dce7fa669a21882cbb0a0c5c7276",
      "selected_scope": "MIT (project LICENSE)"
    },
    {
      "bytes": 5147,
      "installed_notice_is_entire_original_file": true,
      "notice_clues": [],
      "notice_install": "source-notices/source/plutovg-private.h.notice",
      "path": "source/plutovg-private.h",
      "raw_sha256": "536185040b85c07482d04a85d2d67c04cc228fa9ed6ed1351af2f8728db98ba1",
      "selected_scope": "MIT (project LICENSE)"
    },
    {
      "bytes": 12997,
      "installed_notice_is_entire_original_file": true,
      "notice_clues": [],
      "notice_install": "source-notices/source/plutovg-rasterize.c.notice",
      "path": "source/plutovg-rasterize.c",
      "raw_sha256": "49bf5959ad21930c7f9dc17d7fc9b662b4a53b78ece63c93b2ad1eea667ef4e3",
      "selected_scope": "MIT (project LICENSE)"
    },
    {
      "bytes": 71221,
      "installed_notice_is_entire_original_file": true,
      "notice_clues": [
        "   Jon Olick              -    original jo_jpeg.cpp code",
        " * This is based on Jon Olick's jo_jpeg.cpp:",
        "             writing JPEG (using Jon Olick's code)",
        "Copyright (c) 2017 Sean Barrett",
        "Permission is hereby granted, free of charge, to any person obtaining a copy of",
        "The above copyright notice and this permission notice shall be included in all",
        "AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER",
        "In jurisdictions that recognize copyright laws, the author or authors of this",
        "software dedicate any and all copyright interest in the software to the public",
        "this software under copyright law."
      ],
      "notice_install": "source-notices/source/plutovg-stb-image-write.h.notice",
      "path": "source/plutovg-stb-image-write.h",
      "raw_sha256": "fc1f2db67a6914bd34250f34fe64b776f08d6a19b9b97bcc25dafb5973546010",
      "selected_scope": "MIT (explicit STB alternative A)"
    },
    {
      "bytes": 282995,
      "installed_notice_is_entire_original_file": true,
      "notice_clues": [
        "Copyright (c) 2017 Sean Barrett",
        "Permission is hereby granted, free of charge, to any person obtaining a copy of",
        "The above copyright notice and this permission notice shall be included in all",
        "AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER",
        "In jurisdictions that recognize copyright laws, the author or authors of this",
        "software dedicate any and all copyright interest in the software to the public",
        "this software under copyright law."
      ],
      "notice_install": "source-notices/source/plutovg-stb-image.h.notice",
      "path": "source/plutovg-stb-image.h",
      "raw_sha256": "e3ce9e557d85e689bac5f8fcd1624da739508c661a84f7f6cda879b565854ff1",
      "selected_scope": "MIT (explicit STB alternative A)"
    },
    {
      "bytes": 199009,
      "installed_notice_is_entire_original_file": true,
      "notice_clues": [
        "Copyright (c) 2017 Sean Barrett",
        "Permission is hereby granted, free of charge, to any person obtaining a copy of",
        "The above copyright notice and this permission notice shall be included in all",
        "AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER",
        "In jurisdictions that recognize copyright laws, the author or authors of this",
        "software dedicate any and all copyright interest in the software to the public",
        "this software under copyright law."
      ],
      "notice_install": "source-notices/source/plutovg-stb-truetype.h.notice",
      "path": "source/plutovg-stb-truetype.h",
      "raw_sha256": "92dd46ffcbeccad84898fddeb0eff9ab5dccfc46a9f43e7809f743df4d19f93c",
      "selected_scope": "MIT (explicit STB alternative A)"
    },
    {
      "bytes": 10069,
      "installed_notice_is_entire_original_file": true,
      "notice_clues": [],
      "notice_install": "source-notices/source/plutovg-surface.c.notice",
      "path": "source/plutovg-surface.c",
      "raw_sha256": "7a2f033daa045a126747eb8b96c242a72c37c1c833fe336c3d8443754371c698",
      "selected_scope": "MIT (project LICENSE)"
    },
    {
      "bytes": 5809,
      "installed_notice_is_entire_original_file": true,
      "notice_clues": [],
      "notice_install": "source-notices/source/plutovg-utils.h.notice",
      "path": "source/plutovg-utils.h",
      "raw_sha256": "3a6ecf3fb9211c0a8c235aaa23b3bf4fd58e7149ec47356353d0698ded7b5b84",
      "selected_scope": "MIT (project LICENSE)"
    }
  ],
  "source_changes": true,
  "source_change_scope": "Only source/plutovg-font.c: generic UTF-16 lookahead; original35 notices retained before patch",
  "patched_source_sha256": "09c5cba0d63aa9e7d144c83b2960851b23106c87ca0c23bb370e0cb33c12f054",
  "source_files": 35
}
OWNED_PLUTOVG_ASSET_8
cat > .packaging-qa/assets/font-input.json <<'OWNED_PLUTOVG_ASSET_9'
{
  "RPM_bytes": 5161333,
  "RPM_header_file_digest_match": true,
  "RPM_payload_sha256": "f820c49e05564d64e85704ea1ef7e914080e6da04f6a69cdf1e4a29dfaa0fc93",
  "RPM_sha256": "5480f8aaf5cad71bfe5e375f03109b7f88e8866467eeafd8cbedc3841eace6b2",
  "RPM_url": "https://repo.openeuler.org/openEuler-24.03-LTS-SP3/everything/riscv64/rva23/riscv64/Packages/dejavu-fonts-2.37-3.oe2403sp3.noarch.rpm",
  "arch": "noarch",
  "epoch": 0,
  "font_bytes": 759720,
  "font_mode": "0o100644",
  "font_path": "/usr/share/fonts/dejavu/DejaVuSans.ttf",
  "font_redistributed": false,
  "font_sha256": "a85cab1ac6af6c532b4ad59cd00b904fd2850b1aaf33ac88061a682b752d960c",
  "package": "dejavu-fonts",
  "release": "3.oe2403sp3",
  "version": "2.37"
}
OWNED_PLUTOVG_ASSET_9
python3 .packaging-qa/assets/source-check.py . .packaging-qa/assets/source-manifest.json
python3 - <<'PY_PLUTOVG_ORIGINAL_SNAPSHOT'
import hashlib,json,pathlib,shutil
manifest=json.loads(pathlib.Path('.packaging-qa/assets/source-manifest.json').read_text())['files'];assert len(manifest)==35
snapshot=pathlib.Path('.packaging-qa/original-source');snapshot.mkdir(exist_ok=False)
for p,row in sorted(manifest.items()):
 src=pathlib.Path(p);raw=src.read_bytes();assert not src.is_symlink() and len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256'];dest=snapshot/p;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dest);assert dest.read_bytes()==raw
PY_PLUTOVG_ORIGINAL_SNAPSHOT
%patch0 -p1
python3 - <<'PY_PLUTOVG_PATCHED_MANIFEST'
import copy,hashlib,json,pathlib
original=json.loads(pathlib.Path('.packaging-qa/assets/source-manifest.json').read_text());post=copy.deepcopy(original);p='source/plutovg-font.c';assert len(original['files'])==35 and original['files'][p]['sha256']=='e121cbbb3930a1812d4c2a2ab2ee930003092064e79d869420dcb267979d93c9'
raw=pathlib.Path(p).read_bytes();assert len(raw)==35952 and hashlib.sha256(raw).hexdigest()=='09c5cba0d63aa9e7d144c83b2960851b23106c87ca0c23bb370e0cb33c12f054'
post['files'][p]['sha256']='09c5cba0d63aa9e7d144c83b2960851b23106c87ca0c23bb370e0cb33c12f054';post['files'][p]['bytes']=35952
assert [name for name in original['files'] if original['files'][name]!=post['files'][name]]==[p]
post['source_snapshot']='package-patched';post['source_patch_count']=1;post['patch_sha256']='763a9a52a47e2770904246ab18fb1eeac221023971b7a6812c39629095eba1e9'
pathlib.Path('.packaging-qa/assets/post-patch-manifest.json').write_text(json.dumps(post,indent=2,sort_keys=True)+'\n')
PY_PLUTOVG_PATCHED_MANIFEST
python3 .packaging-qa/assets/source-check.py . .packaging-qa/assets/post-patch-manifest.json

%build
%set_build_flags
cmake -S . -B .packaging-qa/build -DCMAKE_BUILD_TYPE=None \
  -DCMAKE_INSTALL_PREFIX=%{_prefix} -DCMAKE_INSTALL_LIBDIR=%{_lib} \
  -DCMAKE_C_FLAGS="%{build_cflags} -UNDEBUG" -DCMAKE_EXPORT_COMPILE_COMMANDS=ON
cmake --build .packaging-qa/build --parallel 2 --verbose
python3 .packaging-qa/assets/source-check.py . .packaging-qa/assets/post-patch-manifest.json --cache .packaging-qa/build/CMakeCache.txt

%install
DESTDIR=%{buildroot} cmake --install .packaging-qa/build
install -d %{buildroot}%{_datadir}/plutovg-tests %{buildroot}%{_licensedir}/%{name}/source-notices %{buildroot}%{_docdir}/%{name}
cp -a .packaging-qa/assets/. %{buildroot}%{_datadir}/plutovg-tests/
install -m 0644 LICENSE %{buildroot}%{_licensedir}/%{name}/LICENSE-MIT
install -m 0644 source/FTL.TXT %{buildroot}%{_licensedir}/%{name}/FTL.TXT
install -m 0644 %{SOURCE1} %{buildroot}%{_licensedir}/%{name}/Apache-2.0.txt
install -m 0644 .packaging-qa/assets/FreeType-acknowledgement.txt %{buildroot}%{_licensedir}/%{name}/FreeType-acknowledgement.txt
install -m 0644 .packaging-qa/assets/rights-ledger.json %{buildroot}%{_licensedir}/%{name}/rights-ledger.json
install -m 0644 README.md %{buildroot}%{_docdir}/%{name}/upstream-README.md
python3 - "%{buildroot}%{_licensedir}/%{name}/source-notices" <<'PY_PLUTOVG_NOTICES'
import hashlib,json,pathlib,shutil,sys
root=pathlib.Path(sys.argv[1]);manifest=json.loads(pathlib.Path('.packaging-qa/assets/source-manifest.json').read_text())['files'];sums=[]
for p,row in sorted(manifest.items()):
 src=pathlib.Path('.packaging-qa/original-source')/p;assert not src.is_symlink() and src.stat().st_size==row['bytes'] and hashlib.sha256(src.read_bytes()).hexdigest()==row['sha256'];dest=root/(p+'.notice');dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dest);assert dest.read_bytes()==src.read_bytes();sums.append(row['sha256']+'  '+p+'.notice')
(root/'SHA256SUMS').write_text('\n'.join(sums)+'\n')
PY_PLUTOVG_NOTICES
python3 .packaging-qa/assets/source-check.py . .packaging-qa/assets/post-patch-manifest.json

%check
python3 .packaging-qa/assets/source-check.py . .packaging-qa/assets/post-patch-manifest.json --cache .packaging-qa/build/CMakeCache.txt
python3 .packaging-qa/assets/run-qa.py --prefix %{buildroot}%{_prefix} --phase build \
  --output .packaging-qa/build-validation --font-contract .packaging-qa/assets/font-input.json \
  --smiley .packaging-qa/build/examples/smiley
python3 .packaging-qa/assets/source-check.py . .packaging-qa/assets/post-patch-manifest.json

%files
%{_includedir}/plutovg/
%{_libdir}/libplutovg.a
%{_libdir}/pkgconfig/plutovg.pc
%{_libdir}/cmake/plutovg/
%{_datadir}/plutovg-tests/
%doc %{_docdir}/%{name}/
%license %{_licensedir}/%{name}/

%changelog
* Wed Oct 28 2026 yinjiayi <yinjiayi@users.noreply.github.com> - 1.3.3-1
- Preserve the native static SDK and example; add target-only consumer validation.
- Fix generic UTF-16 surrogate lookahead; retain the failing supplementary regression.
