<?php
/**
 * The config cascade
 *
 * This array configures the locations of various files in the
 * DokuWiki directory hierarchy.
 */

define('DOKU_LOCAL', '/etc/webapps/dokuwiki/');
define('DOKU_CONF', dirname(__DIR__) . '/conf/');

$config_cascade = array(
    'main' => array(
        'default' => array(DOKU_CONF . 'dokuwiki.php'),
        'local' => array(DOKU_LOCAL . 'local.php'),
        'protected' => array(DOKU_LOCAL . 'local.protected.php'),
    ),
    'acronyms' => array(
        'default' => array(DOKU_CONF . 'acronyms.conf'),
        'local' => array(DOKU_LOCAL . 'acronyms.local.conf'),
    ),
    'entities' => array(
        'default' => array(DOKU_CONF . 'entities.conf'),
        'local' => array(DOKU_LOCAL . 'entities.local.conf'),
    ),
    'interwiki' => array(
        'default' => array(DOKU_CONF . 'interwiki.conf'),
        'local' => array(DOKU_LOCAL . 'interwiki.local.conf'),
    ),
    'license' => array(
        'default' => array(DOKU_CONF . 'license.php'),
        'local' => array(DOKU_LOCAL . 'license.local.php'),
    ),
    'manifest' => array(
        'default' => array(DOKU_CONF . 'manifest.json'),
        'local' => array(DOKU_LOCAL . 'manifest.local.json'),
    ),
    'mediameta' => array(
        'default' => array(DOKU_CONF . 'mediameta.php'),
        'local' => array(DOKU_LOCAL . 'mediameta.local.php'),
    ),
    'mime' => array(
        'default' => array(DOKU_CONF . 'mime.conf'),
        'local' => array(DOKU_LOCAL . 'mime.local.conf'),
    ),
    'scheme' => array(
        'default' => array(DOKU_CONF . 'scheme.conf'),
        'local' => array(DOKU_LOCAL . 'scheme.local.conf'),
    ),
    'smileys' => array(
        'default' => array(DOKU_CONF . 'smileys.conf'),
        'local' => array(DOKU_LOCAL . 'smileys.local.conf'),
    ),
    'wordblock' => array(
        'default' => array(DOKU_CONF . 'wordblock.conf'),
        'local' => array(DOKU_LOCAL . 'wordblock.local.conf'),
    ),
    'userstyle' => array(
        'screen' => array(DOKU_LOCAL . 'userstyle.css', DOKU_LOCAL . 'userstyle.less'),
        'print' => array(DOKU_LOCAL . 'userprint.css', DOKU_LOCAL . 'userprint.less'),
        'feed' => array(DOKU_LOCAL . 'userfeed.css', DOKU_LOCAL . 'userfeed.less'),
        'all' => array(DOKU_LOCAL . 'userall.css', DOKU_LOCAL . 'userall.less')
    ),
    'userscript' => array(
        'default' => array(DOKU_LOCAL . 'userscript.js')
    ),
    'styleini' => array(
        'default' => array(DOKU_INC . 'lib/tpl/%TEMPLATE%/' . 'style.ini'),
        'local' => array(DOKU_LOCAL . 'tpl/%TEMPLATE%/' . 'style.ini')
    ),
    'acl' => array(
        'default' => DOKU_LOCAL . 'acl.auth.php',
    ),
    'plainauth.users' => array(
        'default' => DOKU_LOCAL . 'users.auth.php',
        'protected' => '' // not used by default
    ),
    'plugins' => array(
        'default' => array(DOKU_LOCAL . 'plugins.php'),
        'local' => array(DOKU_LOCAL . 'plugins.local.php'),
        'protected' => array(
            DOKU_CONF . 'plugins.required.php',
            DOKU_LOCAL . 'plugins.protected.php',
        ),
    ),
    'lang' => array(
        'core' => array(DOKU_LOCAL . 'lang/'),
        'plugin' => array(DOKU_LOCAL . 'plugin_lang/'),
        'template' => array(DOKU_LOCAL . 'template_lang/')
    ),
);
