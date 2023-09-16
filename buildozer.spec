[app]

# (str) Title of your application
title = Kaizo Tool

# (str) Package name
package.name = kaizotool

# (str) Package domain (needed for android/ios packaging)
package.domain = org.kaizotool

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (str) Application versioning (method 1)
version = 1.0

# (list) Application requirements
requirements = python3,kivy,kivymd,Pillow

# (str) Custom source folders ( separate with commas )
source.pkgs = lib/py

# (list) Garden requirements (kivy garden flowers)
#garden_requirements =

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
icon.filename = %(source.dir)s/kaizo.png

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (string) Permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE

# (int) Target Android API, should be as high as possible.
android.api = 29

# (int) Minimum Android API
android.minapi = 21

# (int) Android SDK version to use
android.sdk = 29

# (str) Android NDK version to use
#android.ndk = 19b

# (int) Android NDK API to use. This is the minimum API your app will work on.
#android.ndk_api = 21

# (bool) Use --private data storage (True) or --dir public storage (False)
#android.private_storage = True

# (str) Android NDK directory (if empty, it will be automatically downloaded.)
#android.ndk_path =

# (str) Android SDK directory (if empty, it will be automatically downloaded.)
#android.sdk_path =
