pyinstaller ./src/main.py --noconfirm --log-level=WARN \
    --add-data="database.db:." \
    --add-data="config.yaml:." \
    --add-data="anime-titles.dat:." \
    --contents-directory="WIN" \
    --name="Epifetch" \
    --console \