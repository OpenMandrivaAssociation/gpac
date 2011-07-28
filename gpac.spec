%define name	gpac
%define version	0.4.5
%define rel	2
%define release %mkrel %{rel}
%define osmo	Osmo4

# disable format string check, can't fix it for WxWidgets part
%define Werror_cflags %{nil}

Name: 	 	%{name}
Summary: 	MPEG-4 multimedia framework
Version: 	%{version}
Release: 	%{release}

Source:		http://downloads.sourceforge.net/gpac/gpac-%{version}.tar.gz
URL:		http://gpac.sourceforge.net/
License:	LGPL
Group:		Video
BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	ImageMagick
BuildRequires:	SDL-devel
%if %mdkversion <= 200600
BuildRequires:	MesaGLU-devel
%else
BuildRequires:	mesaglu-devel
BuildRequires:	mesaglut-devel
%endif
BuildRequires:	freetype2-devel
BuildRequires:	libfaad2-devel
BuildRequires:	jpeg-devel
BuildRequires:	png-devel
BuildRequires:	libmad-devel
BuildRequires:	xvid-devel
BuildRequires:	ffmpeg-devel
BuildRequires:	libxml2-devel
BuildRequires:	openssl-devel
BuildRequires:	zlib-devel
BuildRequires:	libogg-devel libvorbis-devel libtheora-devel
BuildRequires:	wxgtku2.8-devel
BuildRequires:	xulrunner-devel
BuildRequires:	libalsa-devel
BuildRequires:	pulseaudio-devel
BuildRequires:	libxv-devel

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

This package is in PLF because it incorporates MPEG-4 technology, covered by
software patents.

%package	devel
Summary:	Static library from gpac
Group:		Development/C

%description	devel
Static library from gpac.

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
    * Frame export to JPG, PNG, BMP.

Osmo4 enables the use of MPEG-4 Systems in a vast aplication domain, among
which:
  * downloaded or streamed cartoons
  * synchronized, interactive mixes of graphics, text, video and audio
  * applications benefiting from MPEG-7 and MPEG-21 advances: meta-data,
    encryption, watermarking, rights management

This package is in PLF because it incorporates MPEG-4 technology, covered by
software patents.

%prep
%setup -q -n gpac
chmod 755 configure
# lib64 compatible
perl -p -i -e 's/lGLU/lGLU\ \-L\/usr\/X11R6\/%{_lib}/g' configure
perl -p -i -e 's,\$prefix/lib/gpac,\$prefix/%{_lib}/gpac,' configure
perl -p -i -e 's,\$\(prefix\)/lib,\$(prefix)/%{_lib},' Makefile

# SHH!
perl -p -i -e 's/Wall/w/g' `find -name Makefile`

%build
./configure --prefix=%{buildroot}%{_prefix} \
	--use-js=no

# parallel make fails
make OPTFLAGS="%{optflags} -fPIC" CPPFLAGS="%{optflags} -fPIC" GECKO_PATH="%(pkg-config --variable=includedir libxul)"

%install
rm -rf %{buildroot}
make mandir=%{buildroot}%{_datadir}/man install
make install-lib

# menu
mkdir -p %{buildroot}%{_menudir}
cat << EOF > %{buildroot}%{_menudir}/%{osmo}
?package(%{osmo}): command="Osmo4" icon="%{osmo}.png" needs="x11" title="Osmo4" longtitle="MPEG-4 Media Player" section="Multimedia/Video"
EOF

#icons
mkdir -p %{buildroot}%{_liconsdir}
convert -size 48x48 applications/osmo4_wx/osmo4.xpm %{buildroot}%{_liconsdir}/%{osmo}.png
mkdir -p %{buildroot}%{_iconsdir}
convert -size 32x32 applications/osmo4_wx/osmo4.xpm %{buildroot}%{_iconsdir}/%{osmo}.png
mkdir -p %{buildroot}%{_miconsdir}
convert -size 16x16 applications/osmo4_wx/osmo4.xpm %{buildroot}%{_miconsdir}/%{osmo}.png

%clean
rm -rf %{buildroot}

%post -n %{osmo}
%update_menus
		
%postun -n %{osmo}
%clean_menus

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc AUTHORS BUGS Changelog COPYING README TODO
%{_bindir}/MP4*
%{_libdir}/*.so
%{_libdir}/%{name}
%{_mandir}/man1/*
%{_datadir}/%{name}

%files -n %{osmo}
%defattr(-,root,root)
%{_bindir}/Osmo4
%{_menudir}/%{osmo}
%{_liconsdir}/%{osmo}.png
%{_iconsdir}/%{osmo}.png
%{_miconsdir}/%{osmo}.png

%files devel
%defattr(-,root,root)
%{_includedir}/%{name}
%{_libdir}/*.a

