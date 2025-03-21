import json
import requests
from flask import Flask, render_template, redirect, url_for

app = Flask(__name__, template_folder='templates')

with open('config.json') as config_file:
    config = json.load(config_file)

def fetch_github_user_data():
    try:
        api_url = "https://api.github.com/user"
        headers = {'Authorization': f'Bearer {config["github_token"]}'}

        print("Запрашиваемый URL:", api_url)
        print("Заголовки запроса:", headers)

        response = requests.get(api_url, headers=headers)

        if response.status_code != 200:
            print(f"Ошибка: {response.status_code}, ответ: {response.text}")
            return {}

        if 'application/json' not in response.headers.get('Content-Type', ''):
            print("Ошибка: Сервер вернул HTML вместо JSON.")
            print("Ответ:", response.text[:500])
            return {}

        print("Ответ от API:", response.text)
        user_data = response.json()
        print("Полученные данные:", json.dumps(user_data, indent=4))
        return user_data

    except json.JSONDecodeError:
        print("Ошибка декодирования JSON:", response.text)
        return {}
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return {}

@app.route('/')
def resume():
    user_data = fetch_github_user_data()

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

