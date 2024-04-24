# ProotzyDownloader
A youtube video, audio, playlist and thumbnail downloader

## Start

Credits for the application icon: https://www.reddit.com/user/Kim_orange/

To get started, run the following commands:

Optional:
Instantiate a python virtual environment
`py -m venv venv`

Optional:
Start the environment
`./venv/Scripts/activate`

Install all required modules
`pip install -r ./src/requirements.txt`

Run the program 
`py ./src/main.py`


## Usage
### Video
Enter a youtube video url into the url input
After clicking convert, you can find the output in /videos

### Audio
Enter a youtube audio url into the url input
If you want to convert the output from mp4 to mp3, check the corresponding box
After clicking convert, you can find the output in /audio


### Playlist
Enter a youtube playlist url into the url input
Check only audio to only download audio (.mp4 files)
Check "Add index to file name" to add a prefix index to every file in the format "\[index]. "
Example:
1. Sometrack
2. Notsometrack
After clicking convert, you can find the output in /playlists/\[playlist name]


### Thumbnail
Download a thumbnail from a video
Select the format in "File Format"
Show file after shows the image in your gallery program afterwards
After clicking convert, you can find the output in /thumbnails
