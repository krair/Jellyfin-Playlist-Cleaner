# Jellyfin Playlist Cleaner

Simple Python program to clean up playlists that contain missing files.

This seems to be less of an issue in Jellyfin 10.8.13, but I had some big playlists that were full of old, missing files.

## Motivation

Jellyfin's playlists are stored in XML format. Trying to manipulate them via `bash` is possible, but a pain and requires dependencies. Python is MUCH easier, but not included in the Jellyfin container image. Thus this script is intended to run on the host. It was written and tested on a machine running Python 3.9.18.

I originally wrote this with the intention of cleaning up music playlists, where all of the music files live in a single directory. Any other uses will likely break your playlist or not work. Use at your own risk!

## Usage

1. Download the python file (or clone the repository)
2. Open the `jf_playlist_cleaner.py` file in your favorite editor, and set the `container_directory` and `host_directory` variables at the top of the file.

Note: When you run a container and mount directories inside it, it will look like `/host/directory:/container/directory`. For example, if my music files are on the host at `/mnt/media/music`, I would set that as the `host_directory` variable. **Do not add a trailing slash!** Where your files live in the container will depend on how you've mounted them. To check, you can go to your Jellyfin --> Admin Dashboard --> Libraries and check your mount point.

3. Run the script as such:

```bash
python3 jf_playlist_cleaner.py --clean /path/to/jellyfin/playlist/directory --dry-run
```

Note: The playlists directory is in your Jellyfin `config` directory under `config/data/playlists`. You can run the script on a single playlist, or all playlists in the playlist directory - it will work recursively if you just point it at `config/data/playlists`. 

If everything looks good, you can run without the `--dry-run` flag

The script will make a backup of your current playlist, and tag it with a timestamp and a `.bak` extension. **I haven't yet written the restore function. If you want to restore an old version, you'll have to manually copy the `.bak` file to the `playlist.xml` filename!**

## NB

### How it works

This basic program reads the playlist to find the PlaylistItems in the XML file. It then simply tests whether or not that file exists. If it does not exist, it is removed from the playlist.

The script assumes you are running Jellyfin in a container. If you aren't, you can set the `host_directory` and `container_directory` to be the same.

If you have your music stored in multiple locations on the host (like: `/mnt/storage/music` and `/media/hdd1`), or in multiple locations in the container (like `/music` and `/music2`), **this script will not work for you**. It is simple and does what I need.

### What it **doesn't** do

- Find incorrect file paths and replace with correct ones
- Find corrupted files in a playlist
- Traverse multiple directories.