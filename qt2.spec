%define		libqutil_version 1.0.0
Summary:	The Qt2 GUI application framework
Summary(es.UTF-8):	Biblioteca para ejecutar aplicaciones GUI Qt
Summary(pl.UTF-8):	Biblioteka Qt2 do tworzenia GUI
Summary(pt_BR.UTF-8):	Estrutura para rodar aplicações GUI Qt
Name:		qt2
Version:	2.3.2
Release:	1
License:	GPL
Group:		X11/Libraries
Source0:	ftp://ftp.troll.no/qt/source/qt-x11-%{version}.tar.gz
# Source0-md5:	8b74c7bd9ff0c4752a009f2e5a6482e4
Patch0:		%{name}-tools.patch
Patch1:		%{name}-huge_val.patch
Patch2:		%{name}-charset.patch
BuildRequires:	OpenGL-devel
BuildRequires:	XFree86-devel >= 4.0.2
BuildRequires:	giflib-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libmng-devel >= 1.0.0
BuildRequires:	libpng-devel >= 1.0.8
BuildRequires:	libstdc++-devel
BuildRequires:	nas-devel
BuildRequires:	pkgconfig
BuildRequires:	zlib-devel
Requires:	OpenGL
Requires:	XFree86-libs >= 4.0.2
Provides:	qt = %{version}
Obsoletes:	qt < 3
Obsoletes:	qt-extensions
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define 	_noautoreqdep	libGL.so.1 libGLU.so.1
%define		_includedir	%{_prefix}/include/qt2

%description
Qt is a GUI software toolkit which simplifies the task of writing and
maintaining GUI (Graphical User Interface) applications for the X
Window System. Qt is written in C++ and is fully object-oriented.

%description -l es.UTF-8
Contiene las bibliotecas compartidas necesarias para ejecutar
aplicaciones Qt, bien como los archivos README.

%description -l pl.UTF-8
Zawiera bibliotekę Qt wymaganą przez aplikacje, które z niej
korzystają.

%description -l pt_BR.UTF-8
Contém as bibliotecas compartilhadas necessárias para rodar aplicações
Qt, bem como os arquivos README.

%package devel
Summary:	Development files and documentation for the Qt GUI toolkit
Summary(es.UTF-8):	Archivos de inclusión y documentación necesaria para compilar aplicaciones Qt
Summary(pl.UTF-8):	Pliki nagłówkowe, przykłady i dokumentacja do biblioteki
Summary(pt_BR.UTF-8):	Arquivos de inclusão e documentação necessária para compilar aplicações Qt
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	XFree86-devel
Requires:	libstdc++-devel
Provides:	qt-devel = %{version}
Obsoletes:	qt-devel < 3

%description devel
Contains the files necessary to develop applications using Qt: header
files, the Qt meta object compiler, man pages, HTML documentation and
example programs. See http://www.troll.no/ for more information about
Qt, or file:/usr/share/doc/%{name}-devel-%{version}/index.html for Qt
documentation in HTML.

%description devel -l es.UTF-8
Contiene los archivos necesarios para desarrollar aplicaciones usando
Qt: archivos de inclusión, compilador de metaobjetos Qt, páginas de
manual, documentación HTML y programas ejemplo. Mira
http://www.troll.no para más información sobre el Qt, o el archivo
file:/usr/lib/qt/html/index.html en la documentación en HTML.

%description devel -l pl.UTF-8
Pakiet tem zawiera pliki potrzebne do tworzenia i kompilacji aplikacji
korzystających z biblioteki Qt, jak pliki nagłówkowe, kompilator meta
obiektów (moc), dokumentację. Zobacz http://www.troll.no/ aby
dowiedzieć się więcej o Qt. Dokumentację do biblioteki znajdziesz
także pod: /usr/share/doc/%{name}-devel-%{version}/index.html

%description devel -l pt_BR.UTF-8
Contém os arquivos necessários para desenvolver aplicações usando Qt:
arquivos de inclusão, compilador de meta-objetos Qt, veja
http://www.trolltech.com/ para mais informações sobre ele.

%package examples
Summary:	Example programs made with Qt version %{version}
Summary(pl.UTF-8):	Przykłady do Qt
Summary(pt_BR.UTF-8):	Programas exemplo desenvolvidos com o Qt
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Obsoletes:	qt-examples < 3

