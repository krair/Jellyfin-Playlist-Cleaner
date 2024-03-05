import sys
import os
import pathlib
import logging
import xml.etree.ElementTree as ET
from datetime import datetime
from shutil import copy2

###################################################
# Set these before running the script
container_directory = '/music'
host_directory = '/mnt/media/music'
# Once you've set the above correctly, delete or comment out (#) the line below!
sys.exit("ERROR! Please set the container_directory and host_directory variables, then delete this line!")
###################################################

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)

USAGE = f"""Usage: python {sys.argv[0]} COMMAND [OPTIONS] \n
COMMANDS:\r
--restore <file> OR <directory> to restore backed up playlist file\r
--clean <file> OR <directory>\r
NB: If passing a directory, it will automatically work recursively!!\n
OPTIONS:\r
--no-backup Do not create backups of playlist when using the --clean command.\r
--dry-run Show what would be removed from playlist, but don't actually remove (implies --no-backup)
"""

def restore(args):
	logging.error("Not implemented yet. But if you've run the script before, there's a backup in the playlist's directory with the date it was created and a '.bak' extension. You'll have to manually restore it!")

def main(args):
	path = pathlib.Path(args[0])
	for i in get_playlists(path):
		if not any(x in args for x in ('--no-backup', '--dry-run')):
			logging.info(f"Creating backup for playlist: {str(i)}")
			copy2(i, str(i) + '_' + datetime.strftime(datetime.now(), "%Y%m%d%H%M") + '.bak')
		with open(i) as file:
			playlist = ET.parse(file)
		tracklist = playlist.find('PlaylistItems')
		logging.info(f'Playlist {i.parts[-2]} contains {len(tracklist)} Tracks before cleaning.')
		for track in tracklist.findall('PlaylistItem'):
			if os.path.isfile(track[0].text.replace(container_directory, host_directory)):
				logging.info(f"File exists: {track[0].text.replace(container_directory, host_directory)}")
				continue
			else:
				logging.warning(f"File not found! Removing {track[0].text.replace(container_directory, host_directory)}")
				if not '--dry-run' in args:
					tracklist.remove(track)
		logging.info(f'Playlist {i.parts[-2]} contains {len(tracklist)} Tracks after cleaning.')
		playlist.write(i)

def get_playlists(root: pathlib.Path):
	# If a single playlist is passed
	if root.is_file() and root.name == 'playlist.xml':
		yield root
	# If a directory is passed
	else:
	    for item in root.iterdir():
	        if item.is_file() and item.name == 'playlist.xml':
	            yield item
	        elif item.is_dir():
	            yield from get_playlists(item)
	        else:
	        	continue

if __name__ == "__main__":
    args = sys.argv[1:]

    if not args:
        raise SystemExit(USAGE)
    else:
        if args[0] == '--restore':
                restore(args[1:])
        elif args[0] == '--clean':
                main(args[1:])
        else:
                raise SystemExit(USAGE)