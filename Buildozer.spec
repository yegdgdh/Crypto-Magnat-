[app]
title = Крипто Магнат
package.name = cryptomagnat
package.domain = org.cryptomagnat

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 1.0
requirements = python3,kivy==2.2.1,android

orientation = landscape
fullscreen = 1

android.api = 30
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True
android.permissions = INTERNET
