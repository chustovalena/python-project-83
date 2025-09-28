import logging
import os
import requests
from page_analyzer.services.checks import perform_check
from flask import \
    Flask, \
    render_template, \
    url_for, \
    request, \
    redirect, \
    get_flashed_messages, \
    abort, \
    flash
from page_analyzer.validate import validate
from dotenv import load_dotenv
from repository import UrlRepository
from page_analyzer.log_conf import RequestFormatter, RequestFilter


def create_app(db_url=None):
    app = Flask(__name__)

    formatter = RequestFormatter(
        "%(asctime)s [%(levelname)s] %(remote_addr)s %(method)s %(path)s: %(message)s"
    )
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    handler.addFilter(RequestFilter())
    app.logger.setLevel(logging.INFO)
    app.logger.addHandler(handler)

    load_dotenv()
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['DATABASE_URL'] = db_url or os.getenv('DATABASE_URL')
    app.debug = True

    repo = UrlRepository(app.config['DATABASE_URL'])

    @app.route('/')
    def index():
        app.logger.info('Запрос к /')
        messages = get_flashed_messages(with_categories=True)
        return render_template(
            'index.html',
            messages=messages
        )

    @app.route('/urls')
    def get_urls():
        app.logger.info('Запрос к /urls')
        messages = get_flashed_messages(with_categories=True)
        urls = repo.get_content()
        return render_template('urls/index.html', urls=urls, messages=messages)

    @app.post('/urls')
    def new_url():
        app.logger.info('POST запрос к /urls')
        url = request.form.to_dict()
        errors = validate(url)
        if errors:
            flash('Некорректный URL', 'error')
            return render_template('index.html'), 422
        saved, flag = repo.save(url)
        if flag:
            flash('Страница успешно добавлена', 'success')
        else:
            flash('Страница уже существует', 'info')
            return redirect(url_for('get_url', url_id=saved['id']))
        return redirect(url_for('get_urls'))

    @app.route('/urls/<int:url_id>')
    def get_url(url_id):
        app.logger.info('Запрос к /urls/<url_id>')
        messages = get_flashed_messages(with_categories=True)
        url = repo.find(url_id)
        if not url:
            abort(404)
        checks = repo.get_checks_with_id(url_id)

        return render_template(
            'urls/show.html',
            url=url,
            checks=checks,
            messages=messages
        )

    @app.post('/urls/<int:url_id>/checks')
    def check(url_id):
        app.logger.info(f'POST запрос к /urls/{url_id}/checks')
        url = repo.find(url_id)
        if not url:
            flash('No such id', 'error')
            return redirect(url_for('get_urls'))
        try:
            response = requests.get(url['name'], timeout=5)
            response.raise_for_status()
            result = perform_check(url['name'])
            repo.new_check(
                url_id,
                result['status_code'],
                result['h1'],
                result['title'],
                result['description']
            )
            flash('Проверка успешно выполнена', 'success')
        except Exception:
            app.logger.exception('Failed to create url_check')
            flash('Произошла ошибка при проверке', 'error')
            return redirect(url_for('get_url', url_id=url_id))

        return redirect(url_for('get_url', url_id=url_id))

    @app.errorhandler(404)
    def not_found(error):
        app.logger.error(f'404 error: {error}')
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f'404 error: {error}')
        return render_template("errors/500.html"), 500

    return app


app = create_app()
