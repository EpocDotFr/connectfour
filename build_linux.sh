# Shell script to build the Connect Four Linux executable.
# The resulting "connectfour_linux" script will be available in the "dist" directory.

pyinstaller \
    --clean --noconfirm --onefile \
    --log-level=WARN \
    --name="connectfour_linux" \
    --add-data="resources:resources" \
    run.py