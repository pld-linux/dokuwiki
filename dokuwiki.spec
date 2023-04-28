%define		subver	2023-04-04
%define		ver		%(echo %{subver} | tr -d -)
#define		snap	1
#define		rc_	1
%define		php_min_version 7.2
Summary:	PHP-based Wiki webapplication
Summary(pl.UTF-8):	Aplikacja WWW Wiki oparta na PHP
Name:		dokuwiki
Version:	%{ver}
Release:	1
License:	GPL v2
Group:		Applications/WWW
# Source0Download: https://download.dokuwiki.org/archive
Source0:	https://github.com/dokuwiki/dokuwiki/releases/download/release-%{subver}/dokuwiki-%{subver}.tgz
# Source0-md5:	a112952394f3d4b76efb9dc2f985f99f
Source1:	%{name}-apache.conf
Source2:	%{name}-lighttpd.conf
Source3:	http://glen.alkohol.ee/pld/jude.png
# Source3-md5:	623344128960e18f86097dfee213ad4a
Source4:	eventum.gif
Source5:	preload.php
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
Patch5:		%{name}-http_auth-option.patch
Patch8:		%{name}-notify-respect-minor.patch
Patch10:	%{name}-mailtext.patch
Patch19:	pld-branding.patch
Patch21:	task-1821.patch
Patch24:	more-buttons.patch
Patch27:	iconsizes-dump.patch
URL:		https://www.dokuwiki.org/
BuildRequires:	fslint
BuildRequires:	rpm-php-pearprov >= 4.4.2-11
BuildRequires:	rpmbuild(find_lang) >= 1.41
BuildRequires:	rpmbuild(macros) >= 1.693
Requires:	php(core) >= %{php_min_version}
Requires:	php(session)
Requires:	php(xml)
Requires:	php-geshi >= 1.0.9.1
Requires:	webapps
Requires:	webserver(access)
Requires:	webserver(alias)
Requires:	webserver(php)
Suggests:	php(gd)
Obsoletes:	dokuwiki-plugin-jquery
Obsoletes:	dokuwiki-plugin-showlogin2
Conflicts:	dokuwiki-plugin-gallery < 20161222
Conflicts:	dokuwiki-plugin-icalevents < 20120909
Conflicts:	dokuwiki-plugin-include < 20181129
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
%define		_logdir			/var/log/php/%{name}

%define		_noautoreq_pear lib/byte_safe_strings.php lib/cast_to_int.php lib/error_polyfill.php lib/random.php other/ide_stubs/libsodium.php

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
%patch5 -p1
%patch8 -p1
%patch10 -p1
%patch19 -p1
#%patch21 -p1
#%patch24 -p1
%patch27 -p1
%patch66 -p1

# package as basenames, upgrade overwrite protected with .rpmnew
mv conf/local.php{.dist,}
mv conf/acl.auth.php{.dist,}
mv conf/users.auth.php{.dist,}
mv conf/mysql.conf.php{.example,}

find -name _dummy | xargs %{__rm}
%{__rm} lib/index.html lib/plugins/index.html lib/images/index.html
%{__rm} {conf,inc,bin,data}/.htaccess
%{__rm} vendor/.htaccess
%{__rm} lib/plugins/styling/.travis.yml
%{__rm} -r lib/plugins/*/_test

# we just don't package deleted files, these get removed automatically on rpm upgrades
%{__rm} data/deleted.files
# source for dont-panic-if-you-see-this-in-your-logs-it-means-your-directory-permissions-are-correct.png
%{__rm} data/dont-panic-if-you-see-this-in-your-logs-it-means-your-directory-permissions-are-correct.xcf

%{__rm} lib/scripts/jquery/update.sh

# use system geshi package
%{__rm} -r vendor/geshi/geshi
install -d vendor/geshi/geshi/src
%{__ln} -snf %{php_data_dir}/geshi.php vendor/geshi/geshi/src/geshi.php

# generic vendor cleanup
%{__rm} -v vendor/*/*/composer.*

# use system simplepie package
#%{__rm} inc/SimplePie.php

# pagetools - tools for development
%{__rm} -r lib/tpl/dokuwiki/images/pagetools
%{__rm} lib/tpl/dokuwiki/images/pagetools-build*

