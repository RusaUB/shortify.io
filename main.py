from youtube_transcript_api import YouTubeTranscriptApi

def get_video_transcript(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        return transcript_list
    except Exception as e:
        print("Error:", e)
        return None

def get_frames_from_transcript(transcript):
    frames = {}
    for line in transcript:
        start = line['start']
        duration = line['duration']
        end = start + duration
        text = line['text']
        frames[text] = (start, end)
    return frames

if __name__ == "__main__":
    video_id = input("Enter the YouTube video ID: ")
    transcript = get_video_transcript(video_id)
    if transcript:
        print("Transcript:")
        for line in transcript:
            print(line['text'])
        
        frames = get_frames_from_transcript(transcript)
        print("\nFrames:")
        for word, frame in frames.items():
            print("Word:", word, "Start:", frame[0], "End:", frame[1])
    else:
        print("Failed to retrieve transcript.")
