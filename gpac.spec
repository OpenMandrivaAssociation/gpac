# Test suite requires external data: see  README.md file
%bcond_with check

%define major	16
%define libname	%mklibname %{name}
%define devname	%mklibname %{name} -d

#define snapshot 20240408

Summary:	MPEG-4 multimedia framework
Name:	 	gpac
Version:		26.02.0
Release:	%{?snapshot:0.%{snapshot}.}3
License:		LGPLv2+
Group:		Video
Url:		https://gpac.io/
Source0:	https://github.com/gpac/gpac/archive/v%{version}/%{name}-%{version}.tar.gz
Source100:	%{name}.rpmlintrc
Patch0:		gpac-26.02.0-no-visibility-hidden.patch
Patch1:		gpac-26.02.0-fix-compile.patch
Patch2:		gpac-26.02.0-fix-all-implicit-decls.patch
Patch3:		gpac-26.02.0-drop-rpath.patch
Patch4:		gpac-26.02.0-fix-redefinition-error.patch
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	doxygen
BuildRequires:	git
BuildRequires:	graphviz
BuildRequires:	imagemagick
BuildRequires:	locales-extra-charsets
BuildRequires:	make
BuildRequires:	slibtool
BuildRequires:	a52dec-devel
BuildRequires:	faad2-devel
BuildRequires:	firefox-devel
BuildRequires:	xvid-devel
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(caca)
BuildRequires:	pkgconfig(directfb)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(glut)
BuildRequires:	pkgconfig(jack)
BuildRequires:	pkgconfig(hidapi-hidraw)
BuildRequires:	pkgconfig(libavcodec)
BuildRequires:	pkgconfig(libavfilter)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(libjpeg)
BuildRequires:	pkgconfig(libIDL-2.0)
BuildRequires:	pkgconfig(liblzma)
BuildRequires:	pkgconfig(libnghttp2)
BuildRequires:	pkgconfig(libnghttp3)
BuildRequires:	pkgconfig(libngtcp2)
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
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xmlrpc)
BuildRequires:	pkgconfig(xv)
BuildRequires:	pkgconfig(zlib)

# (Anssi 05/2011) Otherwise partially builds against older version of itself
BuildConflicts:	gpac-devel
BuildConflicts:	gpac <= 2.4.0-6

%description
GPAC is a multimedia framework based on the MPEG-4 Systems standard developed
from scratch in ANSI C.  The original development goal is to provide a clean
(a.k.a. readable by as many people as possible), small and flexible
alternative to the MPEG-4 Systems reference software.

The natural evolution has been the integration of recent multimedia standards
(SVG/SMIL, VRML, X3D, SWF, 3GPP(2) tools, etc) into a single framework.
VRML97 and a good amount of the X3D standard have already been integrated into
GPAC, as well as some SVG support and experimental Macromedia Flash support.

GPAC also features MPEG-4 Systems encoders/multiplexers, publishing tools for
content distribution for MP4 and 3GPP(2) files and many tools for scene
descriptions (MPEG4<->VRML<->X3D converters, SWF->MPEG-4, etc...).

This package is in Restricted repository because it incorporates MPEG-4
technology, covered by software patents.

%files
%license COPYING
%doc README.md Changelog SECURITY.md
%{_bindir}/%{name}
%{_bindir}/MP4Box
%{_bindir}/MPEG4Gen
%{_bindir}/X3DGen
%{_bindir}/SVGGen
%{_bindir}/WGLGen
%{_libdir}/%{name}/
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_datadir}/%{name}/
%{_mandir}/man1/*.1*

#-----------------------------------------------------------------------------

%package -n %{libname}
Summary:		GPAC shared library
Group:		System/Libraries

# Workaround for a bogus macro expansion in a previous build (before 2026)
# creating a literal "lib64%{1}" package
Obsoletes:	%{_lib}%%{1} < %{EVRD}

%description -n %{libname}
GPAC is a multimedia framework based on the MPEG-4 Systems standard developed
from scratch in ANSI C. This package provides the GPAC shared library.
This package is in Restricted repository because it incorporates MPEG-4
technology which may be covered by software patents.

%files -n %{libname}
%{_libdir}/libgpac.so.%{major}*

#-----------------------------------------------------------------------------

%package -n %{devname}
Summary:	Development headers and library for gpac
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Provides:	gpac-devel = %{EVRD}

%description -n %{devname}
Development headers and libraries for gpac.
This package is in Restricted repository because it incorporates MPEG-4
technology which may be covered by software patents.

%files -n %{devname}
%doc share/doc/html-libgpac/*
%{_includedir}/%{name}
%{_libdir}/libgpac.so
%{_libdir}/libgpac_static.a
%{_libdir}/pkgconfig/%{name}.pc

#-----------------------------------------------------------------------------

%prep
%autosetup -p1


%build
# Enabling this makes the build fail with clang 22
#	--enable-fixed-point \
# Not a regular autotools configure: use the provided one
%set_build_flags
./configure	--verbose \
		--prefix=%{_prefix} \
		--mandir=%{_mandir} \
		--libdir=%{_lib} \
		--X11-path="%{_prefix}/include/X11" \
		--enable-depth \
		--enable-pic \
		--use-a52=system \
		--use-curl=system \
		--use-directfb=system \
		--use-faad=system \
		--use-ffmpeg=system \
		--use-freetype=system \
		--use-jack=system \
		--use-hid=system \
		--use-libcaca=system \
		--use-ogg=system \
		--use-openjpeg=system \
		--use-pulseaudio=system \
		--use-theora=system \
		--use-vorbis=system \
		--use-zlib=system \
		%if %{with check}
		--unittests \
		%endif
		--extra-cflags="%{optflags} -D_FILE_OFFSET_BITS=64 -D_LARGE_FILES -D_LARGEFILE_SOURCE=1 -DXP_UNIX -Ofast" \
		--extra-ldflags="%{ldflags}"

sed -ie 's/DEBUGBUILD=no/DEBUGBUILD=yes/' config.mak

# Build library, modules and apps
%make_build
# Build generators
%make_build sggen
# FIXME: Won't automatically build
%make_build -C applications/generators/SVG
# Build devel docs
%make_build doc


%install
%make_install install-lib

# Install built generators binaries
for i in MPEG4 X3D SVG; do
    install -m755 applications/generators/$i/${i}Gen %{buildroot}%{_bindir}
done
install -m755 applications/generators/WebGLGen/WGLGen %{buildroot}%{_bindir}/

# Fix rpath
chrpath -d %{buildroot}%{_libdir}/gpac/gm_sdl_out.so

# -I/usr/include is harmful...
sed -i -e '/^Cflags:/d' %{buildroot}%{_libdir}/pkgconfig/%{name}.pc


%if %{with check}
%check
%make tests_suite
%endif