%{__sed} -i -e '1 s,#!.*php,#!/usr/bin/php,' bin/*.php

# cleanup backups after patching
find '(' -name '*~' -o -name '*.orig' ')' -print0 | xargs -0 -r -l512 rm -f

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/{lang,plugin_lang},%{_localstatedir},%{_cachedir},%{_appdir},%{_logdir}}

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
cp -p %{SOURCE5} $RPM_BUILD_ROOT%{_appdir}/inc/preload.php

# Move back to conf, to be readonly
install -d $RPM_BUILD_ROOT%{_appdir}/conf
set -- acronyms.conf dokuwiki.php entities.conf interwiki.conf license.php mediameta.php mime.conf mysql.conf.php scheme.conf smileys.conf wordblock.conf
(cd $RPM_BUILD_ROOT%{_sysconfdir} && mv "$@" $RPM_BUILD_ROOT%{_appdir}/conf)

# hardlink identical icons.
findup -m $RPM_BUILD_ROOT

cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/lighttpd.conf

# find locales
%find_lang %{name}.lang --with-dokuwiki

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

%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/plugins.php
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/acl.auth.php
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/acronyms.local.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/entities.local.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/interwiki.local.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/license.local.php
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/local.protected.php
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mime.local.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/smileys.local.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/users.auth.php
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/userscript.js
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/userstyle.css

%attr(640,root,http) %config(noreplace) %verify(not md5 mode mtime size) %{_sysconfdir}/local.php
%attr(640,root,http) %config(noreplace) %verify(not md5 mode mtime size) %{_sysconfdir}/plugins.local.php

# use local.php, local.protected.php, etc for local changes
%attr(640,root,http) %config %verify(not md5 mtime size) %{_sysconfdir}/manifest.json
%attr(640,root,http) %config %verify(not md5 mtime size) %{_sysconfdir}/plugins.required.php

%dir %{_appdir}
%{_appdir}/VERSION
%{_appdir}/doku.php
%{_appdir}/feed.php
%{_appdir}/index.php
%{_appdir}/conf
%dir %{_appdir}/bin
%attr(755,root,root) %{_appdir}/bin/dwpage.php
%attr(755,root,root) %{_appdir}/bin/gittool.php
%attr(755,root,root) %{_appdir}/bin/indexer.php
%attr(755,root,root) %{_appdir}/bin/plugin.php
%attr(755,root,root) %{_appdir}/bin/render.php
%attr(755,root,root) %{_appdir}/bin/striplangs.php
%attr(755,root,root) %{_appdir}/bin/wantedpages.php

%dir %{_appdir}/inc
%{_appdir}/inc/*.php
%{_appdir}/inc/preload.php.dist
%{_appdir}/inc/Action
%{_appdir}/inc/Cache
%{_appdir}/inc/ChangeLog
%{_appdir}/inc/Debug
%{_appdir}/inc/Exception
%{_appdir}/inc/Extension
%{_appdir}/inc/File
%{_appdir}/inc/Form
%{_appdir}/inc/HTTP
%{_appdir}/inc/Input
%{_appdir}/inc/Menu
%{_appdir}/inc/Parsing
%{_appdir}/inc/Remote
%{_appdir}/inc/Search
%{_appdir}/inc/Sitemap
%{_appdir}/inc/Subscriptions
%{_appdir}/inc/Ui
%{_appdir}/inc/Utf8
%{_appdir}/inc/parser

# composer generated vendor autoload
%dir %{_appdir}/vendor
%{_appdir}/vendor/README
%{_appdir}/vendor/autoload.php
%{_appdir}/vendor/composer

# bundled packages
# verbose files to detect new addons
%dir %{_appdir}/vendor/aziraphale
%dir %{_appdir}/vendor/geshi
%dir %{_appdir}/vendor/kissifrot
%dir %{_appdir}/vendor/marcusschwarz
%dir %{_appdir}/vendor/openpsa
%dir %{_appdir}/vendor/phpseclib
%dir %{_appdir}/vendor/simplepie
%dir %{_appdir}/vendor/splitbrain
%{_appdir}/vendor/aziraphale/email-address-validator
%{_appdir}/vendor/geshi/geshi
%{_appdir}/vendor/kissifrot/php-ixr
%{_appdir}/vendor/marcusschwarz/lesserphp
%{_appdir}/vendor/openpsa/universalfeedcreator
%{_appdir}/vendor/phpseclib/phpseclib
%{_appdir}/vendor/simplepie/simplepie
%{_appdir}/vendor/splitbrain/php-archive
%{_appdir}/vendor/splitbrain/php-cli
%{_appdir}/vendor/splitbrain/php-jsstrip
%{_appdir}/vendor/splitbrain/slika

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
%dir %{_appdir}/lib/plugins/authpdo
%{_appdir}/lib/plugins/authpdo/*.php
%{_appdir}/lib/plugins/authpdo/*.txt
%{_appdir}/lib/plugins/authpdo/README
%{_appdir}/lib/plugins/authpdo/conf
%dir %{_appdir}/lib/plugins/authplain
%{_appdir}/lib/plugins/authplain/*.php
%{_appdir}/lib/plugins/authplain/*.txt
%dir %{_appdir}/lib/plugins/config
%{_appdir}/lib/plugins/config/*.*
%{_appdir}/lib/plugins/config/core
%{_appdir}/lib/plugins/config/images
%{_appdir}/lib/plugins/config/settings
%dir %{_appdir}/lib/plugins/extension
%{_appdir}/lib/plugins/extension/*.*
%{_appdir}/lib/plugins/extension/helper
%{_appdir}/lib/plugins/extension/images
%dir %{_appdir}/lib/plugins/logviewer
%{_appdir}/lib/plugins/logviewer/*.*
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
%attr(660,root,http) %config(noreplace,missingok) %verify(not md5 mtime size) %{_localstatedir}/media/wiki/dokuwiki.svg
%attr(660,root,http) %config(noreplace,missingok) %verify(not md5 mtime size) %{_localstatedir}/pages/wiki/dokuwiki.txt
%attr(660,root,http) %config(noreplace,missingok) %verify(not md5 mtime size) %{_localstatedir}/pages/wiki/syntax.txt
%attr(660,root,http) %config(noreplace,missingok) %verify(not md5 mtime size) %{_localstatedir}/pages/wiki/welcome.txt
%attr(660,root,http) %config(noreplace,missingok) %verify(not md5 mtime size) %{_localstatedir}/pages/playground/playground.txt
%attr(660,root,http) %config(noreplace,missingok) %verify(not md5 mtime size) %{_localstatedir}/dont-panic-if-you-see-this-in-your-logs-it-means-your-directory-permissions-are-correct.png

%dir %attr(770,root,http) %{_cachedir}
%dir %attr(770,root,http) %{_logdir}

%files setup
%defattr(644,root,root,755)
%{_appdir}/install.php
