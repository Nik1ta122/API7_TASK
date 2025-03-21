from flask import Flask, render_template, redirect, url_for
import json
from API2 import fetch_github_user_data

app = Flask(__name__, template_folder='templates')

with open('config.json') as config_file:
    config = json.load(config_file)

@app.route('/')
def resume():
    user_data = fetch_github_user_data(config["github_token"])

    if not user_data:
        print("Данные не получены. Проверьте логи.")
        user_data = {}

    print("Данные, передаваемые в шаблон:", json.dumps(user_data, indent=4))
    return render_template('resume_template.html', user=user_data)

@app.route('/update')
def update():
    return redirect(url_for('resume'))

if __name__ == '__main__':
    app.run(debug=True)

