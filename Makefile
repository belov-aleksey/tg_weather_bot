# Установка зависимостей
install:
	python3 -m venv venv
	. venv/bin/activate && pip install -r requirements.txt

# Запуск бота вручную
run:
	. venv/bin/activate && python3 bot.py

# Очистка
clean:
	rm -rf venv
	find . -type d -name "__pycache__" -exec rm -rf {} +