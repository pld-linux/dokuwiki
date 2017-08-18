%define		subver	2017-02-19c
%define		ver		%(echo %{subver} | tr -d -)
#define		snap	1
#define		rc_	1
%define		php_min_version 5.3.3
%include	/usr/lib/rpm/macros.php
Summary:	PHP-based Wiki webapplication
Summary(pl.UTF-8):	Aplikacja WWW Wiki oparta na PHP
Name:		dokuwiki
Version:	%{ver}
Release:	0.6
License:	GPL v2
Group:		Applications/WWW
# Source0Download: https://download.dokuwiki.org/archive
Source0:	https://download.dokuwiki.org/src/dokuwiki/%{name}-%{subver}.tgz
# Source0-md5:	324ae70a6322057604edc04b39c9b334
Source1:	%{name}-apache.conf
Source2:	%{name}-lighttpd.conf
Source3:	http://glen.alkohol.ee/pld/jude.png
# Source3-md5:	623344128960e18f86097dfee213ad4a
Source4:	eventum.gif
Source6:	pld_button.png
# Source6-md5:	185afa921e81bd726b9f0f9f0909dc6e
Source7:	cacti.gif
Source8:	nagios.gif
Source9:	http://trac.edgewall.org/export/9404/trunk/doc/trac_icon_16x16.png
# Source9-md5:	0c19ed35bf677f33f6bea14b3a8a2e10
Source10:	pld.gif
Source11:	http://glen.alkohol.ee/pld/astah.png
# Source11-md5:	b1c999e6988440c9e2af6a12e9a56451
Source12:	gitlab.png
# Source12-md5:	619cec6f2b083269b1ec9cd50d9e6ef2
Source13:	http://mirrors.jenkins-ci.org/art/jenkins-logo/16x16/headshot.png?/jenkins.png
# Source13-md5:	ae892e4ca43ffab88f6e3dca951f3e8a
Patch66:	%{name}-config.patch
Patch0:		%{name}-paths.patch
Patch2:		style-width.patch
Patch4:		%{name}-geshi.patch
Patch5:		%{name}-http_auth-option.patch
Patch8:		%{name}-notify-respect-minor.patch
Patch10:	%{name}-mailtext.patch
Patch11:	%{name}-notifyns.patch
Patch19:	pld-branding.patch
Patch20:	fixprivilegeescalationbug.diff
Patch21:	task-1821.patch
Patch24:	more-buttons.patch
Patch26:	system-lessphp.patch
Patch27:	iconsizes-dump.patch
URL:		https://www.dokuwiki.org/
BuildRequires:	fslint
BuildRequires:	rpm-php-pearprov >= 4.4.2-11
BuildRequires:	rpmbuild(macros) >= 1.693
Requires:	lessphp >= 0.3.9
Requires:	php(core) >= %{php_min_version}
Requires:	php(session)
Requires:	php(xml)
Requires:	php-geshi >= 1.0.7.19
Requires:	php-seclib >= 0.3.5
Requires:	php-simplepie >= 1.0.1
Requires:	webapps
Requires:	webserver(access)
Requires:	webserver(alias)
Requires:	webserver(php)
Suggests:	php(gd)
Obsoletes:	dokuwiki-plugin-jquery
Obsoletes:	dokuwiki-plugin-showlogin2
Conflicts:	dokuwiki-plugin-gallery < 20161222
Conflicts:	dokuwiki-plugin-icalevents < 20120909
Conflicts:	dokuwiki-plugin-odt < 20170218
# can use gz compression to store attic pages
Suggests:	php(zlib)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{_webapp}
%define		_localstatedir	/var/lib/%{name}
%define		_cachedir		/var/cache/%{name}
%define		find_lang 	%{_usrlibrpm}/dokuwiki-find-lang.sh %{buildroot}

%define		_noautoreq_pear /usr/share/php/geshi.php

# exclude optional php dependencies
%define		_noautophp	php-bzip2 php-bcmath php-zip php-date php-ftp php-hash php-ldap php-mbstring php-mysql php-pgsql php-tokenizer

