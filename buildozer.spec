
[app]
# (str) Title of your application
title = الميقاتي الفلكي برو

# (str) Package name
package.name = meeqat_pro

# (str) Package domain (needed for android packaging)
package.domain = org.hassan_astro

# (str) Source code where the main.py is located
source.dir = .

# (list) Source files to include (تأكد من شمول الخطوط والملفات الحسابية)
source.include_exts = py,png,jpg,kv,atlas,ttf,se1,json

# (str) Application version
version = 1.0

# (list) Application requirements
# هذا السطر هو الذي سيجلب كل المكتبات الضخمة ليعمل التطبيق
requirements = python3,kivy==2.2.1,swisseph,arabic-reshaper,python-bidi,requests,geopy,pytz,certifi

# (str) Custom source for any requirement (optional)
# (list) Permissions
android.permissions = INTERNET, ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION

# (int) Target Android API, should be as high as possible.
android.api = 31

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (bool) Use --private data storage (True for most apps)
android.private_storage = True

# (str) Android entry point default is PythonActivity
android.entrypoint = org.kivy.android.PythonActivity

# (list) List of architectures to build for
android.archs = arm64-v8a, armeabi-v7a

# (bool) allow backup
android.allow_backup = True

# (str) Full name of the font for the title
# font.name = arial.ttf

[buildozer]
# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = off, 1 = on)
warn_on_root = 1
