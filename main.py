from youtube_transcript_api import YouTubeTranscriptApi
from openai import OpenAI
from config import API_KEY

# Initialize the OpenAI client
client = OpenAI(api_key=API_KEY)

# Function to retrieve the transcript for a YouTube video
def get_video_transcript(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        return transcript_list
    except Exception as e:
        print("Error:", e)
        return None

# Function to generate a summary using ChatGPT
def generate_summary(prompt):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Generate only one important frame of duration of 12second max from the transcript return only and only in this format (strat_frame - last_frame)"},
            {"role": "user", "content": prompt}
        ]
    )
    return completion.choices[0].message.content

def get_frames_from_transcript(transcript):
    frames = []
    for line in transcript:
        start = line['start']
        duration = line['duration']
        end = start + duration
        text = line['text']
        frames.append((text, (start, end)))
    return frames

if __name__ == "__main__":
    video_id = input("Enter the YouTube video ID: ")
    transcript = get_video_transcript(video_id)
    
    if transcript:
        # Get frames and time intervals from the transcript
        frames_with_time = get_frames_from_transcript(transcript)

        # Combine frames and time intervals into the prompt variable
        prompt = ""
        for frame, time_interval in frames_with_time:
            prompt += f"{frame} (Start: {time_interval[0]}, End: {time_interval[1]})\n"

        # Generate a summary using ChatGPT
        important_frames = generate_summary(prompt)
        print(important_frames)
    else:
        print("Failed to retrieve transcript.")
