pyinstaller ./src/main.py --noconfirm \
    --add-data="src/database.db:." \
    --add-data="src/config.yaml:." \
    --add-data="src/anime-titles.dat:." \
    --contents-directory="OSX" \
    --name="Epifetch" \
    --console \