%description examples
Example programs made with Qt version %{version}.

%description examples -l pl.UTF-8
Przykłady do Qt.

%description examples -l pt_BR.UTF-8
Programas exemplo para o Qt versão %{version}.

%prep
%setup -q -n qt-%{version}
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1

%build
QTDIR=`/bin/pwd`; export QTDIR
./configure \
	-gif \
	-no-g++-exceptions \
	-release \
	-shared \
	-sm \
	-system-zlib \
	-system-libmng \
	-system-libpng \
	-system-nas-sound \
	-system-zlib \
	-system-jpeg \
	-thread <<_EOF_
yes
_EOF_

LD_LIBRARY_PATH=%{_libdir}
SYSCONF_CFLAGS="-pipe -DNO_DEBUG %{rpmcflags}"
SYSCONF_CXXFLAGS="-pipe -DNO_DEBUG %{rpmcflags}"
export LD_LIBRARY_PATH SYSCONF_CFLAGS SYSCONF_CXXFLAGS

%{__make} symlinks src-moc src-mt sub-src sub-tools \
%ifnarch alpha
	SYSCONF_CFLAGS="%{rpmcflags}" \
	SYSCONF_CXXFLAGS="%{rpmcflags}"
%else
	SYSCONF_CFLAGS="%{!?debug:-O0}%{?debug:-O0 -g}" \
	SYSCONF_CXXFLAGS="%{!?debug:-O0}%{?debug:-O0 -g}"
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir},%{_includedir},%{_mandir}/man3} \
	$RPM_BUILD_ROOT%{_examplesdir}/%{name} \
	$RPM_BUILD_ROOT%{_datadir}/tutorial/%{name} \

install bin/* $RPM_BUILD_ROOT%{_bindir}
install tools/msg2qm/msg2qm $RPM_BUILD_ROOT%{_bindir}
install tools/mergetr/mergetr $RPM_BUILD_ROOT%{_bindir}

install lib/libqt.so.%{version} $RPM_BUILD_ROOT%{_libdir}
ln -sf libqt.so.%{version} $RPM_BUILD_ROOT%{_libdir}/libqt.so

install lib/libqutil.so.%{libqutil_version} $RPM_BUILD_ROOT%{_libdir}
ln -sf libqutil.so.%{libqutil_version} $RPM_BUILD_ROOT%{_libdir}/libqutil.so

install lib/libqt-mt.so.%{version} $RPM_BUILD_ROOT%{_libdir}
ln -sf libqt-mt.so.%{version} $RPM_BUILD_ROOT%{_libdir}/libqt-mt.so

# empty symlinks
rm -f include/qt_mac.h include/qt_windows.h include/jri.h \
	include/jritypes.h include/npapi.h include/npupp.h
install include/* $RPM_BUILD_ROOT%{_includedir}

install doc/man/man3/* $RPM_BUILD_ROOT%{_mandir}/man3

for a in {tutorial,examples}/{Makefile,*/Makefile}; do
	cat $a | sed 's-^SYSCONF_MOC.*-SYSCONF_MOC = %{_bindir}/moc -' | \
	sed 's-^SYSCONF_CXXFLAGS_QT     = \$(QTDIR)/include-SYSCONF_CXXFLAGS_QT = %{_includedir}-' | \
	sed 's-^SYSCONF_LFLAGS_QT       = \$(QTDIR)/lib-SYSCONF_LFLAGS_QT = %{_libdir}-' > $a.
	mv -f $a. $a
done

cp -dpr examples $RPM_BUILD_ROOT%{_examplesdir}/%{name}
cp -dpr tutorial $RPM_BUILD_ROOT%{_datadir}/tutorial/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE.QPL
%attr(755,root,root) %{_libdir}/libqt.so.*.*
%attr(755,root,root) %{_libdir}/libqutil.so.*.*
%attr(755,root,root) %{_libdir}/libqt-mt.so.*.*

%files devel
%defattr(644,root,root,755)
%doc doc/html/*
%attr(755,root,root) %{_bindir}/*
%{_libdir}/libqt.so
%{_libdir}/libqutil.so
%{_libdir}/libqt-mt.so
%{_includedir}
%{_mandir}/man*/*

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/%{name}
%{_datadir}/tutorial/%{name}
