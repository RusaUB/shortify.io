import cv2
import numpy as np
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

def download_video(video_url):
    """
    Download a video from YouTube.

    Args:
        video_url (str): The URL of the YouTube video.

    Returns:
        str: The path to the downloaded video file, or None if download fails.
    """
    try:
        # Download the video from YouTube
        youtube = YouTube(video_url)
        video = youtube.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        if video:
            video_path = f"video_{youtube.video_id}.mp4"
            video.download(filename=video_path, output_path='.')
            print("Video downloaded successfully.")
            return video_path
        else:
            print("No suitable video stream found.")
            return None
    except Exception as e:
        print("Error downloading video:", e)
        return None

def trim_video(video_path, start_time, end_time):
    """
    Trim a video to the specified time range.

    Args:
        video_path (str): The path to the input video file.
        start_time (float): The start time of the trimmed segment in seconds.
        end_time (float): The end time of the trimmed segment in seconds.
        output_path (str, optional): The path to save the trimmed video. Defaults to "trimmed_video.mp4".

    Returns:
        str: The path to the trimmed video file, or None if trimming fails.
    """
    try:
        # Trim the video to the specified time range
        output_path = f"trimmed_video.mp4"
        ffmpeg_extract_subclip(video_path, start_time, end_time, targetname=output_path)
        print("Video trimmed successfully.")
        return output_path
    except Exception as e:
        print("Error trimming video:", e)
        return None


def get_transcript(video_id, start_time, end_time):
    """
    Retrieve transcript for the specified time range.

    Args:
        video_id (str): The ID of the YouTube video.
        start_time (float): The start time of the transcript segment in seconds.
        end_time (float): The end time of the transcript segment in seconds.

    Returns:
        list: A list of tuples containing text and start time of each transcript line.
    """
    try:
        # Retrieve transcript for the specified time range
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        filtered_transcript = [(line['text'], line['start']) for line in transcript if line['start'] >= start_time and line['start'] <= end_time]
        return filtered_transcript
    except Exception as e:
        print("Error retrieving transcript:", e)
        return None

def add_transcript_to_video(video_path, transcript):
    """
    Add transcript to the video as captions.

    Args:
        video_path (str): The path to the input video file.
        transcript (list): A list of tuples containing text and start time of each transcript line.
    """
    try:
        # Open the trimmed video
        video_clip = VideoFileClip(video_path)

        # Resize the video to TikTok resolution (1080 x 1920 pixels)
        resized_clip = video_clip.resize(width=1280, height=720)   # Width comes first for vertical videos

        # Create text clips for each transcript line
        text_clips = [TextClip(text, fontsize=24, color='white', bg_color='black', method='caption', size=(resized_clip.w, None)).set_position('center').set_duration(end_time - start_time).set_start(start_time)
                      for text, start_time in transcript]

        # Composite text clips onto the video
        final_clip = CompositeVideoClip([resized_clip] + text_clips)

        # Write the final video with transcript
        final_clip.write_videofile("video_with_transcript_tiktok.mp4",audio_codec="aac", bitrate="5000k")

        # Close the video clips
        final_clip.close()
        print("Transcript added to TikTok resolution video successfully.")
    except Exception as e:
        print("Error adding transcript to TikTok resolution video:", e)


def edit_transcript(transcript):
    """
    Allow the user to edit the transcript.

    Args:
        transcript (list): A list of tuples containing text and start time of each transcript line.

    Returns:
        list: The edited transcript.
    """
    edited_transcript = []
    for text, start_time in transcript:
        print(f"Current text: {text}")
        new_text = input("Enter the corrected text (press Enter to keep original): ").strip()
        edited_transcript.append((new_text if new_text else text, start_time))
    return edited_transcript

if __name__ == "__main__":
    video_url = input("Enter the YouTube video URL: ")
    start_time = float(input("Enter the start time (in seconds): "))
    end_time = float(input("Enter the end time (in seconds): "))
    
    # Download the video from YouTube
    video_path = download_video(video_url)
    
    if video_path:
        # Trim the video to the specified time range
        trimmed_video_path = trim_video(video_path, start_time, end_time)
        
        if trimmed_video_path:
            # Get transcript for the specified time range
            video_id = YouTube(video_url).video_id
            transcript = get_transcript(video_id, start_time, end_time)
            
            if transcript:
                # Allow user to edit the transcript
                print("\nEditing transcript:")
                edited_transcript = edit_transcript(transcript)
                
                # Add transcript to the trimmed video
                add_transcript_to_video(trimmed_video_path, edited_transcript)
            else:
                print("Failed to retrieve transcript.")
        else:
            print("Failed to trim video.")
    else:
        print("Failed to download video.")
