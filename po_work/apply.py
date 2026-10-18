#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Apply translations from po_work dictionary files into adifier-ru_RU.po."""
import glob, re, sys

PO = '/workspace/adifier-ru_RU.po'
WORK = '/workspace/po_work'

def unesc(s):
    out = []
    i = 0
    while i < len(s):
        c = s[i]
        if c == '\\' and i + 1 < len(s):
            n = s[i+1]
            if n == 'n': out.append('\n')
            elif n == 't': out.append('\t')
            elif n == 'r': out.append('\r')
            elif n == '"': out.append('"')
            elif n == '\\': out.append('\\')
            else: out.append(c); out.append(n)
            i += 2
        else:
            out.append(c); i += 1
    return ''.join(out)

def joinstr(ml):
    out = []
    for l in ml:
        l = l.strip()
        if l.startswith('"') and l.endswith('"'):
            out.append(l[1:-1])
    return unesc(''.join(out))

# ---------- load dictionary ----------
dic = {}
files = sorted(glob.glob(WORK + '/trans*.txt')) + [WORK + '/part1.tsv', WORK + '/t.tsv']
for f in files:
    for line in open(f, encoding='utf-8').read().split('\n'):
        if not line.strip():
            continue
        parts = line.split('\t')
        if len(parts) >= 2:
            en = parts[0].rstrip()
            ru = ' '.join(p.strip() for p in parts[1:] if p.strip()).strip()
        else:
            m = re.search(r'[а-яА-ЯёЁ]', line)
            if not m:
                continue
            en = line[:m.start()].rstrip()
            ru = line[m.start():].strip()
        if en and ru and en not in dic:
            dic[en] = ru

