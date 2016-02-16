# Jarek Wojciechowski
# spotifyArchiver.py - This program takes all of the current tracks in your discover weekly playlist and adds them to a playlist called "Discover weekly archive". This playlist is created if it doesn't exist

#TODO Create seperate file that sets this up as a CRON job

import spotipy,sys,os
import spotipy.util as util

def read_cfg(cfg, username):
	with open(cfg, 'r') as f:
		scope = str(f.readline())
		redirect = str(f.readline())
		client_id =  str(f.readline())
		client_secet = str(f.readline())
	return scope, redirect, client_id, client_secet, username

#TODO fix this function so that it will take a playlist contents and add all of the tracks instead of the current broken implementation
#Takes the contents of a playlist, and iterates over all of the tracks, and then creates a list of URIs
def add_tracks(results):
    for i, item in enumerate(tracks['items']):
        track = item['track']
        discoverTrackURIs.append(track["uri"])
        #TODO Don't add tracks if they already exist in the list
        print("The track " + track["name"] + " by " + "somebody(lol)" + " has been added!")


if __name__ == '__main__':

	#Validation of command line arguements
	if len(sys.argv) == 2:
	    username = sys.argv[1]
	else:
	    print ("Usage: %s username " % (sys.argv[0],))
	    sys.exit()

	#Get the user's token
	token = spotipy.util.prompt_for_user_token(*read_cfg('spotipy.cfg',sys.argv[1]))

	if token:
		#Create the connection, diable tracking, and get the playlist list
		sp = spotipy.Spotify(auth=token)
		sp.trace = False
		archiveID,discoverID = None,None
		playlists = sp.user_playlists(username)

		#Collect the playlist IDs for the archive and the discover weekly
		for playlist in playlists['items']:
			if playlist['name'] == "Discover Weekly Archive":
				archiveID = playlist['id']
			elif playlist['name'] == "Discover Weekly":
				discoverID = playlist['id']
				#Save the contents of the Discover Weekly playlist to extract later
				playlistContents = sp.user_playlist("spotifydiscover", playlist['id'], fields="tracks,next")
		#This checks if the archivefile was found when looking through the playlists, and creates one if neccesary
		if not archiveID:
			created_playlist = sp.user_playlist_create(username, "Discover Weekly Archive")
			archiveID = created_playlist['id']

		discoverTrackURIs = []
		#Not 100% about the actual function of this section. It came from  here
		#https://github.com/plamere/spotipy/blob/master/examples/user_playlists_contents.py
		tracks = playlistContents['tracks']
		add_tracks(tracks)
		while tracks['next']:
			tracks = sp.next(tracks)
			add_tracks(tracks)
		#Add the extracted URIs to the archive playlist
		archiveContents = sp.user_playlist_add_tracks(username, archiveID, discoverTrackURIs)
	else:
		print ("Can't get token for " + username)
