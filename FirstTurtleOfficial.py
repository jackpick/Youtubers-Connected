####imports
import requests
import json
import time

##variables used throughout

#this provides the link in order to use the API
api_key = ### insert your own Youtube Data API key here ###

## sub procedures

# for every possible channel url channel
def FindUploadsID():
    urlChannel = "https://www.googleapis.com/youtube/v3/channels?part=contentDetails&id=" + channel_id + "&key=" + api_key # creates API URL

    ##uses the API to read the specific web page and then display it

    #connect to API
    ###time.sleep(500) # If being used continuously, uncomment this line to delay program by 500 seconds in order to not exceed quota as a new day will now start before quota limit is exceeded
    ChannelAPIPage = requests.get(urlChannel)
    #pull data from API
    ChannelData = ChannelAPIPage.text
    #parse data into a JSON format so it can properly be processed
    JsonChannelData=json.loads(ChannelData)
    #find exact location of uploads ID in JsonData and put into a string
    global UploadsID
    UploadsID = str(JsonChannelData["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"])
    


###################################################################################################

#start from Oli White - felt a nice central point to start but feel free to change
ChannelURL = "https://www.youtube.com/channel/UCUWhWgXOjE1ET2CRRtgcnQw" #sets inital channel URL as Oli White
# Gets channel ID from URL
channel_id = ChannelURL.rsplit("/", 1)[1]
#set up lists
PossibleChannelURLs = [] # will contain the list of IDs that are going to be searched through next time round
AllChannelURLs = [] # will contain all the channel IDs found - final product
AllChannelNames = [] # will contain all the channel names found - final product
AreAllChannelsFound = 0 # sets this to 0 as all channels are not yet found

