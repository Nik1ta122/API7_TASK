import json
import requests

def fetch_github_user_data(github_token):
    try:
        api_url = "https://api.github.com/user"
        headers = {'Authorization': f'Bearer {github_token}'}

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