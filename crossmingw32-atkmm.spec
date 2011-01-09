Summary:	A C++ interface for atk library - cross MinGW32 version
Summary(pl.UTF-8):	Interfejs C++ dla biblioteki atk - wersja skrośna MinGW32
Name:		crossmingw32-atkmm
Version:	2.22.2
Release:	1
License:	LGPL v2.1+
Group:		Development/Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/atkmm/2.22/atkmm-%{version}.tar.bz2
# Source0-md5:	7541d8c3fc80c1ac2bb1887e1642eb5f
URL:		http://www.gtkmm.org/
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1:1.9
BuildRequires:	crossmingw32-atk >= 1.22.0
BuildRequires:	crossmingw32-gcc-c++
BuildRequires:	crossmingw32-glibmm >= 2.24.0
BuildRequires:	libtool >= 2:1.5
BuildRequires:	mm-common
BuildRequires:	pkgconfig >= 1:0.15
Requires:	crossmingw32-atk >= 1.22.0
Requires:	crossmingw32-glibmm >= 2.24.0
Provides:	crossmingw32-gtkmm-atk
Obsoletes:	crossmingw32-gtkmm-atk
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		no_install_post_strip	1

%define		target			i386-mingw32
%define		target_platform 	i386-pc-mingw32

%define		_sysprefix		/usr
%define		_prefix			%{_sysprefix}/%{target}
%define		_libdir			%{_prefix}/lib
%define		_pkgconfigdir		%{_prefix}/lib/pkgconfig
%define		_dlldir			/usr/share/wine/windows/system
%define		__cc			%{target}-gcc
%define		__cxx			%{target}-g++

%ifnarch %{ix86}
# arch-specific flags (like alpha's -mieee) are not valid for i386 gcc
%define		optflags	-O2
%endif
# -z options are invalid for mingw linker
%define		filterout_ld	-Wl,-z,.*

%description
A C++ interface for atk library - cross MinGW32 version.

%description -l pl.UTF-8
Interfejs C++ dla biblioteki atk - wersja skrośna MinGW32.

%package static
Summary:	Static atkmm library (cross MinGW32 version)
Summary(pl.UTF-8):	Statyczna biblioteka atkmm (wersja skrośna MinGW32)
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Provides:	crossmingw32-gtkmm-atk-static
Obsoletes:	crossmingw32-gtkmm-atk-static

%description static
Static atkmm library (cross MinGW32 version).

%description static -l pl.UTF-8
Statyczna biblioteka atkmm (wersja skrośna MinGW32).

%package dll
Summary:	DLL atkmm library for Windows
Summary(pl.UTF-8):	Biblioteka DLL atkmm dla Windows
Group:		Applications/Emulators
Requires:	crossmingw32-atk-dll >= 1.22.0
Requires:	crossmingw32-glibmm-dll >= 2.24.0
Requires:	wine
Provides:	crossmingw32-gtkmm-atk-dll
Obsoletes:	crossmingw32-gtkmm-atk-dll

%description dll
DLL atkmm library for Windows.

%description dll -l pl.UTF-8
Biblioteka DLL atkmm dla Windows.

%prep
%setup -q -n atkmm-%{version}

%build
export PKG_CONFIG_LIBDIR=%{_prefix}/lib/pkgconfig
%{__libtoolize}
%{__aclocal} -I build
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--target=%{target} \
	--host=%{target} \
	--disable-documentation \
	--enable-static

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_dlldir}
mv -f $RPM_BUILD_ROOT%{_prefix}/bin/*.dll $RPM_BUILD_ROOT%{_dlldir}

%if 0%{!?debug:1}
%{target}-strip --strip-unneeded -R.comment -R.note $RPM_BUILD_ROOT%{_dlldir}/*.dll
%{target}-strip -g -R.comment -R.note $RPM_BUILD_ROOT%{_libdir}/*.a
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%{_libdir}/libatkmm-1.6.dll.a
%{_libdir}/libatkmm-1.6.la
%{_libdir}/atkmm-1.6
%{_includedir}/atkmm-1.6
%{_pkgconfigdir}/atkmm-1.6.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libatkmm-1.6.a

%files dll
%defattr(644,root,root,755)
%{_dlldir}/libatkmm-1.6-*.dll
