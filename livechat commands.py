from TikTokLive import TikTokLiveClient
from TikTokLive.types.events import CommentEvent, ConnectEvent, GiftEvent, FollowEvent
from cleantext import clean
import pyttsx3

# FOR EASY SETUP, GO LIVE, REPLACE MY USERNAME WITH YOURS AND TOGGLE ON THE TTS COMPONENTS YOU WANT
username = "@tuckerisafurry" # REPLACE THIS WITH YOURS (RUN AFTER YOU GO LIVE)
oncomment = True
onfollow = True
ongift = True
cleantext = True

# Instantiate's objects
client: TikTokLiveClient = TikTokLiveClient(unique_id=username)
engine = pyttsx3.init()

# the actual speaking words function
def speakwords(words):
    engine.stop()
    if cleantext == True:
        engine.say(clean(words, no_emoji=True))
    elif cleantext == False:
        engine.say(words)
    engine.runAndWait()
    engine.stop()

# Define how you want to handle specific events via decorator

@client.on("connect")
async def on_connect(_: ConnectEvent):
    print("Connected to Room ID:", client.room_id)
    
# Notice no decorator?
async def on_comment(event: CommentEvent):
    print(f"{event.user.unique_id} says {event.comment}")
    if oncomment == True:
        if "/tts" in event.comment:
            speakwords(f"{event.user.nickname} says {event.comment[4:]}")
    
async def on_gift(event: GiftEvent):
    # Streakable gift & streak is over
    if event.gift.streakable and not event.gift.streaking:
        print(f"{event.user.unique_id} sent {event.gift.count}x \"{event.gift.info.name}\"")
        if ongift == True:
            speakwords(f"{event.user.nickname} sent {event.gift.count} \"{event.gift.info.name}\"")
        
    # Non-streakable gift
    elif not event.gift.streakable:
        print(f"{event.user.unique_id} sent \"{event.gift.info.name}\"")
        if ongift == True:
            speakwords(f"{event.user.nickname} sent a \"{event.gift.info.name}\"")
        
@client.on("follow")
async def on_follow(event: FollowEvent):
    print(f"@{event.user.unique_id} just followed!")
    if onfollow == True:
        speakwords(f"{event.user.nickname} just followed!")
    
# Define handling an event via a "callback"
client.add_listener("comment", on_comment)
client.add_listener("gift", on_gift)
client.add_listener("follow", on_follow)

if __name__ == '__main__':
    # Run the client and block the main thread
    # await client.start() to run non-blocking
    client.run()
