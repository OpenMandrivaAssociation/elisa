%define debug_package	%{nil}

%define rel	2

%define svn	0
%define pre	0
%if %svn
%define release		%mkrel 0.%svn.%rel
%define distname	%name-%svn.tar.lzma
%define dirname		%name
%else
%if %pre
%define release		%mkrel 0.%pre.%rel
%define distname	%name-%version.%pre.tar.gz
%define dirname		%name-%version.%pre
%else
%define release		%mkrel %rel
%define distname	%name-%version.tar.gz
%define dirname		%name-%version
%endif
%endif

# It's the same for releases, but different for pre-releases: please
# don't remove, even if it seems superfluous - AdamW 2008/03
%define fversion	%{version}

Summary:	Media center written in Python
Name:		elisa
Version:	0.5.37
Release:	%{release}
# For SVN:
# svn co https://code.fluendo.com/elisa/svn/trunk elisa
Source0:	http://elisa.fluendo.com/static/download/elisa/%{distname}
# From Debian: disable automatic updates - AdamW 2009/02
Patch0:		http://patch-tracking.debian.net/patch/series/dl/elisa/0.5.28-1/00_disable-plugin-updates.patch
License:	GPLv3 and MIT
Group:		Graphical desktop/Other
URL:		http://elisa.fluendo.com/
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	python
BuildRequires:	python-setuptools
BuildRequires:	python-devel
BuildRequires:	python-twisted
BuildRequires:	imagemagick
BuildRequires:	desktop-file-utils
BuildRequires:	gstreamer0.10-python
Requires:	elisa-plugins-good = %{version}
Requires:	elisa-plugins-bad = %{version}
Requires:	elisa-core = %{version}
Suggests:	elisa-plugins-ugly = %{version}
Suggests:	gstreamer0.10-libvisual

%description
Elisa is a project to create an open source cross platform media center 
solution. Elisa runs on top of the GStreamer multimedia framework and 
takes full advantage of harware acceleration provided by modern graphic 
cards by using OpenGL APIs. In addition to personal video recorder 
functionality (PVR) and Music Jukebox support, Elisa will also 
interoperate with devices following the DLNA standard like Intel’s ViiV 
systems.

%package core
Summary:	Media center written in Python: core files
Group:		Development/Python
Requires:	pigment-python
Requires:	python-imaging
Requires:	python-twisted
Requires:	python-twisted-web2
Requires:	gnome-python-extras
Requires:	gstreamer0.10-python
Requires:	gstreamer0.10-plugins-base
Requires:	python-sqlite2
Requires:	pyxdg
Requires:	python-pkg-resources
Suggests:	gstreamer0.10-plugins-good
Suggests:	gstreamer0.10-plugins-bad
Suggests:	python-gpod
Suggests:	python-dbus
# To fix upgrade: thanks fcrozat (#44627) - AdamW 2008/10
Conflicts:	elisa-plugins-good <= 0.3.5

%description core
Elisa is a project to create an open source cross platform media center 
solution. Elisa runs on top of the GStreamer multimedia framework and 
takes full advantage of harware acceleration provided by modern graphic 
cards by using OpenGL APIs. In addition to personal video recorder 
functionality (PVR) and Music Jukebox support, Elisa will also 
interoperate with devices following the DLNA standard like Intel’s ViiV 
systems. This package contains the core Python files for Elisa. It is
split from the binaries for packaging reasons.

%prep
%setup -q -n %{dirname}
%patch0 -p0 -b .update_disable

%build

%install
rm -rf %{buildroot}
python setup.py install --root=%{buildroot} --single-version-externally-managed --compile --optimize=2

# Install some stuff manually because the build process can't.
install -D -m644 data/%{name}.png %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png

# Generate and install 32x32 and 16x16 icons.
mkdir -p %{buildroot}%{_iconsdir}/hicolor/{32x32,16x16}/apps

convert -scale 32 data/%{name}.png %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
convert -scale 16 data/%{name}.png %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png

# Menu file
rm -f %{buildroot}%{_datadir}/applications/%{name}.desktop
rm -f %{buildroot}%{_datadir}/applications/%{name}-mobile.desktop
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop <<EOF
[Desktop Entry]
Name=Elisa Media Center
Comment=Play movies and songs on TV with remote
Exec=%{name} %U
StartupWMClass=%{name}
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
Categories=GNOME;GTK;AudioVideo;Audio;Video;Player;X-MandrivaLinux-CrossDesktop;
X-Osso-Service=com.fluendo.elisa
EOF

