Summary:	PHP-based Wiki webapplication
Summary(pl.UTF-8):	Aplikacja WWW Wiki oparta na PHP
Name:		dokuwiki
Version:	20070626b
Release:	3
License:	GPL v2
Group:		Applications/WWW
Source0:	http://www.splitbrain.org/_media/projects/dokuwiki/%{name}-2007-06-26b.tgz
# Source0-md5:	84e9b5e8e617658bb0264aa3836f23b3
Source1:	%{name}-apache.conf
Source2:	%{name}-lighttpd.conf
Source3:	%{name}-find-lang.sh
Source4:	jude.png
# Source4-md5:	623344128960e18f86097dfee213ad4a
Source5:	eventum.gif
# Source5-md5:	cac3d0f82591a33eda2afa8ae5fe65cb
Patch0:		%{name}-paths.patch
Patch1:		%{name}-config.patch
Patch2:		%{name}-mysqlauth.patch
Patch3:		%{name}-config-allow-require.patch
Patch4:		%{name}-geshi.patch
Patch5:		%{name}-http_auth-option.patch
Patch6:		%{name}-nice_exit.patch
Patch7:		%{name}-mail-headerencodequotes.patch
Patch8:		%{name}-notify-respect-minor.patch
Patch9:		%{name}-media-userinfo.patch
Patch10:	%{name}-mailtext.patch
URL:		http://wiki.splitbrain.org/wiki:dokuwiki
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	geshi >= 1.0.7.19
Requires:	php(xml)
Requires:	webapps
Requires:	webserver(alias)
Requires:	webserver(php) >= 4.3.3
Suggests:	php(gd)
# can use gz compression to store attic pages
Suggests:	php(zlib)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{_webapp}
%define		_localstatedir	/var/lib/%{name}

%description
DokuWiki is a standards compliant, simple to use Wiki, mainly aimed at
creating documentation of any kind. It is targeted at developer teams,
workgroups and small companies. It has a simple but powerful syntax
which makes sure the datafiles remain readable outside the Wiki and
eases the creation of structured texts. All data is stored in plain
text files - no database is required.

%description -l pl.UTF-8
DokuWiki to zgodne ze standardami i proste w użyciu Wiki, przeznaczone
głównie do tworzenia dokumentów wszelkiego rodzaju. Jest przeznaczone
dla zespołów programistów, grup roboczych i małych firm. Ma prostą,
ale mającą duże możliwości składnię, dzięki której pliki danych
pozostają czytelne poza Wiki, a także ułatwiającą tworzenie tekstów
strukturalnych. Wszystkie dane są przechowywane w plikach tekstowych -
nie jest wymagana baza danych.

%package setup
Summary:	DokuWiki setup package
Summary(pl.UTF-8):	Pakiet do wstępnej konfiguracji DokuWiki
Group:		Applications/WWW
Requires:	%{name} = %{version}-%{release}

%description setup
Install this package to configure initial DokuWiki installation. You
should uninstall this package when you're done, as it considered
insecure to keep the setup files in place.

%description setup -l pl.UTF-8
Ten pakiet należy zainstalować w celu wstępnej konfiguracji DokuWiki
po pierwszej instalacji. Potem należy go odinstalować, jako że
pozostawienie plików instalacyjnych mogłoby być niebezpieczne.

%prep
%setup -q -n %{name}-2007-06-26b
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1

rm -f inc/lang/.htaccess
# safe file
mv conf/words.aspell{.dist,}

# use system geshi package
rm -f inc/geshi.php
rm -rf inc/geshi

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_localstatedir},%{_appdir}/{bin,inc,lib}}

