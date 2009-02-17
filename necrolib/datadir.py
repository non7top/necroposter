# Copyright (c) 2005 ActiveState Corp.
# License: MIT
# Author:  Trent Mick (TrentM at ActiveState.com)

"""Cross-platform application utilities:

Utility Functions:
    user_data_dir(...)      path to user-specific app data dir
    site_data_dir(...)      path to all users shared app data dir
"""
#TODO:
# - Add cross-platform versions of other abstracted dir locations, like
#   a cache dir, prefs dir, something like bundle/Contents/SharedSupport
#   on OS X, etc.
#       http://developer.apple.com/documentation/MacOSX/Conceptual/BPRuntimeConfig/Concepts/UserPreferences.html
#       http://developer.apple.com/documentation/MacOSX/Conceptual/BPFileSystem/index.html
#       http://msdn.microsoft.com/library/default.asp?url=/library/en-us/shellcc/platform/shell/reference/enums/csidl.asp
#

import sys
import os


class Error(Exception):
    pass



def user_data_dir(appname, owner=None, version=None):
    """Return full path to the user-specific data dir for this application.
    
        "appname" is the name of application.
        "owner" (only required and used on Windows) is the name of the
            owner or distributing body for this application. Typically
            it is the owning company name.
        "version" is an optional version path element to append to the
            path. You might want to use this if you want multiple versions
            of your app to be able to run independently. If used, this
            would typically be "<major>.<minor>".
    
    Typical user data directories are:
        Windows:    C:\Documents and Settings\USER\Application Data\<owner>\<appname>
        Mac OS X:   ~/Library/Application Support/<appname>
        Unix:       ~/.<lowercased-appname>
    """
    if sys.platform.startswith("win"):
        # Try to make this a unicode path because SHGetFolderPath does
        # not return unicode strings when there is unicode data in the
        # path.
        if owner is None:
            raise Error("must specify 'owner' on Windows")
        from win32com.shell import shellcon, shell
        path = shell.SHGetFolderPath(0, shellcon.CSIDL_APPDATA, 0, 0)
        try:
            path = unicode(path)
        except UnicodeError:
            pass
        path = os.path.join(path, owner, appname)
    elif sys.platform == 'darwin':
        from Carbon import Folder, Folders
        path = Folder.FSFindFolder(Folders.kUserDomain,
                                   Folders.kApplicationSupportFolderType,
                                   Folders.kDontCreateFolder)
        path = os.path.join(path.FSRefMakePath(), appname)
    else:
        path = os.path.expanduser("~/." + appname.lower())
    if version:
        path = os.path.join(path, version)
    return path


def site_data_dir(appname, owner=None, version=None):
    """Return full path to the user-shared data dir for this application.
    
        "appname" is the name of application.
        "owner" (only required and used on Windows) is the name of the
            owner or distributing body for this application. Typically
            it is the owning company name.
        "version" is an optional version path element to append to the
            path. You might want to use this if you want multiple versions
            of your app to be able to run independently. If used, this
            would typically be "<major>.<minor>".
    
    Typical user data directories are:
        Windows:    C:\Documents and Settings\All Users\Application Data\<owner>\<appname>
        Mac OS X:   /Library/Application Support/<appname>
        Unix:       /etc/<lowercased-appname>
    """
    if sys.platform.startswith("win"):
        # Try to make this a unicode path because SHGetFolderPath does
        # not return unicode strings when there is unicode data in the
        # path.
        if owner is None:
            raise Error("must specify 'owner' on Windows")
        from win32com.shell import shellcon, shell
        shellcon.CSIDL_COMMON_APPDATA = 0x23 # missing from shellcon
        path = shell.SHGetFolderPath(0, shellcon.CSIDL_COMMON_APPDATA, 0, 0)
        try:
            path = unicode(path)
        except UnicodeError:
            pass
        path = os.path.join(path, owner, appname)
    elif sys.platform == 'darwin':
        from Carbon import Folder, Folders
        path = Folder.FSFindFolder(Folders.kLocalDomain,
                                   Folders.kApplicationSupportFolderType,
                                   Folders.kDontCreateFolder)
        path = os.path.join(path.FSRefMakePath(), appname)
    else:
        path = "/etc/"+appname.lower()
    if version:
        path = os.path.join(path, version)
    return path


if __name__ == "__main__":
    print "applib: user data dir:", user_data_dir("Komodo", "ActiveState")
    print "applib: site data dir:", site_data_dir("Komodo", "ActiveState")