# ---------- manual additions (missing keys) ----------
manual = {
 'All ': 'Все',
 'Edit ': 'Изменить',
 'View ': 'Просмотр',
 'Update ': 'Обновить',
 'Add New ': 'Добавить новое',
 'New ': 'Новое',
 'Parent ': 'Родительская',
 'Search ': 'Поиск',
 'Popular ': 'Популярные',
 'Separate ': 'Разделять',
 'Add or remove ': 'Добавляйте или удаляйте',
 'Choose from the most used ': 'Выбирайте из наиболее используемых',
 'No ': 'Нет',
 ' - Reported by ': ' — сообщение о нарушении от',
 'Name: ': 'Имя:',
 'Email: ': 'Эл. почта:',
 'Message: ': 'Сообщение:',
 'I agree to %s ': 'Я принимаю %s',
 'Search by tag: ': 'Поиск по метке:',
 'Search results for: ': 'Результаты поиска:',
 'Share on ': 'Поделиться в',
 'There is a new ad update waiting for your review ': 'Новое обновление объявления ожидает вашего рассмотрения',
 'There is a new ad waiting for your review ': 'Новое объявление ожидает вашего рассмотрения',
 '<b>%d</b> day': '<b>%d</b> день',
 '<b>%d</b> days': '<b>%d</b> дня / <b>%d</b> дней',
 '[Ad Reported] - ': '[Жалоба на объявление] — ',
 'Phone number is changed, you need to verify it in order to be displayed. Click %s': 'Номер телефона изменён, его нужно подтвердить, чтобы он отображался. Нажмите %s',
 'Account is created, check your mail. To resend activation email submit form again.': 'Учётная запись создана, проверьте почту. Чтобы повторно отправить письмо для активации, отправьте форму ещё раз.',
 'Question about: ': 'Вопрос о:',
 'You can reply directly to this email to respond to ': 'Вы можете ответить прямо на это письмо, чтобы ответить пользователю',
 'https://www.facebook.com/...': 'https://www.facebook.com/...',
 'https://twitter.com/...': 'https://twitter.com/...',
 'https://www.youtube.com/channel/...': 'https://www.youtube.com/channel/...',
 'https://linkedin.com/in/...': 'https://linkedin.com/in/...',
 'https://www.instagram.com/...': 'https://www.instagram.com/...',
 'By ': 'Автор: ',
 '%s review': '%s отзыв',
 '%s reviews': '%s отзыва / %s отзывов',
 'Package: ': 'Пакет:',
 'Subscription: ': 'Подписка:',
 'Product: ': 'Товар:',
 'Total ': 'Всего',
 'Tax ID:': 'ИНН:',
 'Promotion: ': 'Продвижение:',
 'Invoice - ': 'Счёт — ',
 '%s day': '%s день',
 '%s days': '%s дня / %s дней',
 'Input how many hours user will be blocked from login ( Default is 3 hours )': 'Укажите, сколько часов пользователь будет заблокирован для входа (по умолчанию 3 часа)',
 'Only numbers and letters and - and _. Must not contain any spaces. After the change you must go to Settings -> Permalinks and click Save': 'Только цифры, буквы, дефис и нижнее подчёркивание, без пробелов. После изменения перейдите в «Настройки» -> «Постоянные ссылки» и нажмите «Сохранить»',
 'Control image sizes. After the changes you must regenerate thumbnails. Regenerate Thumbnails plugin will help you with this. More on function which is being used https://developer.wordpress.org/reference/functions/add_image_size/': 'Управление размерами изображений. После изменений нужно перегенерировать миниатюры — поможет плагин Regenerate Thumbnails. Подробнее о используемой функции: https://developer.wordpress.org/reference/functions/add_image_size/',
 'Register your application on https://console.developers.google.com/project': 'Зарегистрируйте своё приложение на https://console.developers.google.com/project',
 'Select which ad types are alowed to be submitted. If none is selected all will be available': 'Выберите, какие типы объявлений разрешено подавать. Если ничего не выбрано, будут доступны все',
 'Enable or disable account type field ( EU requirements is to have this enabled )': 'Включить или отключить поле типа учётной записи (согласно требованиям ЕС оно должно быть включено)',
 'Input how many top ads places are available or leave empty for unlimited': 'Укажите, сколько мест доступно для топ-объявлений, или оставьте пустым для неограниченного количества',
 'Input number of hom many similar ads to display on ad single page or leave empty to disable': 'Укажите количество похожих объявлений для отображения на странице объявления или оставьте пустым, чтобы отключить',
 'Input map style array which you can find on sites like https://snazzymaps.com/ for Google Map or link of style found here https://www.mapbox.com/designer-maps/ for mapbox': 'Введите массив стиля карты (можно найти на сайтах вроде https://snazzymaps.com/ для Google Maps) или ссылку на стиль для Mapbox: https://www.mapbox.com/designer-maps/',
 'Input map language code, https://developers.google.com/maps/faq#languagesupport': 'Введите код языка карты: https://developers.google.com/maps/faq#languagesupport',
 'Input map language code, https://docs.mapbox.com/vector-tiles/reference/mapbox-streets-v8/#name-text--name_lang-code-text': 'Введите код языка карты: https://docs.mapbox.com/vector-tiles/reference/mapbox-streets-v8/#name-text--name_lang-code-text',
 'Input geocoder language code ( autocomplete box for place select ), http://www.mathguide.de/info/tools/languagecode.html': 'Введите код языка геокодера (поле автодополнения для выбора места): http://www.mathguide.de/info/tools/languagecode.html',
 'Select default sorting on search listing. Leave empty ( click on X ) to sort by default ( date )': 'Выберите сортировку по умолчанию в результатах поиска. Оставьте пустым (нажмите X), чтобы сортировать по умолчанию (по дате)',
 'Input number if you want to limit list of category and predefined locations on search page or leave empty to show them all': 'Укажите число, если хотите ограничить список категорий и предопределённых местоположений на странице поиска, или оставьте пустым, чтобы показать все',
 'If this is set to yes then users will be able to send mail to seller while they are loggedout and at the same time they will be able to register.': 'Если выбрано «да», пользователи смогут писать продавцу без входа в систему, а также смогут зарегистрироваться.',
 'Input number if you want to show some other author ads on ad single page ( it will dispay them random ) or leave empty to disable': 'Укажите число, если хотите показывать другие объявления автора на странице объявления (отображаются в случайном порядке), или оставьте пустым, чтобы отключить',
 'Select style of the price filter on search page which can be draggable slider or two inputs for min and max': 'Выберите стиль фильтра цены на странице поиска: перетаскиваемый ползунок или два поля для минимума и максимума',
 'Enable or disable ability for users to delete their account and all what they have posted': 'Включить или отключить возможность удаления пользователями своей учётной записи и всех их публикаций',
 'If set to yes order associated to account which is being deleted will be kept': 'Если выбрано «да», заказы удаляемой учётной записи будут сохранены',
 'Combined - show all categories in single select box ( search will display radio button list ) Separated - load subcategories based on selected category ( search will display multiple select boxes. Search form element will display only top level categories )': 'Объединённый — показывать все категории в одном выпадающем списке (в поиске — список переключателей). Раздельный — загружать подкатегории в зависимости от выбранной категории (в поиске — несколько выпадающих списков; элемент формы поиска показывает только категории верхнего уровня)',
 'Select to display username instead for dispaly name ( First Name + Last Name )': 'Выберите, чтобы отображать имя пользователя вместо отображаемого имени (имя + фамилия)',
 'Enable or disable redirect to author list of ads after ad has been submitted': 'Включить или отключить перенаправление к списку объявлений автора после подачи объявления',
 'Select whether you want to use map places or dropdown with predefined values for location search. If you set this option to Geo Search then make sure you have set Use Map Locations to Yes': 'Выберите, использовать ли места на карте или выпадающий список с предопределёнными значениями для поиска по местоположению. Если выбран режим геопоиска, установите «Использовать местоположения на карте» в значение «Да»',
 'If this is set to No then map will not be displayed at all ( ad single, profile,... )': 'Если выбрано «Нет», карта не будет отображаться нигде (страница объявления, профиль и т.д.)',
 'If this is set to No then users will not be forced to select predefined location from the dropdown': 'Если выбрано «Нет», пользователям не придётся выбирать предопределённое местоположение из выпадающего списка',
 'Combined - show all predefined locations in single select box ( search will display radio button list ) Separated - load sublocations based on selected location ( search will display multiple select boxes. Search form element will display only top level locations )': 'Объединённый — показывать все предопределённые местоположения в одном выпадающем списке (в поиске — список переключателей). Раздельный — загружать подобласти в зависимости от выбранного местоположения (в поиске — несколько выпадающих списков; элемент формы поиска показывает только местоположения верхнего уровня)',
 'What location to display on ad single? Geo Location means to display values from map and Predefined means to display from dropdown': 'Какое местоположение отображать на странице объявления? «Гео» — значения с карты, «Предопределённое» — значения из выпадающего списка',
 'What location to display on profile? Geo Location means to display values from map and Predefined means to display from dropdown': 'Какое местоположение отображать в профиле? «Гео» — значения с карты, «Предопределённое» — значения из выпадающего списка',
 'Input country code or comma separated list of country codes in which locations will be available': 'Введите код страны или список кодов стран через запятую, в которых будут доступны местоположения',
 'Input pie separated list of bad words which will be removed for example ( word|another|another one )': 'Введите список запрещённых слов, разделённых символом |, которые будут удаляться, например (word|another|another one)',
 'Input maximum chars that can be added in title field or leave empty for unlimited': 'Укажите максимальное число символов в поле заголовка или оставьте пустым для неограниченного количества',
 'If this option is checked then slug of the advert will be changed if the title is changed': 'Если этот флажок установлен, ярлык (URL) объявления будет меняться при изменении заголовка',
 'Abbreviation is 3 letters code ( i.e. USD ). Sign is representative sign of the currency. Rate is value which represents amount of base currency ( currency set in Adifier WP -> Payments ) which is equal to amount of 1 of given currency (i.e. based currency is USD and 1 EUR = 1.4 USD rate value for EUR is 1.4 ). Even if you are not using decimals populate decimal separator ( in this case you can put anything )': 'Аббревиатура — трёхбуквенный код (например, USD). Знак — символ валюты. Курс — количество базовой валюты (заданной в Adifier WP -> Платежи), равное 1 единице данной валюты (например, базовая валюта USD и 1 EUR = 1.4 USD, тогда курс для EUR равен 1.4). Даже если десятичные дроби не используются, заполните десятичный разделитель (в этом случае можно указать что угодно)',
 'Input your Twilio Service SID. To create new service visit this link https://www.twilio.com/console/verify/dashboard': 'Введите SID сервиса Twilio. Чтобы создать новый сервис, откройте https://www.twilio.com/console/verify/dashboard',
 'Input your Twilio Account SID. This info can be found here https://www.twilio.com/console/project/settings': 'Введите SID учётной записи Twilio. Эти данные доступны здесь: https://www.twilio.com/console/project/settings',
 'Input your Twilio Auth Token. This info can be found here https://www.twilio.com/console/project/settings': 'Введите авторизационный токен Twilio. Эти данные доступны здесь: https://www.twilio.com/console/project/settings',
 'Input sender mail which will be used by system mails like registration, password recovery...': 'Укажите адрес отправителя для системных писем: регистрация, восстановление пароля и т.д.',
 'Input sender name which will be used by system mails like registration, password recovery...': 'Укажите имя отправителя для системных писем: регистрация, восстановление пароля и т.д.',
 'If your main logo is SVG you need to add png/jpg logo here since SVG logo is not supported in emails or you can use it anyway': 'Если основной логотип — SVG, добавьте сюда логотип png/jpg, так как SVG не поддерживается в письмах, но можно использовать и его',
 'Free time for posting ads upon registration. If you are inputing days input clean number only ( For example 20 ). If you are inputing hours input it with prefix + ( For example +14 )': 'Бесплатное время для подачи объявлений после регистрации. Для дней укажите просто число (например, 20). Для часов — с префиксом + (например, +14)',
 'Input free ads and free time which users will receive upon registration. If you are inputing days input clean number only ( For example 20 ). If you are inputing hours input it with prefix + ( For example +14 )': 'Укажите количество бесплатных объявлений и бесплатное время, которые пользователи получают при регистрации. Для дней укажите просто число (например, 20). Для часов — с префиксом + (например, +14)',
 'Create packages for posting ads. Packages contain number of ads which user can post. Decimal separator is . ( dot ) no thousands separator. Price can not be 0 since packages are cumulative': 'Создайте пакеты для подачи объявлений. Пакет содержит количество объявлений, которые может разместить пользователь. Десятичный разделитель — точка, разделитель тысяч не используется. Цена не может быть 0, так как пакеты накапливаются',
 'Create subscriptions for posting ads. Subscription contain number of days for how long user can post ad. Decimal separator is . ( dot ) no thousands separator. Price can not be 0 since packages are cumulative': 'Создайте подписки для подачи объявлений. Подписка содержит количество дней, в течение которых пользователь может размещать объявления. Десятичный разделитель — точка, разделитель тысяч не используется. Цена не может быть 0, так как пакеты накапливаются',
 'Create hybrids for posting ads. Hybrid contain number of ads and number of days for how long user can post ad. Decimal separator is . ( dot ) no thousands separator. Price can not be 0 since packages are cumulative': 'Создайте гибридные предложения для подачи объявлений. Гибрид содержит количество объявлений и количество дней, в течение которых пользователь может размещать объявления. Десятичный разделитель — точка, разделитель тысяч не используется. Цена не может быть 0, так как пакеты накапливаются',
 'If you want to test out payment with sandbox accounts select Test and if you want to start receiving payments select Live': 'Для проверки оплаты с песочными аккаунтами выберите тестовый режим, для приёма реальных платежей — рабочий',
 'Input number which will increment with every order. Empty means that it continues to use timestamp': 'Укажите число, которое будет увеличиваться с каждым заказом. Пустое значение означает продолжение использования отметки времени',
 'Input string to be displayed before the incremental number or leave empty to remove': 'Введите текст, отображаемый перед возрастающим номером, или оставьте пустым, чтобы убрать',
 'Input string to be displayed after the incremental number or leave empty to remove': 'Введите текст, отображаемый после возрастающего номера, или оставьте пустым, чтобы убрать',
 'If you are required to have sequential numbers on all paid invoices enable this option. It will add temporary number on each order and apply proper sequential number only when the order is paid.': 'Если требуется сквозная нумерация всех оплаченных счетов, включите эту опцию. Каждому заказу присваивается временный номер, а правильный порядковый номер применяется только после оплаты.',
 'Set up reCaptcha v3 API. Visit https://www.google.com/recaptcha/admin/create': 'Настройте API reCaptcha v3. Перейдите на https://www.google.com/recaptcha/admin/create',
 'If it is set to yes then user will first receive confirmation mail in order to give their consent.': 'Если выбрано «да», пользователь сначала получит письмо для подтверждения согласия.',
 'Upload logo which is used on light  background headers. Used by Inline Navigation, Bottom Navigation, Transaprent Navigation ( on inner pages ), Side Categories': 'Загрузите логотип для шапок со светлым фоном. Используется в навигации: встроенной, нижней, прозрачной (на внутренних страницах), боковых категориях',
 'Upload logo which is used on dark background headers. Used by Inline Navigation, Bottom Navigation ( if sticky is enabled ), Transaprent Navigation ( on home page ), Side Categories ( if sticky is enabled ), Full Dark': 'Загрузите логотип для шапок с тёмным фоном. Используется в навигации: встроенной, нижней (если закреплена), прозрачной (на главной), боковых категориях (если закреплены), Fully Dark',
 'Select font color for the elements which have main color as their background.': 'Выберите цвет шрифта для элементов с основным цветом фона.',
 'Select style of the header submit button - full with text or bullhorn icon only': 'Выберите стиль кнопки подачи объявления в шапке: полная с текстом или только иконка рупора',
 'Select font weight for the regular text. Check out available weights on https://fonts.google.com/': 'Выберите насыщенность шрифта обычного текста. Доступные значения: https://fonts.google.com/',
 'Select font weight for the titles. Check out available weights on https://fonts.google.com/': 'Выберите насыщенность шрифта заголовков. Доступные значения: https://fonts.google.com/',
 'Select background color for the icon of contact seler by phone call to action.': 'Выберите цвет фона значка призыва связаться с продавцом по телефону.',
 'Select background color for the icon of contact seller by message call to action.': 'Выберите цвет фона значка призыва написать продавцу в сообщения.',
 'Select background color for the contact seller by message call to action.': 'Выберите цвет фона блока призыва написать продавцу в сообщения.',
 'Input comma separated list of ad category IDs from whcih to show the posts': 'Введите список ID категорий объявлений через запятую, из которых показывать записи',
 'Input comma separated list of ad location IDs from whcih to show the posts': 'Введите список ID местоположений объявлений через запятую, из которых показывать записи',
 'ad': 'объявление',
 'Select on which categories to show fields from this group. Fields are show only on displayed category so selecting only parent will not show fields on it\'s children': 'Выберите категории, в которых показывать поля этой группы. Поля отображаются только в выбранной категории, поэтому выбор только родительской не покажет поля в дочерних',
 'Unique slug/reference for the custom field; must be no more than 28 characters.': 'Уникальный ярлык (URL) для произвольного поля; не более 28 символов.',
 'If field is fixed then users can select only among created values and will not be able to add their own': 'Если поле фиксированное, пользователи могут выбирать только из созданных значений и не смогут добавлять свои',
 'Determines the sort order of the terms on the frontend shop. With None you can use some plugin for custom term ordering': 'Определяет порядок сортировки терминов на витрине. При выборе «Нет» можно использовать плагин для произвольной сортировки',
 'Slug "%s" is not allowed because it is a reserved term. Change it, please.': 'Ярлык (URL) «%s» запрещён, так как это зарезервированный термин. Пожалуйста, измените его.',
 'Your advert %s has expired but you can renew it by clicking on the button below': 'Срок действия вашего объявления %s истёк, но вы можете продлить его, нажав кнопку ниже',
 'You\'ve just bought %s at auction by placing the highest bid. Please allow up to 24h for the seller to contact you': 'Вы купили %s на аукционе, сделав наивысшую ставку. Продавец свяжется с вами в течение 24 часов',
 'Buyer %s has offered highest bid on your auction %s, go to your ad by clicking button below and contact buyer in the next 24h': 'Покупатель %s сделал наивысшую ставку на вашем аукционе %s. Перейдите к объявлению, нажав кнопку ниже, и свяжитесь с покупателем в течение 24 часов',
 'Hello %s. You\'ve just been outbid on auction %s. Click below to bid again.': 'Здравствуйте, %s! Вашу ставку на аукционе %s перебили. Нажмите кнопку ниже, чтобы сделать новую ставку.',
 'Someone requested password recovery for your account (username: %s). If you have not done this then ignore this mail.': 'Кто-то запросил восстановление пароля для вашей учётной записи (имя пользователя: %s). Если это были не вы, проигнорируйте это письмо.',
 'You have changed your email address, however in order for changes to take effect you need to confirm your new email address by clicking on the button below': 'Вы изменили адрес эл. почты. Чтобы изменения вступили в силу, подтвердите новый адрес, нажав кнопку ниже',
 'Make your payment in amount of %s directly into our bank account. Please use %s as the payment reference. Your order won’t be processed until the funds have cleared in our account.': 'Выполните платёж на сумму %s напрямую на наш банковский счёт. В качестве назначения платежа укажите %s. Заказ будет обработан только после поступления средств на наш счёт.',
 'Your payment is being processed and once it is approved you will receive purchased goods': 'Ваш платёж обрабатывается. После его одобрения вы получите purchased товары'.replace('purchased ',''),
 'Instructions for user on how to pay. To place order ID use %order to place price use %price': 'Инструкции для пользователя о том, как оплатить. Для ID заказа используйте %order, для цены — %price',
 'Input your Paystack secret key. Make sure taht you input test key here if you want to test gateway first': 'Введите секретный ключ Paystack. Если вы сначала хотите протестировать платёжный шлюз, убедитесь, что указали тестовый ключ',
 'Input your Paystack public key. Make sure taht you input test key here if you want to test gateway first': 'Введите публичный ключ Paystack. Если вы сначала хотите протестировать платёжный шлюз, убедитесь, что указали тестовый ключ',
 'Transaction was not successful: Last gateway response was:': 'Платёж не выполнен. Последний ответ платёжного шлюза:',
 'Something went wrong while trying to convert the request variable to json. Uncomment the print_r command to see what is in the result variable': 'Не удалось преобразовать переменную запроса в JSON. Раскомментируйте команду print_r, чтобы увидеть содержимое переменной результата',
 'Showing': 'Показано',
 'ad posted': 'объявление подано',
 'ads posted': 'объявления поданы',
 'In:': 'В:',
 'If you want to show ads in two rows on each slide set this option to Yes': 'Чтобы показывать объявления в два ряда на каждом слайде, установите эту опцию в значение «Да»',
 'If you want to show items in two rows on each slide set this option to Yes': 'Чтобы показывать элементы в два ряда на каждом слайде, установите эту опцию в значение «Да»',
 'If you want to make icon smaller you can place here max width. For example 40px': 'Если нужно уменьшить значок, укажите здесь максимальную ширину, например 40px',
 'If you want to change font size of category name input it here. For example 13px': 'Если нужно изменить размер шрифта названия категории, укажите его здесь, например 13px',
 'If you want to change font size of category count input it here. For example 13px': 'Если нужно изменить размер шрифта счётчика категории, укажите его здесь, например 13px',
 'If you want to adjust bottom marginof the icon input it here. For example 25px': 'Если нужно настроить нижний отступ значка, укажите его здесь, например 25px',
 'Select which blogs to show or leave empty and input number of latest to show in field below': 'Выберите блоги для отображения или оставьте пустым и укажите количество последних записей в поле ниже',
 'If you want to show posts in two rows on each slide set this option to Yes': 'Чтобы показывать записи в два ряда на каждом слайде, установите эту опцию в значение «Да»',
 'Select which package /subscription to show': 'Выберите пакет или подписку для отображения',
 'Input title text. If you want to have some words colored use span like this <span style="color: #fff">TEXT</span> for bold use b tag <b>TEXT</b>': 'Введите текст заголовка. Чтобы покрасить отдельные слова, используйте span, например <span style="color: #fff">ТЕКСТ</span>; для жирного — тег <b>ТЕКСТ</b>',
 'Input subtitle text. If you want to have some words colored use span like this <span style="color: #fff">TEXT</span> for bold use b tag <b>TEXT</b>': 'Введите текст подзаголовка. Чтобы покрасить отдельные слова, используйте span, например <span style="color: #fff">ТЕКСТ</span>; для жирного — тег <b>ТЕКСТ</b>',
 "If this is enabled and you have multiple texts for example 'We Are Number One' 'We Are Awesome' script will recognize We Are and will type only text after it otherwise it will type it all": "Если это включено и задано несколько текстов, например «We Are Number One» и «We Are Awesome», скрипт распознает общее начало «We Are» и будет допечатывать только остальную часть; иначе печатается весь текст целиком",
 'Select image representative for category or leave empty to use associated one': 'Выберите изображение для категории или оставьте пустым, чтобы использовать связанное',
 'Min bid:': 'Мин. ставка:',
 'KingComposer is also supported but we are strongly encourage you to move to Elementor.': 'KingComposer тоже поддерживается, но мы настоятельно рекомендуем перейти на Elementor.',
 'Once you install & activate, Elementor Appearance -> Import Demo Content will allow you to import demo content for Elementor': 'После установки и активации Elementor в разделе «Внешний вид» -> «Импорт демо-контента» вы сможете импортировать демо-контент для Elementor',
 'Reinstall Smeta plugin ( Delete it and theme will offer you to install it again )': 'Переустановите плагин Smeta (удалите его, и тема предложит установить заново)',
 'Reinstall Adifier System plugin ( Delete it and theme will offer you to install it again )': 'Переустановите плагин Adifier System (удалите его, и тема предложит установить заново)',
 'Reinstall Adifier Import plugin ( Delete it and theme will offer you to install it again )': 'Переустановите плагин Adifier Import (удалите его, и тема предложит установить заново)',
 'Theme recommends to install OMGF plugin to load fonts in GDPR compilant way. Plugins -> Add New, search form OMGF, install & activate': 'Тема рекомендует установить плагин OMGF для загрузки шрифтов в соответствии с требованиями GDPR. «Плагины» -> «Добавить новый», найдите OMGF, установите и активируйте',
 'Theme supports following plugins to load 3rd party scripts (such as maps, search by location, etc...) in GDPR compliant way: Complianz | CookieYes | GDPR Cookie Compliance | Cookie Notice & Compliance for GDPR / CCPA | Borlabs Cookie. Go to Plugins -> Add New to install plugin and also read Adifier documentation section GDPR': 'Тема поддерживает следующие плагины для загрузки сторонних скриптов (карты, поиск по местоположению и т.д.) в соответствии с требованиями GDPR: Complianz | CookieYes | GDPR Cookie Compliance | Cookie Notice & Compliance for GDPR / CCPA | Borlabs Cookie. Перейдите в «Плагины» -> «Добавить новый», чтобы установить плагин, и прочитайте раздел документации Adifier о GDPR',
 'Custom Sidebar': 'Произвольный сайдбар',
 'Please use the fallback form below to upload your files like in the olden days.': 'Используйте резервную форму ниже, чтобы загрузить файлы по старинке.',
 'The following plugins were activated successfully:': 'Следующие плагины успешно активированы:',
 'Plugin not activated. A higher version of %s is needed for this theme. Please update the plugin.': 'Плагин не активирован. Для этой темы требуется более новая версия %s. Обновите плагин.',
 'There are one or more required or recommended plugins to install, update or activate.': 'Есть необходимые или рекомендуемые плагины, которые нужно установить, обновить или активировать.',
 'The remote plugin package does not contain a folder with the desired slug and renaming did not work.': 'Удалённый пакет плагина не содержит папки с нужным ярлыком (slug), и переименование не удалось.',
 'Please contact the plugin provider and ask them to package their plugin according to the WordPress guidelines.': 'Свяжитесь с разработчиком плагина и попросите упаковать плагин согласно рекомендациям WordPress.',
 'The remote plugin package consists of more than one file, but the files are not packaged in a folder.': 'Удалённый пакет плагина состоит из нескольких файлов, но они не помещены в папку.',
 'To Install <span class="count">(%s)</span>': 'Для установки <span class="count">(%s)</span>',
 'Update Available <span class="count">(%s)</span>': 'Доступно обновление <span class="count">(%s)</span>',
 'To Activate <span class="count">(%s)</span>': 'Для активации <span class="count">(%s)</span>',
 'The installation and activation process is starting. This process may take a while on some hosts, so please be patient.': 'Начинаются установка и активация. На некоторых хостах это может занять время, пожалуйста, подождите.',
 '%1$s installed and activated successfully.': '%1$s успешно установлен и активирован.',
 'The installation process is starting. This process may take a while on some hosts, so please be patient.': 'Начинается установка. На некоторых хостах это может занять время, пожалуйста, подождите.',
}
dic.update({k: v for k, v in manual.items() if k not in dic})

