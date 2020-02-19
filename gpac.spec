# disable format string check, can't fix it for WxWidgets part
%define Werror_cflags %{nil}

# looks like no stable ABI => version is %major
%define major	8
%define libname	%mklibname %{name} %{major}
%define devname	%mklibname %{name} -d

Name:	 	gpac
Summary:	MPEG-4 multimedia framework
Version:	0.8.0
Release:	1
Source0:	https://github.com/gpac/gpac/archive/v%{version}.tar.gz
Patch0:		gpac-0.8.0-no-Lusrlib.patch
Patch1:		gpac-0.8.0-no-visibility-hidden.patch
Patch10:	110_all_implicitdecls.patch
Patch19:	gpac-0.5.0-system-amr.patch
Patch20:	gpac-0.5.0-svn5277-add-missing-libxml2-cflags-and-libs.patch
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
BuildRequires:	pkgconfig(sdl)
BuildRequires:	pkgconfig(theora)
BuildRequires:	pkgconfig(vorbis)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(xv)
BuildRequires:	subversion
BuildRequires:	xvid-devel
BuildRequires:	firefox-devel
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
Conflicts:	%{name} < 0.4.5-4

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
%autosetup -p1 -n %{name}-%{version}
# Fix encoding warnings
cp -p Changelog Changelog.origine
iconv -f ISO-8859-1 -t UTF8 Changelog.origine > Changelog
touch -r Changelog.origine Changelog
rm Changelog.origine

cp -p doc/ipmpx_syntax.bt doc/ipmpx_syntax.bt.origine
iconv -f ISO-8859-1 -t UTF8 doc/ipmpx_syntax.bt.origine > doc/ipmpx_syntax.bt
touch -r doc/ipmpx_syntax.bt.origine doc/ipmpx_syntax.bt
rm doc/ipmpx_syntax.bt.origine

%build
%set_build_flags
./configure	--verbose \
		--prefix=%{_prefix} \
		--mandir=%{_mandir} \
		--libdir=%{_lib} \
		--X11-path=%{_prefix} \
		--use-js=no \
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
sed -i -e 's,-L\${libdir} ,,;s,-L/usr/lib ,,g' *.pc applications/mp4client/Makefile modules/jack/Makefile
# -I/usr/include is harmful...
sed -i -e '/^Cflags:/d' *.pc

%make_build all
%make_build sggen
%make_build -C applications/generators/SVG
%make_build -C applications/udptsseg

# Needs to be done again because Libs.private is added while running make
sed -i -e 's,-L\${libdir} ,,;s,-L/usr/lib ,,g' *.pc

%install

# Makefile needs the pkgconfig dir to install the gpac.pc file otherwise it can't
mkdir -p %{buildroot}%{_libdir}/pkgconfig

%make_install install-lib

# generated sggen binaries
for i in MPEG4 SVG X3D; do
    install -m755 applications/generators/$i/${i}Gen \
    	%{buildroot}%{_bindir}
done
install -m755 bin/gcc/MP4* %{buildroot}%{_bindir}

# udptsseg
install -m755 bin/gcc/udptsseg %{buildroot}%{_bindir}

# It used to be lower case, now it's upper... Let's support both
ln -s MP42TS %{buildroot}%{_bindir}/mp42ts

%if 0
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
%endif

# Why does this crap get installed?
rm -rf %{buildroot}%{_includedir}/win32 %{buildroot}%{_includedir}/wince

%files
%doc AUTHORS BUGS Changelog COPYING README.md TODO
%doc doc/configuration.html
%{_bindir}/DashCast
%{_bindir}/MP4Box
%{_bindir}/MP4Client
%{_bindir}/MP42TS
%{_bindir}/MPEG4Gen
%{_bindir}/X3DGen
%{_bindir}/SVGGen
%{_bindir}/mp42ts
%{_bindir}/udptsseg
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
