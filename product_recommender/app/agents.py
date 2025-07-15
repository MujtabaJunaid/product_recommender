from youtubesearchpython import VideosSearch
import yt_dlp
import whisper
from moviepy.editor import AudioFileClip
from textblob import TextBlob
from langchain_groq import ChatGroq
import tempfile
import os

llm = ChatGroq(model_name="llama3-70b-8192", temperature=0)

def check_specificity(state):
    query = state["product_query"]
    result = llm.invoke(f"Is this product query specific? Query: {query}")
    state["is_specific"] = "yes" in result.content.lower()
    return state

def youtube_search(state):
    search = VideosSearch(state["product_query"], limit=5)
    state["video_data"] = [{"title": v["title"], "link": v["link"], "id": v["id"]} for v in search.result()["result"]]
    return state

def transcribe_audio(state):
    model = whisper.load_model("base")
    for video in state["video_data"]:
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                ydl_opts = {"format": "bestaudio", "outtmpl": f"{temp_dir}/audio.%(ext)s", "quiet": True}
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([video["link"]])
                audio_path = f"{temp_dir}/audio.mp3"
                clip = AudioFileClip(audio_path)
                clip.write_audiofile(f"{temp_dir}/audio.wav", codec="pcm_s16le")
                video["transcript"] = model.transcribe(f"{temp_dir}/audio.wav")["text"]
        except Exception as e:
            print(f"Error processing {video['title']}: {e}")
    return state