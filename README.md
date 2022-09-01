## Учебный проект YaMDb.

### Описание проекта ###

По адресу http://127.0.0.1:8000/redoc/ подключена документация API YaMDb. В ней описаны возможные запросы к API и структура ожидаемых ответов. Для каждого запроса указаны уровни прав доступа: пользовательские роли, которым разрешён запрос.

### Техническое описание проекта YaMDb. ###

Проект **YaMDb** собирает отзывы (*Review*) пользователей на произведения (*Titles*).

Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Список категорий (*Category*) может быть расширен администратором.

Произведению может быть присвоен жанр (*Genre*) из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). Новые жанры может создавать только администратор.

Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы (*Review*) и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — *рейтинг* (целое число). На одно произведение пользователь может оставить только один отзыв.

Отзыв может быть прокомментирован (*Сomment*) пользователями.

* **Пользовательские роли**
	* Аноним — может просматривать описания произведений, читать отзывы и комментарии.
	* Аутентифицированный пользователь (user) — может читать всё, как и Аноним, может публиковать отзывы и ставить оценки произведениям (фильмам/книгам/песенкам), может комментировать отзывы; может редактировать и удалять свои отзывы и комментарии, редактировать свои оценки произведений. Эта роль присваивается по умолчанию каждому новому пользователю.
	* Модератор (moderator) — те же права, что и у Аутентифицированного пользователя, плюс право удалять и редактировать любые отзывы и комментарии.
	* Администратор (admin) — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.
	* Суперюзер Django должен всегда обладать правами администратора, пользователя с правами admin. Даже если изменить пользовательскую роль суперюзера — это не лишит его прав администратора. Суперюзер — всегда администратор, но администратор — не обязательно суперюзер.


### Запуск проекта:

Клонировать репозиторий и перейти в него в командной строке:

```bash
git clone https://github.dev/femakc/api_yamdb
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```bash
python -m venv venv
```

Для *nix-систем:
```bash
source venv/bin/activate
```

Для windows-систем:
```bash
source venv/Scripts/activate
```

Установить зависимости из файла requirements.txt:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Выполнить миграции:

```bash
cd api_yamdb
python3 manage.py migrate
```

Создать суперпользователя (для раздачи прав админам):

```bash
python manage.py createsuperuser
```

Запустить проект:

```bash
python manage.py runserver
```
