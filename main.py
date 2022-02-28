#!/usr/bin/env python3

import os
from pathlib import Path
from itertools import repeat, chain
from typing import Union
import shutil

controls = """
Actions=Play/Pause;Next;Previous;Stop

[Desktop Action Play/Pause]
Name[en]=Play/Pause
Name[es]=Reproducir/Pausa
Exec=dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.PlayPause

[Desktop Action Next]
Name[en]=Next
Name[es]=Siguiente
Exec=dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Next

[Desktop Action Previous]
Name[en]=Previous
Name[es]=Anterior
Exec=dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Previous

[Desktop Action Stop]
Name[en]=Stop
Name[es]=Parar
Exec=dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Stop
"""

def fileContains(path: Path, text: str) -> bool:
    with open(path, 'rb') as f:
        for line in f:
            if text in line.decode('utf-8', 'ignore'):
                return True
    return False

def lookForExistingIn(path: Path, textToFind: str) -> Union[Path, None]:
    gen1 = ((Path(root, file) for file in files) for root, _, files in os.walk(path))
    gen2 = chain.from_iterable(gen1)
    gen2 = (file for file in gen2 if 
        file.is_file() and
        os.access(file, os.R_OK) and
        file.suffix == ".desktop" and
        fileContains(file, "Exec=spotify"))

    try:
        return next(gen2)
    except StopIteration:
        return None

def addControls(path: Path):
    path.open('a').write(controls)

dataPath = Path(os.environ.get("XDG_DATA_HOME", "~/.local/share")).expanduser()
desktopFile = lookForExistingIn(dataPath, "Exec=spotify")

if desktopFile is not None:
    if not fileContains(desktopFile, "[Desktop Action Play/Pause]"):
        addControls(desktopFile)
        print("Spotify actions added succesfully")
    else:
        print("Desktop file already contains controls")
else:

    def copyAndAdd(path: Path):
        userFile = dataPath.joinpath(path.name)
        shutil.copy(path, userFile)
        addControls(userFile)

    flatpakPath = Path("/var/lib/flatpak/app/com.spotify.Client/current/active/files/share/applications/com.spotify.Client.desktop")
    snapPath = Path("/var/lib/snapd/desktop/applications/spotify_spotify.desktop")

    if flatpakPath.is_file():
        copyAndAdd(flatpakPath)
        print("Spotify actions added succesfully")
    elif snapPath.is_file():
        copyAndAdd(snapPath)
        print("Spotify actions added succesfully")
    else:
        print("Could not find Spotify desktop file")

    
