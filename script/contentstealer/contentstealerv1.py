# -*- coding: utf-8 -*-

# Sample Python code for youtube.channels.list - thanks google!!!
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os
import time
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import googleapiclient.http
import google.oauth2.credentials
import requests

client_id = "insert_client_here"
client_secret = "insert_secret_here"
youtubechannelid = "youtube_channel_id_here"

update = True
uploadnow = True

try:
  with open('token.txt', 'r') as f:
    refresh_token = f.read()
except:
  print("No Previous Token Found - Regeneration Step Needed")
  refresh_token = ""


#with open('channelids.txt', 'r') as f:
#  channelid = dict(f.read())

scopes = ["https://www.googleapis.com/auth/youtube"]

def main():
    print("Started Routine")
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "secret.json"

    if refresh_token == "":
      # Get credentials and create an API client
      flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
      credentials = flow.run_console()
      with open('token.txt', 'w') as f:
        f.write(str(credentials.refresh_token))
    else:
      ## THANKS JOHN HANLEY https://stackoverflow.com/questions/54321848/how-to-use-refresh-token-google-api-in-python
        
      ## This function creates a new Access Token using the Refresh Token
      ## and also refreshes the ID Token (see comment below).
      def refreshToken(client_id, client_secret, refresh_token):
        params = {
            "grant_type": "refresh_token",
            "client_id": client_id,
            "client_secret": client_secret,
            "refresh_token": refresh_token
        }

        authorization_url = "https://www.googleapis.com/oauth2/v4/token"

        r = requests.post(authorization_url, data=params)

        if r.ok:
          return r.json()['access_token']
        else:
          return None
        
      ## Call refreshToken which creates a new Access Token
      access_token = refreshToken(client_id, client_secret, refresh_token)
      if access_token == None:
        refresh_token == ""
        print("Token Unknown, Reseting")
        main()
      print("Refreshed Token")
      ## Pass the new Access Token to Credentials() to create new credentials
      credentials = google.oauth2.credentials.Credentials(access_token)
      print("Built Credentials")

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)
    print("Built Service")

    print("Requesting Upload Playlist")
    x = 0
    request = youtube.channels().list(
      part="contentDetails",
      id=youtubechannelid
    )
    uploads = request.execute()
    uploads = uploads['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    print("Requesting Upload Playlist Items")
    request = youtube.playlistItems().list(
      part="snippet,contentDetails",
      maxResults=50,
      playlistId=uploads
    )
    response = request.execute()
    ## this part deals with the nextpage
    x = 1
    page=response.get('nextPageToken')
    response = response['items']
    
    y = 0
    while x == 1:
      if page == None:
        x = 2
        break
      print("Requesting Upload Playlist Items Page " + page)
      request = youtube.playlistItems().list(
      part="snippet,contentDetails",
      maxResults=50,
      pageToken=page,
      playlistId=uploads
      )
      nextpageresults = request.execute()
      page = nextpageresults.get('nextPageToken')
      nextpageresults = nextpageresults['items']
      response = response + nextpageresults
      y +=1

    videolist = []
    y = 0
    for x in response:
      info = response[y]['snippet']
      infowrite = {'title': info['title'], 'thumbnails':info['thumbnails']['default']['url'], 'resourceid':info['resourceId']['videoId']}
      videolist.append(infowrite)
      y += 1

    description = """
    Edit your description here!!!
    """
    tags = ["tags", "are", "like", "this"]

    def upload_video(video,title,description,category=23,privacy='private',tags=[]):
      """
      youtube is made with get_authenticated_service()
      category is a number, see https://developers.google.com/youtube/v3/docs/videoCategories/list for more
      raises HttpError if connection error
      """

      body=dict(
        snippet=dict(
            title=title,
            description=description,
            tags=tags,
            categoryId=category
        ),
        status=dict(
            privacyStatus=privacy
        )
      )

      # Call the API's videos.insert method to create and upload the video.
      insert_request = youtube.videos().insert(
        part=','.join(body.keys()),
        body=body,
        # The chunksize parameter specifies the size of each chunk of data, in
        # bytes, that will be uploaded at a time. Set a higher value for
        # reliable connections as fewer chunks lead to faster uploads. Set a lower
        # value for better recovery on less reliable connections.
        #
        # Setting 'chunksize' equal to -1 in the code below means that the entire
        # file will be uploaded in a single HTTP request. (If the upload fails,
        # it will still be retried where it left off.) This is usually a best
        # practice, but if you're using Python older than 2.6 or if you're
        # running on App Engine, you should set the chunksize to something like
        # 1024 * 1024 (1 megabyte).
        media_body=googleapiclient.http.MediaFileUpload(video, chunksize=-1, resumable=True)
      )

      return resumable_upload(insert_request)

    # This method implements an exponential backoff strategy to resume a
    # failed upload.
    def resumable_upload(request):
      response = None
      error = None
      retry = 0
      while response is None:
        try:
            print()
            print( 'Uploading file...')
            status, response = request.next_chunk()
            if response is not None:
                # print(response)
                if 'id' in response:
                    print()
                    print( 'Video id "%s" was successfully uploaded.' % response['id'])
                    return f'https://www.youtube.com/watch?v={response["id"]}'
                else:
                    exit('The upload failed with an unexpected response: %s' % response)
        except HttpError as e:
            if e.resp.status in RETRIABLE_STATUS_CODES:
                error = 'A retriable HTTP error %d occurred:\n%s' % (e.resp.status, e.content)
            else:
                raise
        except RETRIABLE_EXCEPTIONS as e:
            error = 'A retriable error occurred: %s' % e

        if error is not None:
            print( error)
            retry += 1
            if retry > MAX_RETRIES:
                exit('No longer attempting to retry.')

            max_sleep = 2 ** retry
            sleep_seconds = random.random() * max_sleep
            print( 'Sleeping %f seconds and then retrying...' % sleep_seconds)
            time.sleep(sleep_seconds)

    videosuploaded = []
    try:
      with open('videolist.txt', 'r') as f:
        videosuploaded = eval(f.read())

      videostoupload = [x for x in videolist if x not in videosuploaded]

      videolist = videostoupload
    except:
      print("Failed to find uploaded videos...")

    if type(videosuploaded) == "class 'str":
      videosuploaded = eval(videosuploaded)


    import youtube_dl
    for _ in videolist:## debug/ only a couple video
      ydl_opts = {'outtmpl': videolist[0]['resourceid']+'.mp4'
      }
      with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(['https://www.youtube.com/watch?v='+ videolist[0]['resourceid']])
        print(upload_video(video=videolist[0]['resourceid']+'.mp4',title=videolist[0]['title'],description=description,tags=tags))
        videosuploaded.append(videolist[0])
        print("Deleting Video")
        os.remove(str(videolist[0]['resourceid']+'.mp4'))
        del videolist[0]
      print("Saving Videos Uploaded List")
      with open('videolist.txt', 'w') as f:
        f.write(str(videosuploaded))

if __name__ == "__main__":
    main()
