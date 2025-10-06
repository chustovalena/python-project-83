### Hexlet tests and linter status:
[![Actions Status](https://github.com/chustovalena/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/chustovalena/python-project-83/actions)
### Test - Coverage
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=chustovalena_python-project-83&metric=coverage)](https://sonarcloud.io/summary/new_code?id=chustovalena_python-project-83)

# 🌐 Page Analyzer - SEO Анализ

**Зачем нужен SEO Анализ** - Поисковые системы (Google, Яндекс и др.) оценивают сайты по множеству факторов.
Одни из базовых — корректность заголовков, структура и метаинформация страницы. 

**Page Analyzer** — это веб-приложение на **Python3 (Flask)**, которое позволяет проводить базовый **SEO-анализ сайтов**.  
Сервис принимает URL, проверяет его доступность и извлекает основные SEO и тхнические данные страницы: **status code**, **title**, **h1** и **meta description**.

Эти данные — основа для оценки качества сайта и его продвижения в поиске.


Приложение развёрнуто на **Render** и доступно по ссылке:  
🔗 [Application Deploy](https://python-project-83-o8lp.onrender.com)

---

## ✅  Возможности

- Форма для ввода URL на главной странице  
- Проверка валидности введённого адреса и его нормализация  
- Отправка HTTP-запроса и получение ответа с сайта  
- Извлечение SEO-данных:
  - Статус-код ответа (`status code`)
  - Заголовок страницы (`<title>`)
  - Главный заголовок (`<h1>`)
  - Мета-описание (`<meta name="description">`)
- Сохранение всех добавленных уникальных сайтов в базу данных
- Возможность повторной проверки сайта
- Отображение истории проверок
- Интерфейс на **Bootstrap**

---

## ⚙️ Технологии

- **Python 3.13+**
- **Flask** — веб-фреймворк  
- **Requests** — HTTP-запросы  
- **BeautifulSoup4 + lxml** — парсинг HTML  
- **PostgreSQL** — база данных  
- **Jinja2** — шаблоны  
- **Bootstrap** — оформление интерфейса  
- **python-dotenv** — конфигурация окружения  
- **pytest / pytest-cov / ruff** — тестирование и линтинг  
- **gunicorn** — продакшен-сервер  
- **uv** — управление зависимостями и средой
