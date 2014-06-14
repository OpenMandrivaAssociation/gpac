%define osmo	Osmo4

# disable format string check, can't fix it for WxWidgets part
%define Werror_cflags %{nil}

# looks like no stable ABI => version is %major
%define major	3
%define libname	%mklibname %{name} %{major}
%define devname	%mklibname %{name} -d

Name:	 	gpac
Summary:	MPEG-4 multimedia framework
Version:	0.5.0.svn5178
Release:	1

Source0:	http://downloads.sourceforge.net/gpac/%{name}-%{version}.tar.bz2
#PATCH-FIX-UPSTREAM i@marguerite.su - enable osmozilla and osmo4_wx
Patch1:		gpac-0.5.0-enable_V4Studio.patch
#PATCH-FIX-UPSTREAM i@marguerite.su - fix SVGGen ldflags
Patch2:		gpac-0.5.0-SVGGen_abuild.patch
#PATCH-FIX-UPSTREAM wengxuetian@gmail.com - fix E: 64bit-portability-issue
Patch3:		gpac-0.5.0-64bit-portability.patch
#PATCH-FIX-OPENSUSE marguerite@opensuse.org - libpng include dir fix
Patch4:		gpac-0.5.0-libpng-version-detection.patch
#PATCH-FIX-UPSTREAM marguerite@opensuse.org - use system amrnb/amrwb
Patch5:		gpac-0.5.0-system-amr.patch
#PATCH-FIX-UPSTREAM marguerite@opensuse.org - no gpac.pc in devel package
Patch6:		gpac-0.5.0-no-pc.patch
#PATCH-FIX-UPSTREAM marguerite@opensuse.org - too many arguments for JS_GetParent
Patch7:		gpac-0.5.0-js_getparent.patch
#PATCH-FIX-UPSTREAM marguerite@opensuse.org - I:Statement is overflowing a buffer
Patch8:		gpac-0.5.0-bufferoverflow.patch
#PATCH-FIX-UPSTREAM marguerite@opensuse.org - fix gf_isom_set_pixel_aspect_ratio
# not available to the public
Patch9:		gpac-0.5.0-x264-export.patch

Patch10:	110_all_implicitdecls.patch
Patch11:	gpac-0.5.0.svn5178-use-system-amr-library.patch

URL:		http://gpac.sourceforge.net/
License:	LGPLv2+
Group:		Video/Utilities
BuildRequires:	imagemagick
BuildRequires:	a52dec-devel
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(directfb)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(glut)
BuildRequires:	%{_lib}faad2-devel
BuildRequires:	jpeg-devel
BuildRequires:	pkgconfig(libavcodec)
BuildRequires:	pkgconfig(libopenjpeg1)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(libpulse)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(mad)
BuildRequires:	pkgconfig(mozjs185)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(ogg)
BuildRequires:	pkgconfig(sdl)
BuildRequires:	pkgconfig(theora)
BuildRequires:	pkgconfig(vorbis)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(xv)
BuildRequires:	subversion
BuildRequires:	xvid-devel
BuildRequires:	wxgtku-devel
# (Anssi 05/2011) Otherwise partially builds against older version of itself:
BuildConflicts:	gpac-devel
BuildConflicts:	gpac < 0.4.5-2 

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

%package -n	%{libname}
Summary:	GPAC shared library
Group:		System/Libraries
Conflicts:	%{name} < 0.4.5-4

%description -n %{libname}
GPAC is a multimedia framework based on the MPEG-4 Systems standard developed
from scratch in ANSI C.

This package provides the GPAC shared library.

This package is in tainted repository because it incorporates MPEG-4
technology which may be covered by software patents.

%package -n	%{devname}
Summary:	Development headers and library for gpac
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Provides:	gpac-devel = %{EVRD}
Conflicts:	%{name}jor

%description -n	%{devname}
Development headers and libraries for gpac.

This package is in tainted repository because it incorporates MPEG-4
technology which may be covered by software patents.