while AreAllChannelsFound == 0: # sets up a loop that runs continuously until all channels are found
    CurrentChannelURLs = [] #sets up a list for the current channel IDs to be put into - also empties all items that were previously in it
    if PossibleChannelURLs == []: # this checks if this is the first run through or not
        CurrentChannelURLs.append(channel_id) # if it is, then just use the initial link
        AllChannelURLs.append(channel_id) # this makes sure that the first channel is in the list as well
        PossibleChannelURLs.append(channel_id) # I have to put this in just so that the next if statement can work for the initial channel URL
    else:
        CurrentChannelURLs=PossibleChannelURLs # if it isn't, set current list to list that was made for the next run through
    if PossibleChannelURLs == []: # if the program has found all the channels, print the lists of channels and exit the loop
        print ("List of all channel IDs: " + AllChannelURLs)
        print (" ") # print an empty line to split them up and make them look nicer
        print ("List of all channel names: " + AllChannelNames)
        AreAllChannelsFound = 1
    else: # else, continue running the program
        PossibleChannelURLs = [] # empties all items that were previously in it

        for channel_id in CurrentChannelURLs:#loops through every channel ID found in the last search
            try: #this sets up a try statement to make sure that the program doesn't crash if a "false" ID is found
                FindUploadsID() #call sub procedure


                ### for every Uploads playlist URL
                    
                #empty whatever was previously in the page token from the last uploads list
                PageToken = ""

                EndLoop = 0
                while EndLoop == 0:
                    
                    ##go to this display
                    #checks to see if PageToken is empty ie. if its the first page
                    if PageToken == "":
                        #if it is the first page, then dont use the variable PageToken as it is not needed
                        UploadsURL = "https://youtube.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=50&playlistId=" + UploadsID + "&key=" + api_key
                    else:
                        #if it is looking for another page then use the variable PageToken as it will only return the forst page without the page token
                        UploadsURL = "https://youtube.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=50&playlistId=" + UploadsID + "&key=" + api_key + "&pageToken=" + PageToken

                    #sets up a counter
                    VideoCount = 0
                    #loops through each number in the counter - each number corresponds to a different video that we are going to search for youtube URLs in (has to be 50 as that is the max number of videos per page)
                    while VideoCount<50:
                        #tries to find the comments section of the specific video number - I am using a try statement as this will allow me to account for the final page of the uploads, which may not have 50 videos, without the program failing
                        try:
                            #uses the API to read the specific web page and then display it

                            #connect to API
                            ###time.sleep(500) # If being used continuously, uncomment this line to delay program by 500 seconds in order to not exceed quota as a new day will now start before quota limit is exceeded
                            UploadsAPIPage = requests.get(UploadsURL)
                            #pull data from API
                            UploadsData = UploadsAPIPage.text
                            #parse data into a JSON format so it can properly be processed
                            JsonUploadsData=json.loads(UploadsData)
                            #find exact location of uploads ID in JsonData and put into a string
                            Description = str(JsonUploadsData["items"][VideoCount]["snippet"]["description"])
                            #splits up the comments by each bit of white space and puts each element into a list
                            DescriptionItems = Description.split()
                            #searches through every element of the comments
                            for PossibleChannelURL in DescriptionItems:
                                if "youtube.com/user/" in PossibleChannelURL: # checks if element is a username by checking its specific link structure
                                    ##uses the API to read the specific web page and then display it
                                    #gets username
                                    PossibleChannelUsername = PossibleChannelURL.rsplit("/", 1)[1]
                                    #gets API link
                                    urlPossibleChannel = "https://www.googleapis.com/youtube/v3/channels?part=contentDetails&forUsername=" + PossibleChannelUsername + "&key=" + api_key
                                    #connect to API
                                    ###time.sleep(500) # If being used continuously, uncomment this line to delay program by 500 seconds in order to not exceed quota as a new day will now start before quota limit is exceeded
                                    PossibleChannelURLAPIPage = requests.get(urlPossibleChannel)
                                    #pull data from API
                                    PossibleChannelURLData = PossibleChannelURLAPIPage.text
                                    #parse data into a JSON format so it can properly be processed
                                    JsonPossibleChannelURLData=json.loads(PossibleChannelURLData)
                                    #find exact location of uploads ID in JsonData and put into a string
                                    PossibleChannelURLID = str(JsonPossibleChannelURLData["items"][0]["id"]) #finds channel ID
                                    PossibleChannelURL = "https://www.youtube.com/channel/" + PossibleChannelURLID # basically converts username URL into a channel ID URL to make the whole process much easier with no IF statements
                                    
                                if "youtube.com/channel/UC" in PossibleChannelURL: #adds it to a new list of possible channel URLs if element is a channel ID, by checking for its specific link structure
                                    if "..." not in PossibleChannelURL: # some URLs collected have elipsis in them - this line makes sure they arent included as they wouldn't work
                                        PossibleChannelURL = PossibleChannelURL.rsplit("/", 1)[1]
                                        if len(PossibleChannelURL)== 24: #this trys to remove unwanted data i.e at the end of some links, there is sometimes "/videos" - this would break the prgram if this was allowed throug
                                            if PossibleChannelURL not in AllChannelURLs: #this makes sure that an element is only added if it is not already in there - avoiding duplicates
                                                AllChannelURLs.append(PossibleChannelURL) #add this channel ID to the list of total channel IDs
                                                PossibleChannelURLs.append(PossibleChannelURL)# add this channel to the list of channel IDs to search through next
                            #adds 1 to the counter so the description for the next video can be obtained
                            VideoCount=VideoCount+1
                        except:
                            #if this try statement fails then it means that there is no more videos so I end the loop by setting the video count to 50
                            VideoCount=50
                    #finds the next page token so we can go onto the next page of uploads
                    try:
                        #tries to find the next page token - I am using a try statement as this will allow me to account for the final page of the uploads, which will not have a next page token, without the program failing
                        PageToken = str(JsonUploadsData["nextPageToken"])
                    except:
                        #when the program cannot find a next page token, it will end the loop by making EndLoop not equal 0
                        EndLoop = 1
                print ("Channel ID: " + channel_id) # print channel ID as this channel works - delete this if you don't want to see channel IDs
                #find exact location of channel in JsonData and put into a string
                ChannelName = str(JsonUploadsData["items"][0]["snippet"]["channelTitle"])# this is basically the same as finding the description, except you are finding a different part, you just go onto a video and find the channel name, the video count is set to 0 here in case of the page only having 1 item - it also just uses a previous variable which will still be the same in order to create less queries, speeding up the program
                AllChannelNames.append(ChannelName) #add this channel name to the list of total channel names
                print ("Channel name: " + ChannelName)
                print (" ") # print an empty line to separe the channels
            except: #if a false ID is found, nothing happens - it just deletes this false ID and name from the total set of IDs names
                AllChannelURLs.remove(channel_id)
