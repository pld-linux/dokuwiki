Summary:	PHP-based Wiki webapplication
Summary(pl.UTF-8):	Aplikacja WWW Wiki oparta na PHP
Name:		dokuwiki
Version:	20070626b
Release:	0.6
License:	GPL v2
Group:		Applications/WWW
Source0:	http://www.splitbrain.org/_media/projects/dokuwiki/%{name}-2007-06-26b.tgz
# Source0-md5:	84e9b5e8e617658bb0264aa3836f23b3
URL:		http://wiki.splitbrain.org/wiki:dokuwiki
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	webapps
Requires:	webserver(php) >= 4.0.6
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

%prep
%setup -q -n %{name}-2007-06-26b

cat > apache.conf <<EOF
Alias /%{_webapp} %{_appdir}
<Directory %{_appdir}/>
	Allow from all
</Directory>
EOF

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_appdir},%{_localstatedir}}

cp -a *.php $RPM_BUILD_ROOT%{_appdir}
cp -a bin inc lib $RPM_BUILD_ROOT%{_appdir}
cp -a conf/* $RPM_BUILD_ROOT%{_sysconfdir}
cp -a data/* $RPM_BUILD_ROOT%{_localstatedir}
ln -s %{_localstatedir} $RPM_BUILD_ROOT%{_appdir}/data
ln -s %{_sysconfdir} $RPM_BUILD_ROOT%{_appdir}/conf
install apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
install apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

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
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/acl.auth.php.dist
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/acronyms.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/dokuwiki.php
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/entities.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/interwiki.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/local.php.dist
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mediameta.php
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mime.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/msg
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mysql.conf.php.example
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/smileys.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/users.auth.php.dist
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/wordblock.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/words.aspell.dist

%{_appdir}

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
%attr(770,root,http) %config(noreplace,missingok) %verify(not md5 mtime size) %{_localstatedir}/attic/_dummy
%attr(770,root,http) %config(noreplace,missingok) %verify(not md5 mtime size) %{_localstatedir}/cache/_dummy
%attr(770,root,http) %config(noreplace,missingok) %verify(not md5 mtime size) %{_localstatedir}/index/_dummy
%attr(770,root,http) %config(noreplace,missingok) %verify(not md5 mtime size) %{_localstatedir}/locks/_dummy
%attr(770,root,http) %config(noreplace,missingok) %verify(not md5 mtime size) %{_localstatedir}/media/wiki/dokuwiki-128.png
%attr(770,root,http) %config(noreplace,missingok) %verify(not md5 mtime size) %{_localstatedir}/meta/_dummy
%attr(770,root,http) %config(noreplace,missingok) %verify(not md5 mtime size) %{_localstatedir}/pages/playground/playground.txt
%attr(770,root,http) %config(noreplace,missingok) %verify(not md5 mtime size) %{_localstatedir}/pages/wiki/dokuwiki.txt
%attr(770,root,http) %config(noreplace,missingok) %verify(not md5 mtime size) %{_localstatedir}/pages/wiki/syntax.txt
