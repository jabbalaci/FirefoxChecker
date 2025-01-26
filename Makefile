cat:
	cat Makefile

compile:
	pyrcc5 systray.qrc -o systray_rc.py

run:
	uv run systray.py
