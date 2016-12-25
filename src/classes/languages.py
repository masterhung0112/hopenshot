import os
import locale

from classes import info
from classes.logger import log
from PyQt5.QtCore import QLocale, QTranslator, QCoreApplication


def init_languages():
    
    translator_types = (
        {"type": 'OpenShot',
         "pattern": os.path.join('%s', 'LC_MESSAGES', 'OpenShot'),
         "path": os.path.join(info.PATH, 'locale')
        },
    )
    
    # Get app instance
    app = QCoreApplication.instance()
    
    # Determine the environment locale, or default to system locale name
    locale_names = [
        os.environ.get('LANG', QLocale().system().name()),
        os.environ.get('LOCALE', QLocale().system().name())
    ]
    
    # Output all system languages detected
    log.info("Qt Detected Languages: {}".format(QLocale().system().uiLanguages()))
    log.info("LANG Environment Variable: {}".format(os.environ.get('LANG', QLocale().system().name())))
    log.info("LOCALE Environment Variable: {}".format(os.environ.get('LOCALE', QLocale().system().name())))
    
    locale.setlocale(locale.LC_ALL, 'C')  # use default (C) locale
    
    found_language = False
    for locale_name in locale_names:
        
        # Don't try on default locale, since it fails to load what is the default language
        if 'en_US' in locale_name:
            log.info("Skipping English language (no need for translation): {}".format(locale_name))
            continue
    
        for type in translator_types:
            trans = QTranslator(app)
            if find_language_match(locale_name, type["path"], type["pattern"], trans):
                app.installTranslator(trans)
                found_languages = True
        
        # Exit if found language
        if found_languages:
            log.info("Exiting translation system (since we successfully loaded: {})".format(locale_name))
            break
            
    
def find_language_match(locale_name, path, pattern, trans):
    success = False
    locale_parts = locale_name.split('_')
    
    i = len(locale_parts)
    while not success and i > 0:
        formatted_name = pattern % '_'.join(locale_parts[:i])
        log.info('Attempting to load {} in \'{}\''.format(formatted_name, path))
        success = trans.load(formatted_name, path)
        if success:
            log.info('Successfully loaded {} in \'{}\''.format(formatted_name, path))
        i -= 1
    
    return success

