[app]
title = الميقاتي الفلكي برو
package.name = meeqat_pro
package.domain = org.hassan_astro
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,se1,json
version = 1.0

# السطر الحاسم لضبط نسخة بايثون ومنع الانهيار
python_version = 3.10

# المكتبات المطلوبة
requirements = python3,kivy==2.2.1,swisseph,arabic-reshaper,python-bidi,requests,geopy,pytz,certifi

android.permissions = INTERNET, ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION
android.api = 31
android.minapi = 21
android.ndk = 25b
android.private_storage = True
android.entrypoint = org.kivy.android.PythonActivity
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 1