cp -a *.php $RPM_BUILD_ROOT%{_appdir}
cp -a bin/* $RPM_BUILD_ROOT%{_appdir}/bin
cp -a inc/* $RPM_BUILD_ROOT%{_appdir}/inc
cp -a lib/* $RPM_BUILD_ROOT%{_appdir}/lib
cp -a conf/* $RPM_BUILD_ROOT%{_sysconfdir}
cp -a data/* $RPM_BUILD_ROOT%{_localstatedir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/lighttpd.conf
touch $RPM_BUILD_ROOT%{_sysconfdir}/local.php
touch $RPM_BUILD_ROOT%{_sysconfdir}/local.protected.php
touch $RPM_BUILD_ROOT%{_sysconfdir}/acronyms.local.conf
touch $RPM_BUILD_ROOT%{_sysconfdir}/entities.local.conf
touch $RPM_BUILD_ROOT%{_sysconfdir}/interwiki.local.conf
touch $RPM_BUILD_ROOT%{_sysconfdir}/mime.local.conf
touch $RPM_BUILD_ROOT%{_sysconfdir}/smileys.local.conf

ln $RPM_BUILD_ROOT%{_appdir}/lib/images/interwiki/{dokubug,bug}.gif
cp -a %{SOURCE4} $RPM_BUILD_ROOT%{_appdir}/lib/images/fileicons
cp -a %{SOURCE5} $RPM_BUILD_ROOT%{_appdir}/lib/images/interwiki/eventum.gif

# find locales
sh %{SOURCE3} %{name}.lang

%clean
rm -rf $RPM_BUILD_ROOT

%post setup
chmod 770 %{_sysconfdir}
chmod 660 %{_sysconfdir}/dokuwiki.php

%postun setup
if [ "$1" = "0" ]; then
	chmod 750 %{_sysconfdir}
	chmod 640 %{_sysconfdir}/dokuwiki.php
fi

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%triggerin -- lighttpd
%webapp_register lighttpd %{_webapp}

%triggerun -- lighttpd
%webapp_unregister lighttpd %{_webapp}

%pretrans
if [ -d %{_appdir}/data -a ! -L %{_appdir}/data ]; then
	mv -f %{_appdir}/data/* %{_localstatedir}
	rm -rf %{_appdir}/data
fi
if [ -d %{_appdir}/conf -a ! -L %{_appdir}/conf ]; then
	mv -f %{_appdir}/conf/* %{_sysconfdir}
	rm -rf %{_appdir}/conf
fi
exit 0

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README VERSION
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lighttpd.conf

%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mediameta.php
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/msg
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/words.aspell

%attr(660,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/local.php
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/local.protected.php
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/acronyms.local.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/entities.local.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/interwiki.local.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mime.local.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/smileys.local.conf

# use local.php,local.protected.php, etc for local changes
%attr(640,root,http) %config %verify(not md5 mtime size) %{_sysconfdir}/dokuwiki.php
%attr(640,root,http) %config %verify(not md5 mtime size) %{_sysconfdir}/acronyms.conf
%attr(640,root,http) %config %verify(not md5 mtime size) %{_sysconfdir}/entities.conf
%attr(640,root,http) %config %verify(not md5 mtime size) %{_sysconfdir}/interwiki.conf
%attr(640,root,http) %config %verify(not md5 mtime size) %{_sysconfdir}/mime.conf
%attr(640,root,http) %config %verify(not md5 mtime size) %{_sysconfdir}/smileys.conf

# samples. perhaps move to %doc instead?
%attr(640,root,http) %{_sysconfdir}/mysql.conf.php.example
%attr(640,root,http) %{_sysconfdir}/acl.auth.php.dist
%attr(640,root,http) %{_sysconfdir}/wordblock.conf
%attr(640,root,http) %{_sysconfdir}/local.php.dist
%attr(640,root,http) %{_sysconfdir}/users.auth.php.dist

%dir %{_appdir}
%{_appdir}/doku.php
%{_appdir}/feed.php
%{_appdir}/index.php
%dir %{_appdir}/bin
%attr(755,root,root) %{_appdir}/bin/dwpage.php
%attr(755,root,root) %{_appdir}/bin/indexer.php
%attr(755,root,root) %{_appdir}/bin/wantedpages.php

%dir %{_appdir}/inc
%{_appdir}/inc/*.php
%{_appdir}/inc/auth
%{_appdir}/inc/parser

%dir %{_appdir}/lib
%dir %{_appdir}/lib/plugins
%dir %{_appdir}/lib/plugins/acl
%{_appdir}/lib/plugins/acl/*.*
%dir %{_appdir}/lib/plugins/config
%{_appdir}/lib/plugins/config/*.*
%{_appdir}/lib/plugins/config/settings
%dir %{_appdir}/lib/plugins/plugin
%{_appdir}/lib/plugins/plugin/*.*
%dir %{_appdir}/lib/plugins/revert
%{_appdir}/lib/plugins/revert/*.*
%dir %{_appdir}/lib/plugins/usermanager
%{_appdir}/lib/plugins/usermanager/*.*
%{_appdir}/lib/plugins/usermanager/images
%{_appdir}/lib/plugins/importoldchangelog
%{_appdir}/lib/plugins/importoldindex
%{_appdir}/lib/plugins/info
%{_appdir}/lib/plugins/*.php
%{_appdir}/lib/images
%{_appdir}/lib/scripts
%{_appdir}/lib/styles
%{_appdir}/lib/tpl
%{_appdir}/lib/exe

%dir %attr(770,root,http) %{_localstatedir}
%dir %attr(770,root,http) %{_localstatedir}/attic
%dir %attr(770,root,http) %{_localstatedir}/cache
%dir %attr(770,root,http) %{_localstatedir}/index
%dir %attr(770,root,http) %{_localstatedir}/locks
%dir %attr(770,root,http) %{_localstatedir}/media
%dir %attr(770,root,http) %{_localstatedir}/media/wiki
%dir %attr(770,root,http) %{_localstatedir}/meta
%dir %attr(770,root,http) %{_localstatedir}/pages
%dir %attr(770,root,http) %{_localstatedir}/pages/playground
%dir %attr(770,root,http) %{_localstatedir}/pages/wiki
%attr(660,root,http) %config(noreplace,missingok) %verify(not md5 mtime size) %{_localstatedir}/attic/_dummy
%attr(660,root,http) %config(noreplace,missingok) %verify(not md5 mtime size) %{_localstatedir}/cache/_dummy
%attr(660,root,http) %config(noreplace,missingok) %verify(not md5 mtime size) %{_localstatedir}/index/_dummy
%attr(660,root,http) %config(noreplace,missingok) %verify(not md5 mtime size) %{_localstatedir}/locks/_dummy
%attr(660,root,http) %config(noreplace,missingok) %verify(not md5 mtime size) %{_localstatedir}/media/wiki/dokuwiki-128.png
%attr(660,root,http) %config(noreplace,missingok) %verify(not md5 mtime size) %{_localstatedir}/meta/_dummy
%attr(660,root,http) %config(noreplace,missingok) %verify(not md5 mtime size) %{_localstatedir}/pages/playground/playground.txt
%attr(660,root,http) %config(noreplace,missingok) %verify(not md5 mtime size) %{_localstatedir}/pages/wiki/dokuwiki.txt
%attr(660,root,http) %config(noreplace,missingok) %verify(not md5 mtime size) %{_localstatedir}/pages/wiki/syntax.txt

%files setup
%defattr(644,root,root,755)
%{_appdir}/install.php