#don't want these
rm -rf %{buildroot}%{py_puresitedir}/mswin32
rm -f %{buildroot}%{_datadir}/pixmaps/%{name}.png
rm -f %{buildroot}%{_datadir}/icons/%{name}.png
rm -rf %{buildroot}%{_datadir}/mobile-basic-flash

# as there's three plugins packages that aren't interdependent, best
# let the core package own the plugins dir - AdamW 2008/02
mkdir -p %{buildroot}%{py_puresitedir}/%{name}/plugins

%if %mdkversion < 200900
%post
%{update_menus}
%{update_icon_cache hicolor}
%endif

%if %mdkversion < 200900
%postun
%{clean_menus}
%{clean_icon_cache hicolor}
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS FAQ FIRST_RUN NEWS RELEASE TRANSLATORS
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/hicolor/*/apps/*
%{_mandir}/man1/%{name}.1*
%{_datadir}/dbus-1/services/*.service

%files core
%defattr(-,root,root)
%{py_puresitedir}/%{name}
%{py_puresitedir}/%{name}-%{fversion}-py%{pyver}-nspkg.pth
%{py_puresitedir}/%{name}-%{fversion}-py%{pyver}.egg-info



%changelog
* Thu Dec 09 2010 Oden Eriksson <oeriksson@mandriva.com> 0.5.37-2mdv2011.0
+ Revision: 618037
- the mass rebuild of 2010.0 packages

* Fri May 01 2009 Frederik Himpe <fhimpe@mandriva.org> 0.5.37-1mdv2010.0
+ Revision: 370182
- update to new version 0.5.37

* Mon Apr 13 2009 Adam Williamson <awilliamson@mandriva.org> 0.5.35-1mdv2009.1
+ Revision: 366800
- new release 0.5.35

* Mon Mar 16 2009 Adam Williamson <awilliamson@mandriva.org> 0.5.32-1mdv2009.1
+ Revision: 356264
- new release 0.5.32

* Sat Mar 07 2009 Adam Williamson <awilliamson@mandriva.org> 0.5.30-1mdv2009.1
+ Revision: 352183
- new release 0.5.30

* Wed Feb 18 2009 Adam Williamson <awilliamson@mandriva.org> 0.5.28-2mdv2009.1
+ Revision: 342646
- add 00_disable-plugin-updates.patch from Debian: disable automatic updates

* Mon Feb 16 2009 Adam Williamson <awilliamson@mandriva.org> 0.5.28-1mdv2009.1
+ Revision: 341136
- new release 0.5.28

* Thu Feb 12 2009 Adam Williamson <awilliamson@mandriva.org> 0.5.27-1mdv2009.1
+ Revision: 339856
- new release 0.5.27

* Mon Feb 09 2009 Adam Williamson <awilliamson@mandriva.org> 0.5.25-1mdv2009.1
+ Revision: 338667
- new release 0.5.25

* Fri Jan 16 2009 Adam Williamson <awilliamson@mandriva.org> 0.5.23-1mdv2009.1
+ Revision: 330346
- new release 0.5.23

* Thu Dec 25 2008 Adam Williamson <awilliamson@mandriva.org> 0.5.22-1mdv2009.1
+ Revision: 318557
- new release 0.5.22

  + Oden Eriksson <oeriksson@mandriva.com>
    - lowercase ImageMagick

* Wed Dec 10 2008 Adam Williamson <awilliamson@mandriva.org> 0.5.21-2mdv2009.1
+ Revision: 312409
- drop the setuptools dep again (upstream bug is supposed to be fixed now)

* Tue Dec 09 2008 Adam Williamson <awilliamson@mandriva.org> 0.5.21-1mdv2009.1
+ Revision: 312337
- new release 0.5.21

* Mon Dec 01 2008 Adam Williamson <awilliamson@mandriva.org> 0.5.20-1mdv2009.1
+ Revision: 308867
- new release 0.5.20

* Mon Dec 01 2008 Adam Williamson <awilliamson@mandriva.org> 0.5.19-3mdv2009.1
+ Revision: 308747
- restore elisa-core's dependency on python-setuptools (upstream bug #303938)

* Sat Nov 29 2008 Wanderlei Cavassin <cavassin@mandriva.com.br> 0.5.19-2mdv2009.1
+ Revision: 308107
- Requires python-pkg-resources instead of whole python-setuptools,
  not draging python-devel and others at runtime.

* Tue Nov 25 2008 Adam Williamson <awilliamson@mandriva.org> 0.5.19-1mdv2009.1
+ Revision: 306680
- drop updater.patch, it's not really needed any more
- new release 0.5.19

* Tue Nov 18 2008 Adam Williamson <awilliamson@mandriva.org> 0.5.18-1mdv2009.1
+ Revision: 304122
- adjust file list for some now apparently dead files
- drop manpage location substitution (fixed upstream)
- new release 0.5.18

* Tue Nov 04 2008 Adam Williamson <awilliamson@mandriva.org> 0.5.17-1mdv2009.1
+ Revision: 299868
- new release 0.5.17

* Tue Oct 28 2008 Adam Williamson <awilliamson@mandriva.org> 0.5.16-1mdv2009.1
+ Revision: 298110
- new release 0.5.16

* Tue Oct 21 2008 Adam Williamson <awilliamson@mandriva.org> 0.5.15-1mdv2009.1
+ Revision: 296240
- drop unneeded.patch (can't do this here any more, moved it to the plugins
  packages)
- new release 0.5.15

* Wed Oct 15 2008 Adam Williamson <awilliamson@mandriva.org> 0.5.14-1mdv2009.1
+ Revision: 293836
- rediff unneeded.patch
- new release 0.5.14

* Sat Oct 11 2008 Adam Williamson <awilliamson@mandriva.org> 0.5.13-2mdv2009.1
+ Revision: 291727
- core conflicts with older plugins-good to fix upgrade

* Fri Oct 10 2008 Adam Williamson <awilliamson@mandriva.org> 0.5.13-1mdv2009.1
+ Revision: 291598
- rediff unneeded.patch
- new release 0.5.13

* Tue Sep 30 2008 Adam Williamson <awilliamson@mandriva.org> 0.5.12-1mdv2009.0
+ Revision: 289955
- new release 0.5.12

* Thu Sep 25 2008 Adam Williamson <awilliamson@mandriva.org> 0.5.11-1mdv2009.0
+ Revision: 288038
- new release 0.5.11

* Tue Sep 09 2008 Adam Williamson <awilliamson@mandriva.org> 0.5.9-1mdv2009.0
+ Revision: 283178
- rediff unneeded.patch
- new release 0.5.9

* Thu Sep 04 2008 Adam Williamson <awilliamson@mandriva.org> 0.5.8-1mdv2009.0
+ Revision: 280814
- new release 0.5.8
- rediff unneeded.patch
- version the intra-elisa requires

* Mon Aug 25 2008 Adam Williamson <awilliamson@mandriva.org> 0.5.7-1mdv2009.0
+ Revision: 276045
- new release 0.5.7

* Wed Aug 13 2008 Adam Williamson <awilliamson@mandriva.org> 0.5.5-1mdv2009.0
+ Revision: 271535
- rediff unneeded.patch
- new release 0.5.5

* Thu Jul 31 2008 Adam Williamson <awilliamson@mandriva.org> 0.5.3-3mdv2009.0
+ Revision: 258386
- suggests gstreamer0.10-libvisual (for music visualizations)
- add unneeded.patch: disable several plugins useless on Linux

* Wed Jul 30 2008 Adam Williamson <awilliamson@mandriva.org> 0.5.3-2mdv2009.0
+ Revision: 255574
- requires python-twisted-web2

* Wed Jul 30 2008 Adam Williamson <awilliamson@mandriva.org> 0.5.3-1mdv2009.0
+ Revision: 254498
- change updater.patch for new release
- small cleanups for new release
- new release 0.5.3

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

* Tue May 20 2008 Adam Williamson <awilliamson@mandriva.org> 0.3.5-4mdv2009.0
+ Revision: 209555
- elisa-core requires gstreamer0.10-plugins-base (Caio), suggests gstreamer0.10-plugins-good

* Thu Apr 17 2008 Adam Williamson <awilliamson@mandriva.org> 0.3.5-3mdv2009.0
+ Revision: 195036
- suggests elisa-plugins-ugly

* Sun Mar 23 2008 Anne Nicolas <ennael@mandriva.org> 0.3.5-2mdv2008.1
+ Revision: 189626
- Fix Mandriva menu for Elisa

* Tue Mar 18 2008 Adam Williamson <awilliamson@mandriva.org> 0.3.5-1mdv2008.1
+ Revision: 188614
- update file list
- clean up svn / pre-release conditionals
- new release 0.3.5

* Thu Mar 06 2008 Adam Williamson <awilliamson@mandriva.org> 0.3.4-2mdv2008.1
+ Revision: 180276
- drop bogus example MimeType line from the .desktop file (thanks neoclust)

* Tue Mar 04 2008 Adam Williamson <awilliamson@mandriva.org> 0.3.4-1mdv2008.1
+ Revision: 178929
- use Graphical desktop/Other as the group
- split into elisa and elisa-core to resolve dependency issue with plugins
- final 0.3.4

* Sun Mar 02 2008 Adam Williamson <awilliamson@mandriva.org> 0.3.4-0.rc3.3mdv2008.1
+ Revision: 177619
- requires elisa-plugins-bad (it shouldn't, but it does: tested by me and anne)

* Sat Mar 01 2008 Adam Williamson <awilliamson@mandriva.org> 0.3.4-0.rc3.2mdv2008.1
+ Revision: 177518
- requires plugins-good (won't launch without it: reported upstream)

* Sat Mar 01 2008 Adam Williamson <awilliamson@mandriva.org> 0.3.4-0.rc3.1mdv2008.1
+ Revision: 177152
- adjust file lists
- new release 0.3.4.rc3

* Fri Feb 29 2008 Adam Williamson <awilliamson@mandriva.org> 0.3.4-0.rc1.1mdv2008.1
+ Revision: 176633
- ok, that wasn't the right way to do it...
- correct fversion
- ghost plugins directory
- adjust spec for building core only (plugins now will be separate .src.rpms)
- new release 0.3.4rc1

* Tue Feb 26 2008 Adam Williamson <awilliamson@mandriva.org> 0.3.3.1-0.5106.2mdv2008.1
+ Revision: 175559
- fix a stray #
- add parameters so build pre-generates .pyo as well as .pyc files (per policy)

* Tue Feb 26 2008 Adam Williamson <awilliamson@mandriva.org> 0.3.3.1-0.5106.1mdv2008.1
+ Revision: 175245
- stupid, stupid upstream versioning...
- drop slideshow.patch (effectively merged upstream)
- new snapshot 5106

* Sat Feb 23 2008 Adam Williamson <awilliamson@mandriva.org> 0.3.3.1-0.5063.1mdv2008.1
+ Revision: 174022
- add slideshow.patch to make the slideshow plugin get installed (it seems to be required for elisa to launch)
- adapt to totally new buildsystem (all plugins still in main package for now)
- update to svn (to match new pigment and pigment-python)

* Wed Feb 13 2008 Adam Williamson <awilliamson@mandriva.org> 0.3.3-3mdv2008.1
+ Revision: 166846
- correct license (now GPLv3, not v2)
- including a pre-compiled .so file violates Mandriva packaging policy, noarch, and common decency, so remove this atrocity

* Wed Jan 30 2008 Adam Williamson <awilliamson@mandriva.org> 0.3.3-2mdv2008.1
+ Revision: 160137
- requires pyxdg and python-setuptools (thanks Anne and Erwan)

* Sat Jan 26 2008 Adam Williamson <awilliamson@mandriva.org> 0.3.3-1mdv2008.1
+ Revision: 158188
- br gstreamer0.10-python
- adjust spec
- new release 0.3.3

* Fri Dec 28 2007 Adam Williamson <awilliamson@mandriva.org> 0.3.2-1mdv2008.1
+ Revision: 138691
- correct file list
- drop fixhal.patch, merged upstream
- new release 0.3.2

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Fri Jun 08 2007 Frederic Crozat <fcrozat@mandriva.com> 0.1.6-2mdv2008.0
+ Revision: 37468
- Patch0 (SVN): fix hal plugin
- add dependency on dbus-python and python-setuptools

  + Adam Williamson <awilliamson@mandriva.org>
    - correct URL
    - use %%pyver, do not hardcode 2.5

* Thu May 10 2007 Adam Williamson <awilliamson@mandriva.org> 0.1.6-1mdv2008.0
+ Revision: 26134
- noarch
- BuildRequires desktop-file-utils
- Import elisa

