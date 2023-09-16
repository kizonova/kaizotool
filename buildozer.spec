[app]

# (str) Title of your application
title = kaizotool

# (str) Package name
package_name = kaizotool
version = 0.0.1

# (str) Package domain (needed for android/ios packaging)
package.domain = org.test

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (list) Application requirements
requirements = python3,kivy,kivymd,pillow

# (list) Permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE

# (str) Icon of the application
icon.filename = %(source.dir)s/images/kaizonova.png

# (str) Background image for the application
presplash.filename = %(source.dir)s/images/kaizo.png