# plural handling: entries with msgid_plural need forms keyed "<singular>\x00<plural>"
# build secondary dict: try to detect plural pairs already present in dic via common patterns
# We'll handle plurals explicitly below with a table.
plural_forms = {
 ('%d day', '%d days'): ('%d день', '%d дня', '%d дней'),
 ('%s day', '%s days'): ('%s день', '%s дня', '%s дней'),
 ('<b>%d</b> day', '<b>%d</b> days'): ('<b>%d</b> день', '<b>%d</b> дня', '<b>%d</b> дней'),
 ('%s review', '%s reviews'): ('%s отзыв', '%s отзыва', '%s отзывов'),
 ('ad posted', 'ads posted'): ('объявление подано', 'объявления поданы', 'объявлений подано'),
 ('ad', 'ads'): ('объявление', 'объявления', 'объявлений'),
 ('The following plugin was activated successfully:', 'The following plugins were activated successfully:'):
    ('Следующий плагин успешно активирован:', 'Следующих плагина успешно активировано:', 'Следующих плагинов успешно активировано:'),
 ('To Install <span class="count">(%s)</span>', 'To Install <span class="count">(%s)</span>'):
    ('Для установки <span class="count">(%s)</span>', 'Для установки <span class="count">(%s)</span>', 'Для установки <span class="count">(%s)</span>'),
 ('Update Available <span class="count">(%s)</span>', 'Update Available <span class="count">(%s)</span>'):
    ('Доступно обновление <span class="count">(%s)</span>', 'Доступно обновления <span class="count">(%s)</span>', 'Доступно обновлений <span class="count">(%s)</span>'),
 ('To Activate <span class="count">(%s)</span>', 'To Activate <span class="count">(%s)</span>'):
    ('Для активации <span class="count">(%s)</span>', 'Для активации <span class="count">(%s)</span>', 'Для активации <span class="count">(%s)</span>'),
}

