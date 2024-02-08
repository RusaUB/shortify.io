from youtube_transcript_api import YouTubeTranscriptApi


def get_video_transcript(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = ""
        for line in transcript_list:
            transcript += line['text'] + " "
        return transcript
    except Exception as e:
        print("Error:", e)
        return None

if __name__ == "__main__":
    video_id = input("Enter the YouTube video ID: ")
    transcript = get_video_transcript(video_id)
    if transcript:
        print("Transcript:")
        print(transcript)
    else:
        print("Failed to retrieve transcript.")
