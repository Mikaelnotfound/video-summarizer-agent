from dotenv import load_dotenv
import os
import datetime
import re
import yt_dlp
import whisper
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.tools import tool

load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(google_api_key=google_api_key, model="gemini-2.5-flash")

@tool
def get_video_content(url: str) -> str:
    """
    Downloads audio from a YouTube video, transcribes it using Whisper, and returns the text.
    This function is more robust as it does not rely on pre-existing subtitles in the video.
    """
    print(f"Starting transcription process for URL: {url}")
    audio_file = "temp_audio.mp3"

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'temp_audio',
        'quiet': True,
    }

    try:
        print("Downloading audio...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("Audio download complete.")

        print("Loading Whisper model...")
        model = whisper.load_model("base")
        print("Model loaded.")

        print("Transcribing audio... (This may take a few minutes depending on the video size)")
        result = model.transcribe(audio_file, fp16=False)
        transcription = result["text"]
        print("Transcription complete.")
        
        return f"Video transcription: {transcription}"

    except Exception as e:
        print(f"An error occurred during the process: {e}")
        return (f"Error processing video. "
                f"Check if the URL '{url}' is valid and accessible. "
                f"Error detail: {e}")
    finally:
        if os.path.exists(audio_file):
            os.remove(audio_file)
            print(f"Temporary file '{audio_file}' removed.")

tools = [get_video_content]

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an agent specialized in summarizing YouTube videos. Use the 'get_video_content' tool to get the transcription of a video, and then create a detailed report. Include the central topic and the main points of the video."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])

agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools)

def is_valid_youtube_url(url):
    """Checks if the URL has a valid YouTube format."""
    youtube_regex = (
        r'(https?://)?(www.)?'
        r'(youtube|youtu|youtube-nocookie).(com|be)/'
        r'(watch?v=|embed/|v/|.+?v=)?([^&=%?]{11})')
    return re.match(youtube_regex, url)

def generate_video_report(url: str):
    """
    Generates and saves a summary report of a YouTube video.
    """
    if not is_valid_youtube_url(url):
        print("Invalid URL. Please enter a valid YouTube URL.")
        return

    print("\nInvoking the agent to generate the report...")
    response = agent_executor.invoke({
        "input": f"Generate a report for the video at this URL: {url}"
    })

    content = response['output']

    if "Error processing video" in content:
        print("\nCould not generate the report due to an error in content extraction.")
        print(content)
        return

    reports_dir = 'reports'
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = os.path.join(reports_dir, f"video-report-{timestamp}.txt")

    with open(file_name, 'w', encoding='utf-8') as video_file:
        video_file.write("---" + " " + "VIDEO REPORT" + "---" + "\n")
        video_file.write(f"URL: {url}\n")
        video_file.write(f"Generation Date: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        video_file.write("--------------------------------\n\n")
        video_file.write(content)

    print(f"\nReport saved successfully to file: '{file_name}'")


if __name__ == '__main__':
    try:
        url = input("Enter the YouTube video URL: ")
        generate_video_report(url)
    except KeyboardInterrupt:
        print("\nOperation canceled by the user.")