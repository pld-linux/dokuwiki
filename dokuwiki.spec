%define		subver	2012-01-25
%define		ver		%(echo %{subver} | tr -d -)
%define		php_min_version 5.2.4
%include	/usr/lib/rpm/macros.php
Summary:	PHP-based Wiki webapplication
Summary(pl.UTF-8):	Aplikacja WWW Wiki oparta na PHP
Name:		dokuwiki
Version:	%{ver}
Release:	1
License:	GPL v2
Group:		Applications/WWW
#Source0:	https://github.com/splitbrain/dokuwiki/tarball/master#/%{name}.tgz
Source0:	http://www.splitbrain.org/_media/projects/dokuwiki/%{name}-%{subver}.tgz
# Source0-md5:	da7ec30fc51c48035adc48dc0535a317
#Source0:	http://www.splitbrain.org/_media/projects/dokuwiki/%{name}-rc%{subver}.tgz
Source1:	%{name}-apache.conf
Source2:	%{name}-lighttpd.conf
Source3:	http://glen.alkohol.ee/pld/jude.png
# Source3-md5:	623344128960e18f86097dfee213ad4a
Source4:	eventum.gif
Source5:	http://forum.skype.com/style_emoticons/skype/skype.png
# Source5-md5:	25c355be038267dc9fdb724b628000b9
Source6:	pld_button.png
# Source6-md5:	185afa921e81bd726b9f0f9f0909dc6e
Source7:	cacti.gif
Source8:	nagios.gif
Source9:	http://trac.edgewall.org/export/9404/trunk/doc/trac_icon_16x16.png
# Source9-md5:	0c19ed35bf677f33f6bea14b3a8a2e10
Source10:	pld.gif
Source11:	http://glen.alkohol.ee/pld/astah.png
# Source11-md5:	b1c999e6988440c9e2af6a12e9a56451
Patch66:	%{name}-config.patch
Patch0:		%{name}-paths.patch
Patch3:		%{name}-config-allow-require.patch
Patch4:		%{name}-geshi.patch
Patch5:		%{name}-http_auth-option.patch
Patch6:		%{name}-nice_exit.patch
Patch8:		%{name}-notify-respect-minor.patch
Patch10:	%{name}-mailtext.patch
Patch11:	%{name}-notifyns.patch
Patch12:	%{name}-mailthreads.patch
Patch13:	%{name}-media-directlink.patch
Patch14:	interwiki-outputonly.patch
Patch15:	simplepie.patch
Patch18:	install.patch
Patch19:	pld-branding.patch
Patch20:	fixprivilegeescalationbug.diff
Patch21:	task-1821.patch
Patch22:	adldap.patch
Patch23:	backlink-rightside.patch
URL:		http://www.dokuwiki.org/dokuwiki
BuildRequires:	fslint
BuildRequires:	rpm-php-pearprov >= 4.4.2-11
BuildRequires:	rpmbuild(macros) >= 1.520
Requires:	php-common >= 4:%{php_min_version}
Requires:	php-geshi >= 1.0.7.19
Requires:	php-session
Requires:	php-simplepie >= 1.0.1
Requires:	php-xml
Requires:	webapps
Requires:	webserver(access)
Requires:	webserver(alias)
Requires:	webserver(php)
Suggests:	php-adldap >= 3.3.1
Suggests:	php-gd
Obsoletes:	dokuwiki-plugin-jquery
# can use gz compression to store attic pages
Suggests:	php-zlib
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{_webapp}
%define		_localstatedir	/var/lib/%{name}
%define		find_lang 	%{_usrlibrpm}/dokuwiki-find-lang.sh %{buildroot}

# bad depsolver
%define		_noautopear	'pear(/usr/share/php/geshi.php)' 'pear(/usr/share/php/adLDAP.php)'

# exclude optional php dependencies
%define		_noautophp	php-bzip2 php-bcmath php-zip php-date php-ftp php-hash php-ldap php-mbstring php-mysql php-pgsql php-tokenizer

%define		_noautoreq	%{_noautophp} %{_noautopear}

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
%setup -q -n %{name}-%{subver}
%patch0 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch8 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1
%patch21 -p1
%patch22 -p1
%patch23 -p1

%patch66 -p1

find -name _dummy | xargs rm
%{__rm} lib/index.html lib/plugins/index.html inc/lang/.htaccess

# we just don't package deleted files, so these get removed automatically on rpm upgrades
%{__rm} data/deleted.files
# source for security.png
%{__rm} data/security.xcf

# use system geshi package
%{__rm} inc/geshi.php
%{__rm} -r inc/geshi

# use system adldap package
%{__rm} inc/adLDAP.php

