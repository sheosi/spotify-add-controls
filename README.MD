# Spotify Add Controls

A Simple Python script to add media controls to Spotify's dock icon in Linux. Supports Spotify installed by package, *Flatpak* and *Snap*. The script will check if media controls are present and won't operate if they are to be found.

Based on https://www.omgubuntu.co.uk/2022/01/add-spotify-player-controls-ubuntu-dock-icon.

Minimum version of Python: 3.8

## Usage

```shell
python3 main.py
```

It will detect which version of Spotify is available and will copy the '.desktop' file into the user's location, appending the controls into the file.