%define		_noautoreq	%{_noautophp}

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
%setup -q -n %{name}-%{?rc_:rc}%{subver} %{?snap:-c}
%if 0%{?snap:1}
mv *-dokuwiki-*/* .
test -e VERSION || echo %{subver}-git > VERSION
%endif
install -d data/pages/playground
test -e data/pages/playground/playground.txt || \
echo '====== PlayGround ======' >  data/pages/playground/playground.txt

%patch0 -p1
%patch2 -p1
%patch4 -p1
%patch5 -p1
%patch8 -p1
%patch10 -p1
%patch11 -p1
%patch19 -p1
%patch20 -p1
%patch21 -p1
%patch24 -p1
%patch26 -p1
%patch27 -p1

%patch66 -p1

# package as basenames, upgrade overwrite protected with .rpmnew
mv conf/local.php{.dist,}
mv conf/acl.auth.php{.dist,}
mv conf/users.auth.php{.dist,}
mv conf/mysql.conf.php{.example,}

find -name _dummy | xargs %{__rm}
%{__rm} lib/index.html lib/plugins/index.html lib/images/index.html
%{__rm} {conf,inc,bin,data,inc/lang}/.htaccess

# we just don't package deleted files, these get removed automatically on rpm upgrades
%{__rm} data/deleted.files
# source for security.png
%{__rm} data/security.xcf

%{__rm} lib/scripts/jquery/update.sh

# use system geshi package
%{__rm} -r vendor/easybook/geshi
rmdir vendor/easybook

# use system simplepie package
#%{__rm} inc/SimplePie.php

# use system lessphp package
%{__rm} inc/lessc.inc.php

# flash source on git tarballs
rm -rf lib/plugins/testing
rm -rf lib/plugins/*/_test

# pagetools - tools for development
%{__rm} -r lib/tpl/dokuwiki/images/pagetools
%{__rm} lib/tpl/dokuwiki/images/pagetools-build*

# cleanup backups after patching
find '(' -name '*~' -o -name '*.orig' ')' -print0 | xargs -0 -r -l512 rm -f

%build
md5=$(md5sum -b conf/dokuwiki.php | awk '{print $1}')
if ! grep $md5 install.php; then
	: update %{name}-config.patch -- it is outdated
	exit 1
fi

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/{lang,plugin_lang},%{_localstatedir},%{_cachedir},%{_appdir}}

# hardlink test
cp -al VERSION $RPM_BUILD_ROOT%{_appdir} 2>/dev/null && l=l

