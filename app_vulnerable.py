from http.server import  HTTPServer, BaseHTTPRequestHandler
import sqlite3
from pathlib import Path
from urllib.parse import urlparse, parse_qs

def create_datebase():
	connection=sqlite3.connect("users.db")
	connection.execute(
		"CREATE TABLE IF NOT EXISTS users"
		"(id INTEGER PRIMARY KEY, username TEXT, role TEXT)"
		)
	connection.executemany(
		"INSERT OR IGNORE INTO users VALUES (?, ? ,?)",
		[
			(1, "admin", "administrator"),
			(2, "Ivan", "student"),
			(3, "Petr", "student")
		],
		)
	connection.commit()
	connection.close()

class MyHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		parsed = urlparse(self.path)
		params = parse_qs(parsed.query)

		if parsed.path == "/file":
			filename = params.get("name", [""])[0]
			file_path = Path("public") / filename

			try:
				content = file_path.read_text(encoding="utf-8")
				page = (
					"<h1>Содержимое файла</h1>"
					f"<pre>{content}</pre>"
					"<a href='/'>Назад</a>"
					)
			except (OSError, UnicodeError) as error:
				page = f"<p>Ошибка чтения файла: {error}</p>"

		elif parsed.path == "/search":
			username = params.get("username", [""])[0]
			connection = sqlite3.connect("users.db")

			query = (
				f"SELECT username, role FROM users "
				f"WHERE username = '{username}'"
			)

			try:
				users = connection.execute(query).fetchall()
				result = "<ul>"
				for user in users:
					result += f"<li>{user[0]} — {user[1]}</li>"
					result += "</ul>"
			except sqlite3.Error as error:
				result = f"<p>Ошибка SQL: {error}</p>"

			connection.close()
			page = f"<h1>Результаты поиска</h1>{result}<a href='/'>Назад</a>"
		else:
			page = """
			<h1>Поиск пользователей</h1>
			<form action="/search" method="get">
				<input name="username" placeholder="Введите имя">
				<button type="submit">Найти</button>
			</form>
			"""

		html = f"""
		<!DOCTYPE html>
		<html lang="ru">
		<head><meta charset="UTF-8"><title>Лабораторная №2</title></head>
		<body>{page}</body>
		<p><a href="/file?name=info,txt">Открыть публичный файл</a></p>
		</html>
		"""

		self.send_response(200)
		self.send_header("Content-Type", "text/html; charset=utf-8")
		self.end_headers()
		self.wfile.write(html.encode("utf-8"))

create_datebase()
server = HTTPServer(("127.0.0.1", 8000), MyHandler)
print("Сервер запущен: http://127.0.0.1:8000")
server.serve_forever()
