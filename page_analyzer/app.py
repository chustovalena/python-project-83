import logging
import os
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
app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')
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
    urls = repo.get_content()
    app.logger.info('Запрос к /urls')
    return render_template('urls/index.html', urls=urls)


@app.post('/urls')
def new_url():
    app.logger.info('POST запрос к /urls')
    url = request.form.to_dict()
    errors = validate(url)
    if errors:
        for error in errors:
            flash(error, "danger")
        return redirect(url_for('index'))
    saved = repo.save(url)
    print(saved)
    if 'id' in saved:
        flash('Url был успешно добавлен', 'success')
    else:
        flash('Url уже существует')
    return redirect(url_for('get_urls'))


@app.route('/urls/<url_id>')
def get_url(url_id):
    app.logger.info('Запрос к /urls/<url_id>')
    url = repo.find(url_id)
    if not url:
        abort(404)
    return render_template(
        'urls/show.html',
        url=url
    )