extra_manual = {
 ' at ': ' в ',
 'Custom Sidebar ': 'Произвольный сайдбар',
 'Free time for posting ads upon registration. If you are inputing days input clean number only ( For example 20 ). If you are inputing hours input it with prefix + ( For example +14 ) ':
   'Бесплатное время для подачи объявлений после регистрации. Для дней укажите просто число (например, 20). Для часов — с префиксом + (например, +14) ',
 'Input free ads and free time which users will receive upon registration. If you are inputing days input clean number only ( For example 20 ). If you are inputing hours input it with prefix + ( For example +14 ) ':
   'Укажите количество бесплатных объявлений и бесплатное время, которые пользователи получают при регистрации. Для дней укажите просто число (например, 20). Для часов — с префиксом + (например, +14) ',
 'If type is Nested Values make sure that name of the field is in form LEVEL1|LEVEL2.. ( for example Make|Model - divider is pipe not backslash or forwardslash ). If type of field is Single Value Numeric you can add prefix or sufix like this [prefix]  (sufix) for example Mileage (km)':
   'Если тип — «Вложенные значения», имя поля должно быть в формате УРОВЕНЬ1|УРОВЕНЬ2 (например, Марка|Модель; разделитель — вертикальная черта, а не обратная или прямая косая черта). Если тип поля — «Одиночное числовое значение», можно добавить префикс или суффикс так: [префикс] (суффикс), например Пробег (км)',
 'If type is Nested Values make sure that name of the field is in form LEVEL1|LEVEL2.. ( for example Make|Model - divider is pipe not backslash or forwardslash ). If type of field is Single Value Numeric you can add prefix or sufix like this [prefix]  (sufix) for example Mileage (km).':
   'Если тип — «Вложенные значения», имя поля должно быть в формате УРОВЕНЬ1|УРОВЕНЬ2 (например, Марка|Модель; разделитель — вертикальная черта, а не обратная или прямая косая черта). Если тип поля — «Одиночное числовое значение», можно добавить префикс или суффикс так: [префикс] (суффикс), например Пробег (км).',
 'In: ': 'В:',
 'Min bid: ': 'Мин. ставка:',
 'Select which package /subscription to show ': 'Выберите пакет или подписку для отображения',
 'Showing ': 'Показано',
 'Tax ID: ': 'ИНН:',
 'Transaction was not successful: Last gateway response was: ': 'Платёж не выполнен. Последний ответ платёжного шлюза: ',
}
dic.update(extra_manual)

