"""
@file 
@brief This file contains the current version number of OpenShot, along with other global settings
"""

import os

VERSION = "2.1.0-dev1"
DATE = "20160327000000"
NAME = "openshot-qt"
PRODUCT_NAME = "OpenShot Video Editor"
GPL_VERSION = "3"
DESCRIPTION = "Create and edit videos and movies"
COMPANY_NAME = "OpenShot Studios, LLC"
COPYRIGHT = "Copyright (c) 2008-2016 %s" % COMPANY_NAME
CWD = os.getcwd()
PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))  # Primary openshot folder
HOME_PATH = os.path.join(os.path.expanduser("~"))
USER_PATH = os.path.join(HOME_PATH, ".openshot_qt")
BACKUP_PATH = os.path.join(USER_PATH, "backup")
BLENDER_PATH = os.path.join(USER_PATH, "blender")
THUMBNAIL_PATH = os.path.join(USER_PATH, "thumbnail")
CACHE_PATH = os.path.join(USER_PATH, "cache")
PREVIEW_CACHE_PATH = os.path.join(USER_PATH, "preview-cache")
TITLE_PATH = os.path.join(USER_PATH, "title")
PROFILES_PATH = os.path.join(PATH, "profiles")
IMAGES_PATH = os.path.join(PATH, "images")
TRANSITIONS_PATH = os.path.join(USER_PATH, "transitions")
EXPORT_PRESETS_DIR = os.path.join(PATH, "presets")
EXPORT_TESTS = os.path.join(USER_PATH, "tests")
USER_PROFILES_PATH = os.path.join(USER_PATH, "profiles")

for folder in [USER_PATH, THUMBNAIL_PATH, CACHE_PATH, BLENDER_PATH, TITLE_PATH, PROFILES_PATH, IMAGES_PATH,
               TRANSITIONS_PATH, EXPORT_TESTS, BACKUP_PATH, USER_PROFILES_PATH, PREVIEW_CACHE_PATH]:
    if not os.path.exists(folder.encode("UTF-8")):
        os.makedirs(folder, exist_ok=True)

# names of all contributers, using "u" for unicode encoding
AF = {"name": u"Andy Finch", "email": "andy@openshot.org", "website":"http://openshot.org/developers/andy"}
NF = {"name": u"Noah Figg", "email": "eggmunkee@hotmail.com"}
JT = {"name": u"Jonathan Thomas", "email": "jonathan@openshot.org", "website":"http://openshot.org/developers/jonathan"}
OG = {"name": u"Olivier Girard", "email": "olivier@openshot.org", "website":"http://openshot.org/developers/olivier"}
CP = {"name": u"Cody Parker", "email": "cody@yourcodepro.com", "website":"http://openshot.org/developers/cody_parker"}

SUPPORTED_LANGUAGES = ['en_US']
for lang in os.listdir(os.path.join(PATH, 'locale')):
    if lang not in ["Openshot"] and not os.path.isfile(os.path.join(PATH, 'locale', lang)):
        SUPPORTED_LANGUAGES.append(lang)

# credits
CREDITS = {
    "code": [JT, NF, AF, CP, OG],
    "artwork": [JT],
    "documentation": [JT],
    "translation": [OG],
}

SETUP = {
    "name": NAME,
    "version": VERSION,
    "author": JT["name"] + " and others",
    "author_email": JT["email"],
    "maintainer": JT["name"],
    "maintainer_email": JT["email"],
    "url": "http://www.openshot.org/",
    "license": "GNU GPL v." + GPL_VERSION,
    "description": DESCRIPTION,
    "long_description": "Create and edit videos and movies\n"
                        " OpenShot Video Editor is a free, open-source, non-linear video editor. It\n"
                        " can create and edit videos and movies using many popular video, audio, \n"
                        " image formats.  Create videos for YouTube, Flickr, Vimeo, Metacafe, iPod,\n"
                        " Xbox, and many more common formats!\n"
                        ".\n"
                        " Features include:\n"
                        "  * Multiple tracks (layers)\n"
                        "  * Compositing, image overlays, and watermarks\n"
                        "  * Support for image sequences (rotoscoping)\n"
                        "  * Key-frame animation\n  * Video and audio effects (chroma-key)\n"
                        "  * Transitions (lumas and masks)\n"
                        "  * 3D animation (titles and simulations)\n"
                        "  * Upload videos (YouTube and Vimeo supported)",

    # see http://pypi.python.org/pypi?%3Aaction=list_classifiers
    "classifiers": [
                       "Development Status :: 5 - Production/Stable",
                       "Environment :: X11 Applications",
                       "Environment :: X11 Applications :: GTK",
                       "Intended Audience :: End Users/Desktop",
                       "License :: OSI Approved :: GNU General Public License (GPL)",
                       "Operating System :: OS Independent",
                       "Operating System :: POSIX :: Linux",
                       "Programming Language :: Python",
                       "Topic :: Artistic Software",
                       "Topic :: Multimedia :: Video :: Non-Linear Editor", ] +
                   ["Natural Language :: " + language for language in SUPPORTED_LANGUAGES],

    # Automatic launch script creation
    "entry_points": {
        "gui_scripts": [
            "openshot-qt = openshot_qt.launch:main"
        ]
    }
}
