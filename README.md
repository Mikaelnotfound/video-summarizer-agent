# Video Summarizer Agent

This project is a Python-based agent that automatically generates detailed summaries of YouTube videos. It takes a video URL, transcribes the audio content, and uses a Large Language Model (LLM) to create a comprehensive report.

## Features

- **YouTube Video Transcription**: Downloads the audio from any YouTube video and transcribes it into text using OpenAI's Whisper model.
- **Detailed Summarization**: Utilizes Google's Gemini model via LangChain to generate a detailed report, including the video's central topic and key points.
- **Report Generation**: Saves the generated summary as a `.txt` file in the `reports/` directory for future reference.
- **Robust Error Handling**: Checks for valid YouTube URLs and handles potential errors during the video processing pipeline.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- [Python 3.8+](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/installation/) (Python package installer)
- [FFmpeg](https://ffmpeg.org/download.html) (A command-line tool for handling multimedia data)

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/resume-video-agent.git
    cd resume-video-agent
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # For Linux/macOS
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up your environment variables:**
    - Rename the `.env.example` file to `.env`.
    - Open the `.env` file and add your Google API key:
      ```
      GOOGLE_API_KEY="your_google_api_key_here"
      ```

## Usage

To generate a video summary, run the `main.py` script from your terminal:

```bash
python main.py
```

You will be prompted to enter the YouTube video URL. Paste the URL and press Enter.

```
Enter the YouTube video URL: <your_youtube_url_here>
```

The agent will then process the video and save the report in the `reports/` directory. The report will be named with a timestamp, for example: `video-report-2025-08-17_14-30-00.txt`.
