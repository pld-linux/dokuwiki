Summary:	PHP-based Wiki webapplication
Name:		dokuwiki
Version:	20070626b
Release:	0.1
License:	GPL v2
Group:		Applications/WWW
Source0:	http://www.splitbrain.org/_media/projects/dokuwiki/%{name}-2007-06-26b.tgz
# Source0-md5:	84e9b5e8e617658bb0264aa3836f23b3
URL:		http://phpwiki.sourceforge.net/
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	webapps
Requires:	webserver(php) >= 4.0.6
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{_webapp}

%description
DokuWiki is a standards compliant, simple to use Wiki, mainly aimed at
creating documentation of any kind. It is targeted at developer teams,
workgroups and small companies. It has a simple but powerful syntax
which makes sure the datafiles remain readable outside the Wiki and
eases the creation of structured texts. All data is stored in plain
text files – no database is required.

%prep
%setup -q -n %{name}-2007-06-26b

cat > apache.conf <<EOF
Alias /%{_webapp} %{_appdir}
<Directory %{_appdir}/>
Deny from all
Allow from 127.0.0.1
</Directory>
EOF

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_appdir},/var/lib/%{name}}

cp -a *.php $RPM_BUILD_ROOT%{_appdir}
cp -a bin conf data inc lib $RPM_BUILD_ROOT%{_appdir}
#cp -a conf/* $RPM_BUILD_ROOT%{_sysconfdir}
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

%files
%defattr(644,root,root,755)
%doc COPYING README VERSION
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(670,root,http) %{_appdir}
%dir %attr(770,root,http) /var/lib/%{name}