# use system simplepie package
%{__rm} inc/SimplePie.php

# flash source on git tarballs
rm -rf lib/_fla

# cleanup backups after patching
find . '(' -name '*~' -o -name '*.orig' ')' -print0 | xargs -0 -r -l512 rm -f

%build
md5=$(md5sum -b conf/dokuwiki.php | awk '{print $1}')
if ! grep $md5 install.php; then
	: update %{name}-config.patch -- it is outdated
	exit 1
fi

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/{lang,plugin_lang},%{_localstatedir},%{_appdir}/{bin,inc,lib}}

# hardlink test
cp -al VERSION $RPM_BUILD_ROOT%{_appdir} 2>/dev/null && l=l

cp -a$l *.php $RPM_BUILD_ROOT%{_appdir}
cp -p$l VERSION $RPM_BUILD_ROOT%{_appdir}
cp -a$l bin/* $RPM_BUILD_ROOT%{_appdir}/bin
cp -a$l inc/* $RPM_BUILD_ROOT%{_appdir}/inc
cp -a$l lib/* $RPM_BUILD_ROOT%{_appdir}/lib
cp -a$l conf/* $RPM_BUILD_ROOT%{_sysconfdir}
cp -a$l data/* $RPM_BUILD_ROOT%{_localstatedir}
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/lighttpd.conf
touch $RPM_BUILD_ROOT%{_sysconfdir}/acronyms.local.conf
touch $RPM_BUILD_ROOT%{_sysconfdir}/entities.local.conf
touch $RPM_BUILD_ROOT%{_sysconfdir}/interwiki.local.conf
touch $RPM_BUILD_ROOT%{_sysconfdir}/license.local.php
touch $RPM_BUILD_ROOT%{_sysconfdir}/plugins.local.php
touch $RPM_BUILD_ROOT%{_sysconfdir}/local.php
touch $RPM_BUILD_ROOT%{_sysconfdir}/local.protected.php
touch $RPM_BUILD_ROOT%{_sysconfdir}/mime.local.conf
touch $RPM_BUILD_ROOT%{_sysconfdir}/smileys.local.conf
touch $RPM_BUILD_ROOT%{_sysconfdir}/userstyle.css

ln $RPM_BUILD_ROOT%{_appdir}/lib/images/interwiki/{dokubug,bug}.gif
cp -p %{SOURCE4} $RPM_BUILD_ROOT%{_appdir}/lib/images/interwiki/eventum.gif
cp -p %{SOURCE7} $RPM_BUILD_ROOT%{_appdir}/lib/images/interwiki/cacti.gif
cp -p %{SOURCE8} $RPM_BUILD_ROOT%{_appdir}/lib/images/interwiki/nagios.gif
cp -p %{SOURCE5} $RPM_BUILD_ROOT%{_appdir}/lib/images/interwiki/skype.png
cp -p %{SOURCE9} $RPM_BUILD_ROOT%{_appdir}/lib/images/interwiki/trac.png
cp -p %{SOURCE10} $RPM_BUILD_ROOT%{_appdir}/lib/images/interwiki/pld.gif

cp -p %{SOURCE3} $RPM_BUILD_ROOT%{_appdir}/lib/images/fileicons/jude.png
cp -p %{SOURCE11} $RPM_BUILD_ROOT%{_appdir}/lib/images/fileicons/asta.png

cp -p %{SOURCE6} $RPM_BUILD_ROOT%{_appdir}/lib/tpl/default/images/button-pld.png

# hardlink identical icons.
findup -m $RPM_BUILD_ROOT

# find locales
%find_lang %{name}.lang

%clean
rm -rf $RPM_BUILD_ROOT

%post setup
chmod 770 %{_sysconfdir}
chmod 660 %{_sysconfdir}/local.php
chmod 660 %{_sysconfdir}/plugins.local.php

%postun setup
if [ "$1" = "0" ]; then
	if [ -f %{_sysconfdir}/dokuwiki.php ]; then
		chmod 750 %{_sysconfdir}
		chmod 640 %{_sysconfdir}/local.php
		chmod 640 %{_sysconfdir}/plugins.local.php
	fi
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
%doc README
%dir %attr(750,root,http) %verify(not mode) %{_sysconfdir}
%dir %attr(750,root,http) %{_sysconfdir}/lang
%dir %attr(750,root,http) %{_sysconfdir}/plugin_lang
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lighttpd.conf

%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mediameta.php
%attr(660,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/scheme.conf

%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/acronyms.local.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/entities.local.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/interwiki.local.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/license.local.php
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size mode) %{_sysconfdir}/local.php
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/local.protected.php
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mime.local.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size mode) %{_sysconfdir}/plugins.local.php
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/smileys.local.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/userstyle.css

# use local.php, local.protected.php, etc for local changes
%attr(640,root,http) %config %verify(not md5 mtime size) %{_sysconfdir}/acronyms.conf
%attr(640,root,http) %config %verify(not md5 mtime size) %{_sysconfdir}/entities.conf
%attr(640,root,http) %config %verify(not md5 mtime size) %{_sysconfdir}/interwiki.conf
%attr(640,root,http) %config %verify(not md5 mtime size) %{_sysconfdir}/mime.conf
%attr(640,root,http) %config %verify(not md5 mtime size) %{_sysconfdir}/smileys.conf

%attr(640,root,http) %config %verify(not md5 mtime size) %{_sysconfdir}/dokuwiki.php
%attr(640,root,http) %config %verify(not md5 mtime size) %{_sysconfdir}/license.php
%attr(640,root,http) %config %verify(not md5 mtime size) %{_sysconfdir}/plugins.required.php

# samples. perhaps move to %doc instead?
%attr(640,root,http) %{_sysconfdir}/mysql.conf.php.example
%attr(640,root,http) %{_sysconfdir}/acl.auth.php.dist
%attr(640,root,http) %{_sysconfdir}/wordblock.conf
%attr(640,root,http) %{_sysconfdir}/local.php.dist
%attr(640,root,http) %{_sysconfdir}/users.auth.php.dist

%dir %{_appdir}
%{_appdir}/VERSION
%{_appdir}/doku.php
%{_appdir}/feed.php
%{_appdir}/index.php
%dir %{_appdir}/bin
%attr(755,root,root) %{_appdir}/bin/dwpage.php
%attr(755,root,root) %{_appdir}/bin/indexer.php
%attr(755,root,root) %{_appdir}/bin/render.php
%attr(755,root,root) %{_appdir}/bin/wantedpages.php
%attr(755,root,root) %{_appdir}/bin/striplangs.php

%dir %{_appdir}/inc
%{_appdir}/inc/*.php
%{_appdir}/inc/auth
%{_appdir}/inc/parser

%dir %{_appdir}/lib
%dir %{_appdir}/lib/plugins
%dir %{_appdir}/lib/plugins/acl
%{_appdir}/lib/plugins/acl/*.*
%{_appdir}/lib/plugins/acl/pix
%dir %{_appdir}/lib/plugins/config
%{_appdir}/lib/plugins/config/*.*
%{_appdir}/lib/plugins/config/images
%{_appdir}/lib/plugins/config/settings
%dir %{_appdir}/lib/plugins/plugin
%{_appdir}/lib/plugins/plugin/*.*
%{_appdir}/lib/plugins/plugin/classes
%dir %{_appdir}/lib/plugins/revert
%{_appdir}/lib/plugins/revert/*.*
%dir %{_appdir}/lib/plugins/safefnrecode
%{_appdir}/lib/plugins/safefnrecode/*.*
%dir %{_appdir}/lib/plugins/usermanager
%{_appdir}/lib/plugins/usermanager/*.*
%{_appdir}/lib/plugins/usermanager/images
%dir %{_appdir}/lib/plugins/info
%{_appdir}/lib/plugins/info/*.*
%dir %{_appdir}/lib/plugins/popularity
%{_appdir}/lib/plugins/popularity/*.*
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
%dir %attr(770,root,http) %{_localstatedir}/media_attic
%dir %attr(770,root,http) %{_localstatedir}/media_meta
%dir %attr(770,root,http) %{_localstatedir}/media/wiki
%dir %attr(770,root,http) %{_localstatedir}/meta
%dir %attr(770,root,http) %{_localstatedir}/pages
%dir %attr(770,root,http) %{_localstatedir}/pages/playground
%dir %attr(770,root,http) %{_localstatedir}/pages/wiki
%dir %attr(770,root,http) %{_localstatedir}/tmp

%attr(660,root,http) %config(noreplace,missingok) %verify(not md5 mtime size) %{_localstatedir}/media/wiki/dokuwiki-128.png
%attr(660,root,http) %config(noreplace,missingok) %verify(not md5 mtime size) %{_localstatedir}/pages/wiki/dokuwiki.txt
%attr(660,root,http) %config(noreplace,missingok) %verify(not md5 mtime size) %{_localstatedir}/pages/wiki/syntax.txt
%attr(660,root,http) %config(noreplace,missingok) %verify(not md5 mtime size) %{_localstatedir}/pages/playground/playground.txt
%attr(660,root,http) %config(noreplace,missingok) %verify(not md5 mtime size) %{_localstatedir}/security.png

%files setup
%defattr(644,root,root,755)
%{_appdir}/install.php
