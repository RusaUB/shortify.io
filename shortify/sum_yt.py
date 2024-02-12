from youtube_transcript_api import YouTubeTranscriptApi
from openai import OpenAI
from shortify.config import API_KEY
import time

# Initialize the OpenAI client
client = OpenAI(api_key=API_KEY)

# Function to fetch YouTube transcript and generate a summary
def generate_summary_from_youtube_video(video_id):
    # Fetch YouTube transcript
    try:
        print("Fetching transcript...")
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        transcript = transcript_list.find_transcript(['en'])
        if transcript:
            transcript_text = ""
            for line in transcript.fetch():
                transcript_text += line['text'] + " "
            
            # Generate summary using ChatGPT
            print("Generating summary...")
            summary = generate_summary(transcript_text)
            return summary
        else:
            return "Transcript not found for the given video."
    except Exception as e:
        return f"Error fetching transcript: {e}"

# Function to generate a summary using ChatGPT
def generate_summary(prompt):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Summarize a text"},
            {"role": "user", "content": prompt}
        ]
    )
    return completion.choices[0].message.content

# Take video_id as input
def main():
    video_id = input("Enter the YouTube video ID: ")
    summary = generate_summary_from_youtube_video(video_id)
    print("\nSummary:")
    print(summary)

if __name__ == "__main__":
    main()