def get_ru(mid, mpl=None):
    if mpl is not None:
        key = (mid, mpl)
        if key in plural_forms and plural_forms[key]:
            return plural_forms[key]
    if mid in dic:
        return dic[mid]
    return None

# ---------- rewrite PO ----------
with open(PO, encoding='utf-8') as f:
    content = f.read()
lines = content.split('\n')
blocks, cur, block_starts = [], [], []
start = 0
for idx, ln in enumerate(lines):
    if ln.strip() == '':
        blocks.append((start, idx, cur)); block_starts.append(start)
        cur = []; start = idx + 1
    else:
        cur.append(ln)
if cur:
    blocks.append((start, len(lines), cur))

def esc(s):
    return s.replace('\\', '\\\\').replace('"', '\\"')

def wrap_po(text, prefix):
    """Return list of lines for msgstr/msgid value with escaping, splitting on \n like gettext."""
    # split into segments ending with \n to mimic standard formatting
    parts = []
    seg = ''
    i = 0
    while i < len(text):
        if text[i] == '\n':
            parts.append(seg + '\n'); seg = ''
        else:
            seg += text[i]
        i += 1
    if seg:
        parts.append(seg)
    if not parts:
        parts = ['']
    out = []
    for pi, p in enumerate(parts):
        val = esc(p)
        if pi == 0:
            out.append(prefix + ' "' + val + '"' + ('' if len(parts) > 1 else ''))
        else:
            out.append('"' + val + '"')
    if len(parts) == 1:
        pass
    return out