%package -n	%{osmo}
Summary:	Media player based on gpac
Group:		Video

%description -n %{osmo}
Osmo4 is an MPEG-4 player with the following features:
  * MPEG-4 Systems player:
  * Optimized 2D graphics renderer compliant with the Complete2D Scene Graph
    and Graphics profiles.
  * Video and audio presentation achieved through plugins
  * Multimedia player features:
  * Timeline controls: play, pause, step.
  * Graphics features: antialising, zoom and pan, scalable resizing of
    rendering area, basic full screen support.
  * Support for Advanced Text and Graphics extension of MPEG-4 Systems
    under standardization.
    * Frame export to JPG, PNG, B./modules/ffmpeg_in/ffmpeg_demux.c.rejMP.

Osmo4 enables the use of MPEG-4 Systems in a vast aplication domain, among
which:
  * downloaded or streamed cartoons
  * synchronized, interactive mixes of graphics, text, video and audio
  * applications benefiting from MPEG-7 and MPEG-21 advances: meta-data,
    encryption, watermarking, rights management


%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1 -b .0010~
%patch11 -p1 -b .amr~

%build
./configure	--verbose \
		--prefix=%{_prefix} \
		--mandir=%{_mandir} \
		--libdir=%{_lib} \
		--use-js=yes \
		--use-ffmpeg=system \
		--enable-depth \
		--enable-jack \
		--enable-pulseaudio \
		--enable-fixed-point \
		--enable-tinygl \
		--enable-joystick \
		--enable-amr \
		--use-a52=system \
		--use-openjpeg=system \
		--use-theora=system \
		--use-vorbis=system \
		--use-ogg=system \
		--use-zlib=system \
		--extra-cflags="%{optflags} -D_FILE_OFFSET_BITS=64 -D_LARGE_FILES -D_LARGEFILE_SOURCE=1 -DXP_UNIX -fPIC -Ofast" \
		--extra-ldflags="%{ldflags}"

%make all -C . -C applications -C osmo4_wx

%install
%makeinstall_std -C . -C applications -C osmo4_wx
%makeinstall_std install-lib 

# menu
mkdir -p %{buildroot}%{_datadir}/applications
cat << EOF > %{buildroot}%{_datadir}/applications/%{osmo}.desktop
[Desktop Entry]
Name=%{osmo}
Comment=MPEG-4 Media Player
Exec=%{osmo}
Icon=%{osmo}
Terminal=false
Type=Application
Categories=AudioVideo;Video;
EOF

#icons
mkdir -p %{buildroot}%{_liconsdir}
convert -size 48x48 applications/osmo4_wx/osmo4.xpm %{buildroot}%{_liconsdir}/%{osmo}.png
mkdir -p %{buildroot}%[_iconsdir}
convert -size 32x32 applications/osmo4_wx/osmo4.xpm %{buildroot}%{_iconsdir}/%{osmo}.png
mkdir -p %{buildroot}%{_miconsdir}
convert -size 16x16 applications/osmo4_wx/osmo4.xpm %{buildroot}%{_miconsdir}/%{osmo}.png

%files
%doc AUTHORS BUGS Changelog COPYING README TODO
%exclude %{_bindir}/Osmo4
%{_bindir}/*
%{_libdir}/%{name}
%{_mandir}/man1/*
%{_datadir}/%{name}

%files -n %{osmo}
%{_bindir}/Osmo4
%{_datadir}/applications/%{osmo}.desktop
%{_liconsdir}/%{osmo}.png
%{_iconsdir}/%{osmo}.png
%{_miconsdir}/%{osmo}.png

%files -n %{libname}
%{_libdir}/libgpac.so.%{major}
%{_libdir}/libgpac.so.%{major}.*

%files -n %{devname}
%{_includedir}/%{name}
%{_libdir}/libgpac.so
%{_libdir}/libgpac_static.a
%{_libdir}/pkgconfig/gpac.pc
