# disable format string check, can't fix it for WxWidgets part
%define Werror_cflags %{nil}

# gpac uses "printf" as the name of a struct member -- therefore doesn't
# like glibc's `#define printf ...` with -DFORTIFY_SOURCE=2 at all...
%undefine _fortify_cflags

%define major	12
%define oldlibname	%mklibname 12
%define libname	%mklibname
%define devname	%mklibname %{name} -d

%define snapshot 20240408

Name:	 	gpac
Summary:	MPEG-4 multimedia framework
Version:	2.2.2
Release:	%{?snapshot:0.%{snapshot}.}1
Source0:	https://github.com/gpac/gpac/archive/refs/%{?snapshot:heads/master}%{!?snapshot:tags/v%{version}}.tar.gz%{?snapshot:#/%{name}-%{snapshot}.tar.gz}
Patch1:		gpac-0.8.0-no-visibility-hidden.patch
Patch2:		gpac-1.0.1-compile.patch
Patch3:		gpac-1.1-compile.patch
Patch10:	110_all_implicitdecls.patch
URL:		http://gpac.io/
License:	LGPLv2+
Group:		Video
BuildRequires:	imagemagick
BuildRequires:	a52dec-devel
BuildRequires:	graphviz
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(glut)
BuildRequires:	pkgconfig(jack)
BuildRequires:	faad2-devel
BuildRequires:	pkgconfig(libjpeg)
BuildRequires:	pkgconfig(libavcodec)
BuildRequires:	pkgconfig(libIDL-2.0)
BuildRequires:	pkgconfig(libopenjp2)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(libpulse)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(mad)
BuildRequires:	pkgconfig(mozjs185)
BuildRequires:	pkgconfig(opencore-amrnb)
BuildRequires:	pkgconfig(opencore-amrwb)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(ogg)
BuildRequires:	pkgconfig(sdl2)
BuildRequires:	pkgconfig(theora)
BuildRequires:	pkgconfig(vorbis)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(xv)
BuildRequires:	subversion
BuildRequires:	xvid-devel
BuildRequires:	firefox-devel
BuildRequires:	locales-extra-charsets
# (Anssi 05/2011) Otherwise partially builds against older version of itself:
BuildConflicts:	gpac-devel
BuildConflicts:	gpac < 0.4.5-2
Obsoletes:	Osmo4
Obsoletes:	gpac-browser-plugin

%description
GPAC is a multimedia framework based on the MPEG-4 Systems standard developed
from scratch in ANSI C.  The original development goal is to provide a clean
(a.k.a. readable by as many people as possible), small and flexible
alternative to the MPEG-4 Systems reference software.

The natural evolution has been the integration of recent multimedia standards
(SVG/SMIL, VRML, X3D, SWF, 3GPP(2) tools, etc) into a single framework.
VRML97 and a good amount of the X3D standard have already been integrated
into GPAC, as well as some SVG support and experimental Macromedia Flash
support.

The current GPAC release (0.4.0) already covers a very large part of the
MPEG-4 standard, and has some good support for 3GPP and VRML/X3D, and
features what can probably be seen as the most advanced and robust 2D MPEG-4
Player available worldwide, as well as a decent 3D player.

GPAC also features MPEG-4 Systems encoders/multiplexers, publishing tools for
content distribution for MP4 and 3GPP(2) files and many tools for scene
descriptions (MPEG4<->VRML<->X3D converters, SWF->MPEG-4, etc...).

This package is in tainted repository because it incorporates MPEG-4
technology, covered by software patents.

%package -n %{libname}
Summary:	GPAC shared library
Group:		System/Libraries
%rename %{oldlibname}

%description -n %{libname}
GPAC is a multimedia framework based on the MPEG-4 Systems standard developed
from scratch in ANSI C.

This package provides the GPAC shared library.

This package is in tainted repository because it incorporates MPEG-4
technology which may be covered by software patents.

%package -n %{devname}
Summary:	Development headers and library for gpac
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Provides:	gpac-devel = %{EVRD}
Conflicts:	%{name}jor

%description -n %{devname}
Development headers and libraries for gpac.

This package is in tainted repository because it incorporates MPEG-4
technology which may be covered by software patents.

%prep
%autosetup -p1 %{?snapshot:-n gpac-master}
# Fix encoding warnings
cp -p Changelog Changelog.origine
iconv -f ISO-8859-1 -t UTF8 Changelog.origine > Changelog
touch -r Changelog.origine Changelog
rm Changelog.origine

%build
%set_build_flags
./configure	--verbose \
		--prefix=%{_prefix} \
		--mandir=%{_mandir} \
		--libdir=%{_lib} \
		--X11-path=%{_prefix} \
		--use-ffmpeg=system \
		--enable-depth \
		--enable-jack \
		--enable-pulseaudio \
		--enable-fixed-point \
		--enable-joystick \
		--enable-amr-nb \
		--enable-amr-wb \
		--enable-amr \
		--use-a52=system \
		--use-theora=system \
		--use-vorbis=system \
		--use-ogg=system \
		--use-zlib=system \
		--extra-cflags="%{optflags} -D_FILE_OFFSET_BITS=64 -D_LARGE_FILES -D_LARGEFILE_SOURCE=1 -DXP_UNIX -fPIC -Ofast" \
		--extra-ldflags="%{ldflags}"
#sed -i -e 's,-L\${libdir} ,,;s,-L/usr/lib ,,g' applications/mp4client/Makefile modules/jack/Makefile
# -I/usr/include is harmful...
sed -i -e '/^Cflags:/d' *.pc

%make_build all
%make_build sggen
%make_build -C applications/generators/SVG

%install
# Makefile needs the pkgconfig dir to install the gpac.pc file otherwise it can't
mkdir -p %{buildroot}%{_libdir}/pkgconfig

%make_install install-lib

# generated sggen binaries
for i in MPEG4 SVG X3D; do
    install -m755 applications/generators/$i/${i}Gen \
    	%{buildroot}%{_bindir}
done
install -m755 applications/generators/WebGLGen/WGLGen %{buildroot}%{_bindir}/
install -m755 bin/gcc/MP4* bin/gcc/gpac %{buildroot}%{_bindir}

# Why does this crap get installed?
rm -rf %{buildroot}%{_includedir}/win32 %{buildroot}%{_includedir}/wince

%files
%{_bindir}/gpac
%{_bindir}/MP4Box
%{_bindir}/MPEG4Gen
%{_bindir}/X3DGen
%{_bindir}/SVGGen
%{_bindir}/WGLGen
%{_datadir}/applications/gpac.desktop
%{_datadir}/icons/*/*/*/gpac.png
%{_libdir}/%{name}/
%{_datadir}/%{name}/
%{_mandir}/man1/*

%files -n %{libname}
%{_libdir}/libgpac.so.%{major}*

%files -n %{devname}
%{_includedir}/%{name}
%{_libdir}/libgpac.so
%{_libdir}/libgpac_static.a
%{_libdir}/pkgconfig/gpac.pc
