from moviepy.editor import VideoFileClip
from PIL import Image

def generate_thumbnail(video_path, output_path="thumb.jpg", time_in_seconds=5):
    # Load the video file
    with VideoFileClip(video_path) as video:
        # Get the frame at the specified time
        frame = video.get_frame(time_in_seconds)
        
        # Save the frame as an image
        img = Image.fromarray(frame)
        img.save(output_path)
        
        print(f"Thumbnail saved at {output_path}")
        return output_path
