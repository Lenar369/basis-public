# Базис Android 1.0.1 — исправление запуска

# Базис Android 1.0.1 — исправление запуска

Что изменилось:
# Базис Android 1.0.1 — исправление запуска
Дата: 22 октября 2026 г.

## Результат
Версия 1.0.1 (versionCode 2, package ru.calcul369.bazis) опубликована во внутреннем тестировании Google Play 22.10.2026 в 09:37 МСК. Пользователь обновил приложение через Play Маркет и подтвердил, что всё работает.
ADB подтвердил versionCode=2, versionName=1.0.1, installerPackageName=com.android.vending. На Xiaomi 2109119DG, Android 14/API 34 выполнены пять именно холодных запусков: все COLD, переход в Chrome CustomTabActivity успешен, новых ошибок приложения в crash Logcat нет. Данные приложения не очищались, приложение не удалялось.

## Причина и исправление
Logcat исходной Play-версии: IllegalArgumentException: Component class com.google.androidbrowserhelper.trusted.ManageDataLauncherActivity does not exist in ru.calcul369.bazis.
ABH 2.7.4 LauncherActivity.launchTwa вызывает ManageDataLauncherActivity.addSiteSettingsShortcut, который включает/выключает компонент через PackageManager. Компонент отсутствовал в манифесте.
Добавлено объявление Activity с APPLICATION_PREFERENCES и MANAGE_SPACE_URL. Убран ошибочный autoVerify из MAIN/LAUNCHER-фильтра; у веб-ссылок сохранён. Версия повышена с 1.0/code1 до 1.0.1/code2. Package ID, стартовый URL, зависимости и R8 сохранены. Signed workflow теперь выполняет lintRelease.

## Проверки и происхождение сборки
- Коммиты кода: 5d73292 и 27723ae; исходники подписанной сборки — 27723ae.
- Git diff --check: OK; Android pytest: 6 passed; полный CI pytest: 671 passed.
- Локально bundleRelease, assembleRelease, lintRelease: BUILD SUCCESSFUL; 0 ошибок Lint, 11 прежних предупреждений об иконках.
- Signed workflow: https://github.com/Lenar369/Kalkulytor/actions/runs/39734369035 — success.
- Bundletool validate: OK; в итоговом манифесте правильные package/version и ManageDataLauncherActivity.
- Jarsigner: jar verified; upload SHA-256 BB:91:54:C8:07:8A:65:94:64:AD:0C:0D:AE:B1:10:9D:D4:59:63:CA:E3:DE:61:4D:3A:29:33:73:EA:F5:44:5B.
- Финальный AAB SHA-256: 23cc9ed87e79299b318114990b42697ea6c0a49c05904f12ece48af277cc420d.
- PR: https://github.com/Lenar369/Kalkulytor/pull/105 — готов к ревью; main не изменена.

## Digital Asset Links
Из реально установленного Play APK извлечён сертификат C5:FD:BA:4F:F0:6C:B0:55:2D:8F:2A:0C:51:B8:6B:C7:4B:47:35:02:59:8E:72:A7:45:85:55:F0:68:B1:21:66.
В публичном assetlinks.json был только debug-сертификат. Play-сертификат атомарно добавлен в /var/www/calcul369/.well-known/assetlinks.json с сохранением прежнего. Резервная копия: assetlinks.json.before-play-20261022T070235Z. Health до/после: HTTP 200. CRM, nginx и БД не перезапускались и не менялись.
Публичный JSON и Google statements:list подтверждают оба сертификата. Отдельный assetlinks:check вернул maxAge=3600s без linked=true: этот результат не считается подтверждением полноэкранного режима. После обновления серверного файла полноэкранный режим повторно через ADB не проверялся — телефон отключён. До серверного исправления screenshot показывал адресную строку Chrome; это отдельная проблема от устранённого Java crash.

## Следующий этап
Согласовать/слить PR #105 при подготовке дальнейшего выпуска, учитывая автоматический deploy main. Продолжить подготовку публичной публикации: проверить актуальные требования Console и закрытое тестирование. При необходимости отдельно перепроверить полноэкранный TWA после обновления кэша Chrome.

Для кого: Пользователи БАЗИС.

БАЗИС объединяет рабочие процессы строительных, монтажных и производственных компаний в одной CRM.

Подробнее: https://github.com/Lenar369/Kalkulytor/releases/tag/android-v1.0.1
