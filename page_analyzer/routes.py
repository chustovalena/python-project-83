from flask import \
    render_template, \
    url_for, \
    request, \
    redirect, \
    get_flashed_messages, \
    abort, \
    flash
from page_analyzer.services.normalize import normalize_url
from page_analyzer.services.validate import validate
import requests
from page_analyzer.services.checks import perform_check


def register_urls(app, repo):
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
        normalized = normalize_url(url['url'])
        saved, flag = repo.save({'url': normalized})
        if flag:
            flash('Страница успешно добавлена', 'success')
        else:
            flash('Страница уже существует', 'info')
            return redirect(url_for('get_url', url_id=saved['id']))
        return redirect(url_for('get_url', url_id=saved['id']))

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


def register_checks(app, repo):
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
            flash('Страница успешно проверена', 'success')
        except Exception:
            app.logger.exception('Failed to create url_check')
            flash('Произошла ошибка при проверке', 'error')
            return redirect(url_for('get_url', url_id=url_id))

        return redirect(url_for('get_url', url_id=url_id))


def register_errors(app):
    @app.errorhandler(404)
    def not_found(error):
        app.logger.error(f'404 error: {error}')
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f'500 error: {error}')
        return render_template("errors/500.html"), 500


def register_routes(app, repo):
    register_errors(app)
    register_urls(app, repo)
    register_checks(app, repo)