cp -a$l *.php $RPM_BUILD_ROOT%{_appdir}
cp -p$l VERSION $RPM_BUILD_ROOT%{_appdir}
cp -a$l bin $RPM_BUILD_ROOT%{_appdir}
cp -a$l inc $RPM_BUILD_ROOT%{_appdir}
cp -a$l lib $RPM_BUILD_ROOT%{_appdir}
cp -a$l vendor $RPM_BUILD_ROOT%{_appdir}
cp -a$l conf/* $RPM_BUILD_ROOT%{_sysconfdir}
cp -a$l data/* $RPM_BUILD_ROOT%{_localstatedir}
touch $RPM_BUILD_ROOT%{_sysconfdir}/acronyms.local.conf
touch $RPM_BUILD_ROOT%{_sysconfdir}/entities.local.conf
touch $RPM_BUILD_ROOT%{_sysconfdir}/interwiki.local.conf
touch $RPM_BUILD_ROOT%{_sysconfdir}/license.local.php
touch $RPM_BUILD_ROOT%{_sysconfdir}/plugins.local.php
touch $RPM_BUILD_ROOT%{_sysconfdir}/local.protected.php
touch $RPM_BUILD_ROOT%{_sysconfdir}/mime.local.conf
touch $RPM_BUILD_ROOT%{_sysconfdir}/smileys.local.conf
touch $RPM_BUILD_ROOT%{_sysconfdir}/userscript.js
touch $RPM_BUILD_ROOT%{_sysconfdir}/userstyle.css

# https://github.com/splitbrain/dokuwiki/pull/1247
#ln $RPM_BUILD_ROOT%{_appdir}/lib/images/interwiki/{dokubug,bug}.gif
cp -p %{SOURCE4} $RPM_BUILD_ROOT%{_appdir}/lib/images/interwiki/eventum.gif
cp -p %{SOURCE7} $RPM_BUILD_ROOT%{_appdir}/lib/images/interwiki/cacti.gif
cp -p %{SOURCE8} $RPM_BUILD_ROOT%{_appdir}/lib/images/interwiki/nagios.gif
cp -p %{SOURCE9} $RPM_BUILD_ROOT%{_appdir}/lib/images/interwiki/trac.png
cp -p %{SOURCE10} $RPM_BUILD_ROOT%{_appdir}/lib/images/interwiki/pld.gif
cp -p %{SOURCE12} $RPM_BUILD_ROOT%{_appdir}/lib/images/interwiki/gitlab.png
cp -p %{SOURCE13} $RPM_BUILD_ROOT%{_appdir}/lib/images/interwiki/jenkins.png

cp -p %{SOURCE3} $RPM_BUILD_ROOT%{_appdir}/lib/images/fileicons/jude.png
cp -p %{SOURCE11} $RPM_BUILD_ROOT%{_appdir}/lib/images/fileicons/asta.png

cp -p %{SOURCE6} $RPM_BUILD_ROOT%{_appdir}/lib/tpl/dokuwiki/images/button-pld.png

# hardlink identical icons.
findup -m $RPM_BUILD_ROOT

cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/lighttpd.conf

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
if [ -d %{_localstatedir}/cache ]; then
	rm -rf %{_localstatedir}/cache
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
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/plugins.php
%attr(660,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/scheme.conf

%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/acl.auth.php
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/acronyms.local.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/entities.local.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/interwiki.local.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/license.local.php
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/local.protected.php
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mime.local.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/smileys.local.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/userscript.js
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/userstyle.css
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/users.auth.php
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mysql.conf.php

%attr(640,root,http) %config(noreplace) %verify(not md5 mode mtime size) %{_sysconfdir}/local.php
%attr(640,root,http) %config(noreplace) %verify(not md5 mode mtime size) %{_sysconfdir}/plugins.local.php

# use local.php, local.protected.php, etc for local changes
%attr(640,root,http) %config %verify(not md5 mtime size) %{_sysconfdir}/acronyms.conf
%attr(640,root,http) %config %verify(not md5 mtime size) %{_sysconfdir}/entities.conf
%attr(640,root,http) %config %verify(not md5 mtime size) %{_sysconfdir}/interwiki.conf
%attr(640,root,http) %config %verify(not md5 mtime size) %{_sysconfdir}/mime.conf
%attr(640,root,http) %config %verify(not md5 mtime size) %{_sysconfdir}/smileys.conf
%attr(640,root,http) %config %verify(not md5 mtime size) %{_sysconfdir}/wordblock.conf

%attr(640,root,http) %config %verify(not md5 mtime size) %{_sysconfdir}/dokuwiki.php
%attr(640,root,http) %config %verify(not md5 mtime size) %{_sysconfdir}/license.php
%attr(640,root,http) %config %verify(not md5 mtime size) %{_sysconfdir}/plugins.required.php

%dir %{_appdir}
%{_appdir}/VERSION
%{_appdir}/doku.php
%{_appdir}/feed.php
%{_appdir}/index.php
%dir %{_appdir}/bin
%attr(755,root,root) %{_appdir}/bin/dwpage.php
%attr(755,root,root) %{_appdir}/bin/gittool.php
%attr(755,root,root) %{_appdir}/bin/indexer.php
%attr(755,root,root) %{_appdir}/bin/render.php
%attr(755,root,root) %{_appdir}/bin/striplangs.php
%attr(755,root,root) %{_appdir}/bin/wantedpages.php

%dir %{_appdir}/inc
%{_appdir}/inc/*.php
%{_appdir}/inc/preload.php.dist
%{_appdir}/inc/Form
%{_appdir}/inc/Ui
%{_appdir}/inc/parser

# composer generated vendor autoload
%dir %{_appdir}/vendor
%{_appdir}/vendor/README
%{_appdir}/vendor/autoload.php
%{_appdir}/vendor/composer

# bundled packages
# verbose files to detect new addons
%dir %{_appdir}/vendor/splitbrain
%{_appdir}/vendor/splitbrain/php-archive

%dir %{_appdir}/vendor/paragonie
%{_appdir}/vendor/paragonie/random_compat

%dir %{_appdir}/vendor/phpseclib
%{_appdir}/vendor/phpseclib/phpseclib

%dir %{_appdir}/vendor/simplepie
%{_appdir}/vendor/simplepie/simplepie

%dir %{_appdir}/lib
# allow plugins dir permission change to allow installation of plugins from admin
# however does not work with rpm 4.5
%dir %config %verify(not group mode) %{_appdir}/lib/plugins

%{_appdir}/lib/plugins/*.php
%dir %{_appdir}/lib/plugins/acl
%{_appdir}/lib/plugins/acl/*.*
%{_appdir}/lib/plugins/acl/pix
%dir %{_appdir}/lib/plugins/authad
%{_appdir}/lib/plugins/authad/*.php
%{_appdir}/lib/plugins/authad/*.txt
%{_appdir}/lib/plugins/authad/adLDAP
%{_appdir}/lib/plugins/authad/conf
%dir %{_appdir}/lib/plugins/authldap
%{_appdir}/lib/plugins/authldap/*.php
%{_appdir}/lib/plugins/authldap/*.txt
%{_appdir}/lib/plugins/authldap/conf
%dir %{_appdir}/lib/plugins/authmysql
%{_appdir}/lib/plugins/authmysql/*.php
%{_appdir}/lib/plugins/authmysql/*.txt
%{_appdir}/lib/plugins/authmysql/conf
%dir %{_appdir}/lib/plugins/authpdo
%{_appdir}/lib/plugins/authpdo/*.php
%{_appdir}/lib/plugins/authpdo/*.txt
%{_appdir}/lib/plugins/authpdo/README
%{_appdir}/lib/plugins/authpdo/conf
%{_appdir}/lib/plugins/authpgsql/*.php
%{_appdir}/lib/plugins/authpgsql/conf
%{_appdir}/lib/plugins/authpgsql/*.txt
%dir %{_appdir}/lib/plugins/authpgsql
%dir %{_appdir}/lib/plugins/authplain
%{_appdir}/lib/plugins/authplain/*.php
%{_appdir}/lib/plugins/authplain/*.txt
%dir %{_appdir}/lib/plugins/config
%{_appdir}/lib/plugins/config/*.*
%{_appdir}/lib/plugins/config/images
%{_appdir}/lib/plugins/config/settings
%dir %{_appdir}/lib/plugins/extension
%{_appdir}/lib/plugins/extension/*.*
%{_appdir}/lib/plugins/extension/helper
%{_appdir}/lib/plugins/extension/images
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
%dir %{_appdir}/lib/plugins/styling
%{_appdir}/lib/plugins/styling/README
%{_appdir}/lib/plugins/styling/*.*

%{_appdir}/lib/images
%{_appdir}/lib/scripts
%{_appdir}/lib/styles
%{_appdir}/lib/exe

%dir %{_appdir}/lib/tpl
%{_appdir}/lib/tpl/index.php

%dir %{_appdir}/lib/tpl/dokuwiki
%{_appdir}/lib/tpl/dokuwiki/css
%{_appdir}/lib/tpl/dokuwiki/images
%{_appdir}/lib/tpl/dokuwiki/*.info.txt
%{_appdir}/lib/tpl/dokuwiki/*.ini
%{_appdir}/lib/tpl/dokuwiki/*.js
%{_appdir}/lib/tpl/dokuwiki/*.php

%dir %attr(770,root,http) %{_localstatedir}
%dir %attr(770,root,http) %{_localstatedir}/attic
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
%attr(660,root,http) %config(noreplace,missingok) %verify(not md5 mtime size) %{_localstatedir}/pages/wiki/welcome.txt
%attr(660,root,http) %config(noreplace,missingok) %verify(not md5 mtime size) %{_localstatedir}/pages/playground/playground.txt
%attr(660,root,http) %config(noreplace,missingok) %verify(not md5 mtime size) %{_localstatedir}/security.png

%dir %attr(770,root,http) %{_cachedir}

%files setup
%defattr(644,root,root,755)
%{_appdir}/install.php


