[app]

# (str) Title of your application
title = Kaizo Tool

# (str) Package name
package.name = kaizotool

# (str) Package domain (needed for android/ios packaging)
package.domain = org.kaizotool

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (str) Application version
version = 1.0

# (list) Application requirements
requirements = python3,kivy,kivymd,Pillow

# (bool) Use precompiled python packages
source.include_patterns = assets/*,images/*.png

# (str) Application icon
icon.filename = %(source.dir)s/kaizo.png

# (str) Application presplash
presplash.filename = %(source.dir)s/kaizonova.png

# (str) Supported orientations (landscape, portrait or all)
orientation = portrait

# (bool) Fullscreen (hide status bar)
fullscreen = 0

# (str) Permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE

# (int) Android API to use
android.api = 30

# (int) Android min API
android.minapi = 21

# (int) Android architecture (armeabi-v7a, arm64-v8a, x86, x86_64)
android.arch = arm64-v8a

# (int) Android NDK version to use
android.ndk = 19b

# (bool) Android App Bundle (aab) - This should be False for APK
android.aab = False

# (list) List of Java .jar files to add to the libs so that pyjnius can access
android.add_jars = jars/path/to/your/jar/file.jar

# (list) List of Java files to add to the android project (can be java or a directory containing the files)
android.add_src = src/path/to/your/java/files

# (bool) Log printout (default False)
log_level = 2

# (bool) Remove the .pyc files
remove_pyc = 1

# (str) Python for android directory (this should contain the Android NDK)
android.ndk_path = ~/path/to/your/android/ndk

# (str) Android SDK version to use
android.sdk = 24

# (str) Android Gradle dependencies
android.gradle_dependencies = 'com.android.support:support-compat:27.1.1'

# (str) Android Gradle dependencies to add to compile
android.gradle_dependencies_add = 'implementation "com.android.support:appcompat-v7:27.1.1"'

# (str) Android Gradle dependencies to add to compile
android.gradle_dependencies_add = 'implementation "com.android.support:appcompat-v7:27.1.1"'