new_lines = []
unfilled = []
first = True
for (s, e, b) in blocks:
    mid = mpl = None
    j = 0
    msgstr_positions = {}
    while j < len(b):
        l = b[j]
        if l.startswith('msgid ') and not l.startswith('msgid_plural'):
            ml = [l[6:]]; k = j + 1
            while k < len(b) and b[k].startswith('"'):
                ml.append(b[k]); k += 1
            mid = joinstr(ml); j = k; continue
        if l.startswith('msgid_plural '):
            ml = [l[13:]]; k = j + 1
            while k < len(b) and b[k].startswith('"'):
                ml.append(b[k]); k += 1
            mpl = joinstr(ml); j = k; continue
        if l.startswith('msgstr[') or l.startswith('msgstr '):
            mm = re.match(r'msgstr(?:\[(\d+)\])?\s*', l)
            idx = int(mm.group(1)) if mm.group(1) is not None else 0
            ml = [l[len(mm.group(0)):]]; k = j + 1
            while k < len(b) and b[k].startswith('"'):
                ml.append(b[k]); k += 1
            msgstr_positions[idx] = (j, k, joinstr(ml))
            j = k; continue
        j += 1

    if first:
        # header block: keep as-is
        new_lines.extend(b)
        new_lines.append('')
        first = False
        continue

    trans = get_ru(mid, mpl)
    rebuild = {}
    if isinstance(trans, tuple):
        for fi, ft in enumerate(trans):
            rebuild[fi] = ft
    elif trans is not None:
        rebuild[0] = trans
    # if existing msgstr non-empty, do not overwrite (rule: don't touch translated)
    final_map = {}
    for idx, (js, je, oldval) in msgstr_positions.items():
        if oldval != '':
            final_map[idx] = None  # keep original raw lines
        elif idx in rebuild:
            final_map[idx] = rebuild[idx]
        else:
            final_map[idx] = None
            unfilled.append(mid)

    # emit block
    emitted_idx = set()
    j = 0
    while j < len(b):
        l = b[j]
        if l.startswith('msgstr[') or l.startswith('msgstr '):
            mm = re.match(r'msgstr(?:\[(\d+)\])?\s*', l)
            idx = int(mm.group(1)) if mm.group(1) is not None else 0
            js, je, oldval = msgstr_positions[idx]
            if idx in final_map and final_map[idx] is not None:
                prefix = 'msgstr[%d] ' % idx if mm.group(1) is not None else 'msgstr '
                new_lines.extend(wrap_po(final_map[idx], prefix))
            else:
                new_lines.extend(b[js:je])
            emitted_idx.add(idx)
            j = je; continue
        new_lines.append(l)
        j += 1
    # add missing plural indices if entry is plural and had fewer msgstr lines
    if mpl is not None:
        for idx in range(len(msgstr_positions), 3):
            if idx in final_map and final_map[idx] is not None:
                new_lines.extend(wrap_po(final_map[idx], 'msgstr[%d] ' % idx))
    new_lines.append('')

# trim trailing extra blank line duplication at EOF
while len(new_lines) > 1 and new_lines[-1] == '' and new_lines[-2] == '':
    new_lines.pop()

with open(PO, 'w', encoding='utf-8') as f:
    f.write('\n'.join(new_lines))

print('unfilled entries:', len(set(unfilled)))
for u in sorted(set(unfilled))[:50]:
    print('MISS:', repr(u[:90]))
