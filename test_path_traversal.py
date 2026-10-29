from urllib.request import urlopen
from urllib.parse import urlencode


def test_path_traversal():
	params = urlencode({"name": "../secret.txt"})
	url = f"http://127.0.0.1:8000/file?{params}"

	with urlopen(url) as response:
		page = response.read().decode("utf-8")

	print("Ответ сервера:")
	print(page)

	if "Учебный секретный файл для демонстрации" in page:
		print("\nУязвимость подтверждена: файл прочитан.")
	elif "Доступ запрещён" in page:
		print("\nЗащита работает: доступ запрещён.")
	else:
		print("\nФайл не раскрыт. Проверь ответ сервера.")


if __name__ == "__main__":
	test_path_traversal()
