Summary:	The Qt2 GUI application framework
Summary(pl):	Biblioteka Qt2 do tworzenia GUI
Name:		qt2
Version:	2.0.1
Release:	1
Copyright:	QPL
Group:		X11/Libraries
Group(pl):	X11/Biblioteki
#ftp:		ftp.troll.no
#path:		qt/source
Source:		qt-%version.tar.gz
BuildRequires:	libungif-devel
BuildRequires:	zlib-devel
BuildRequires:	libpng-devel
Buildroot: /tmp/%{name}-%{version}-root

%define	_prefix	/usr/X11R6
%define	_mandir	/usr/share/man

%description
Contains the shared library needed to run Qt applications, as well as
the README files for Qt.

%description -l pl
Zawiera bibliotekê Qt wymagan± przez aplikacje, które z niej korzystaj±.

%package devel
Summary:        Include files and documentation needed to compile
Summary(pl):    Pliki nag³ówkowe, przyk³ady i dokumentacja do biblioteki 
Group:          X11/Development/Libraries
Group(pl):      X11/Programowanie/Biblioteki
Requires:       %{name} = %{version}
Requires:       %{name}-extensions = %{version}
Obsoletes:	qt-devel

%description devel
Contains the files necessary to develop applications using Qt: header
files, the Qt meta object compiler, man pages, HTML documentation and
example programs. See http://www.troll.no/ for more information about
Qt, or file:/usr/share/doc/%{name}-devel-%{version}/index.html 
for Qt documentation in HTML.

%description -l pl devel
Pakiet tem zawiera pliki potrzebne do tworzenia i kompilacji aplikacji
korzystaj±cych z biblioteki Qt, jak pliki nag³ówkowe, meta kompiler (moc),
dokumentacjê. Zobacz http://www.troll.no/ aby dowiedzieæ siê wiêcej o Qt.
Dokumentacjê do biblioteki znajdziesz tak¿e pod:
/usr/share/doc/%{name}-devel-%{version}/index.html  

%package extensions
Summary:        Qt extensions, library and headers file
Summary(pl):    Qt extensions, rozrze¿enia dla QT biblioteki i pliki nag³ówkowe 
Group:          X11/Libraries
Group(pl):      X11/Biblioteki
Requires:       %{name} = %{version}

%description extensions
Contains the Qt extension files with library and include files.
Contains extension for Motif/Lesstif, OpenGL, image manipulation.

%description -l pl extensions
Pakiet zawiera zestaw rozsze¿eñ dla biblioteki Qt. Biblioteki oraz pliki
nag³ówkowe dla nastêpuj±cych pakietów: Motif/Lestif, OpenGL, Netscape oraz
operacji na obrazach.

%prep
%setup -q -n qt-%version

%build
QTDIR=`/bin/pwd`; export QTDIR
./configure \
	-shared \
	-sm \
	-system-zlib \
	-gif \
	-system-libpng

#make  RPM_OPT_FLAGS="$RPM_OPT_FLAGS"

LD_LIBRARY_PAYH=%{_libdir} make

(cd extensions/opengl/src;LD_LIBRARY_PATH=%{_libdir};make)
(cd extensions/imageio/src;LD_LIBRARY_PATH=%{_libdir};make)
(cd extensions/xt/src;LD_LIBRARY_PATH=%{_libdir};make \
	INCPATH="-I%{_includepatch} -I../../../include")

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/{%{_bindir},%{_libdir},%{_includedir},%{_mandir}/man{1,3}}

install -s bin/* $RPM_BUILD_ROOT/%{_bindir}/

install -s lib/lib*.so* $RPM_BUILD_ROOT/%{_libdir}

install lib/lib*.a $RPM_BUILD_ROOT%{_libdir}

install include/* $RPM_BUILD_ROOT/%{_includedir}
install man/man1/* $RPM_BUILD_ROOT/%{_mandir}/man1
install man/man3/* $RPM_BUILD_ROOT/%{_mandir}/man3

# Extensions
install -s lib/libqimgio.so.*.* $RPM_BUILD_ROOT%{_libdir}
ln -sf libqimgio.so.0.1 $RPM_BUILD_ROOT%{_libdir}/libqimgio.so
install extensions/imageio/src/*.h $RPM_BUILD_ROOT%{_includedir}

install lib/libqgl.a $RPM_BUILD_ROOT%{_libdir}
install extensions/opengl/src/*.h $RPM_BUILD_ROOT%{_includedir}

if [ -f lib/libqxt.a ] ; then
        install lib/libqxt.a $RPM_BUILD_ROOT%{_libdir}
fi
install extensions/xt/src/*.h $RPM_BUILD_ROOT%{_includedir}/
	
bzip2 -9 $RPM_BUILD_ROOT%{_mandir}/man[13]/* \
	ANNOUNCE FAQ README* MANIFEST PLATFORMS changes* LICENSE.QPL

%post   
/sbin/ldconfig

%postun 
/sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644, root, root, 755)
%doc {ANNOUNCE,FAQ,README*,MANIFEST,changes*,PLATFORMS,LICENSE.QPL}.bz2
%attr(755,root,root) %{_libdir}/libqt.so.2*

%files devel
%defattr(644, root, root, 755)
%doc doc/*
%attr(755,root,root) %{_bindir}/*
%{_libdir}/*.a
%{_mandir}/man[13]/*
%{_includedir}/*

%files extensions
%defattr(755,root,root,755)
%{_libdir}/libqimgio.so.*.*

%changelog
* Mon Aug  9 1999 Wojciech "Sas" Ciêciwa <cieciwa@alpha.zarz.agh.edu.pl>
  [2.0.1-1]
- update to last version.

* Tue Jun 15 1999 Wojciech "Sas" Ciêciwa <cieciwa@alpha.zarz.agh.edu.pl>
  [2.00beta2-snapshot-19990614-1]
- update to last version.

* Mon Jun 14 1999 Wojciech "Sas" Ciêciwa <cieciwa@alpha.zarz.agh.edu.pl>
  [2.00beta2-snapshot-19990613-1]
- build RPM.
