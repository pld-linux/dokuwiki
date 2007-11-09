Summary:	PHP-based Wiki webapplication
Summary(pl.UTF-8):	Aplikacja WWW Wiki oparta na PHP
Name:		dokuwiki
Version:	20070626b
Release:	0.21
License:	GPL v2
Group:		Applications/WWW
Source0:	http://www.splitbrain.org/_media/projects/dokuwiki/%{name}-2007-06-26b.tgz
# Source0-md5:	84e9b5e8e617658bb0264aa3836f23b3
Source1:	%{name}-apache.conf
Source2:	%{name}-lighttpd.conf
Patch0:		%{name}-paths.patch
Patch1:		%{name}-config.patch
URL:		http://wiki.splitbrain.org/wiki:dokuwiki
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	geshi >= 1.0.7.19
Requires:	webapps
Requires:	webserver(alias)
Requires:	webserver(php) >= 4.0.6
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{_webapp}
%define		_localstatedir	/var/lib/%{name}
%define		_phpdir	/usr/share/php

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
Summary:	Dokuwiki setup package
Summary(pl.UTF-8):	Pakiet do wstępnej konfiguracji Dokuwiki
Group:		Applications/WWW
Requires:	%{name} = %{version}-%{release}

%description setup
Install this package to configure initial Dokuwiki installation. You
should uninstall this package when you're done, as it considered
insecure to keep the setup files in place.

%description setup -l pl.UTF-8
Ten pakiet należy zainstalować w celu wstępnej konfiguracji Dokuwiki
po pierwszej instalacji. Potem należy go odinstalować, jako że
pozostawienie plików instalacyjnych mogłoby być niebezpieczne.

%prep
%setup -q -n %{name}-2007-06-26b
%patch0 -p1
%patch1 -p1

# safe file
mv conf/words.aspell{.dist,}

# use system geshi package
cat <<'EOF' > inc/geshi.php
<?php
require_once '%{_phpdir}/geshi.php';
EOF
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

ln $RPM_BUILD_ROOT%{_appdir}/lib/images/interwiki/{dokubug,issue}.gif
ln $RPM_BUILD_ROOT%{_appdir}/lib/images/interwiki/{dokubug,bug}.gif

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

%files
%defattr(644,root,root,755)
%doc README VERSION
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lighttpd.conf

%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/acronyms.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/entities.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mediameta.php
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mime.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/msg
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/smileys.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/words.aspell

# use local.php for local changes
%attr(640,root,http) %config %verify(not md5 mtime size) %{_sysconfdir}/dokuwiki.php
# use interwiki.local.conf for local changes
%attr(640,root,http) %config %verify(not md5 mtime size) %{_sysconfdir}/interwiki.conf

%attr(640,root,http) %{_sysconfdir}/mysql.conf.php.example
%attr(640,root,http) %{_sysconfdir}/acl.auth.php.dist
%attr(640,root,http) %{_sysconfdir}/wordblock.conf
%attr(640,root,http) %{_sysconfdir}/local.php.dist
%attr(640,root,http) %{_sysconfdir}/users.auth.php.dist

%dir %{_appdir}
%dir %{_appdir}/bin
%attr(755,root,root) %{_appdir}/bin/dwpage.php
%attr(755,root,root) %{_appdir}/bin/indexer.php
%attr(755,root,root) %{_appdir}/bin/wantedpages.php
%{_appdir}/inc
%{_appdir}/lib
%{_appdir}/doku.php
%{_appdir}/feed.php
%{_appdir}/index.php

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
