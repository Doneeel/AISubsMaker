from utils.video_processing import process_video
import moviepy.editor as mp
import sys

if __name__ == '__main__':
    try:
        base_file = sys.argv[sys.argv.index('-f') + 1]
    except:
        print('Usage: python main.py -f <path_to_video>')
        sys.exit()

    try:
        filename = process_video(base_file)
    except:
        print('Error processing video or file was not found')
                
    print(f"Processed video: {filename}")

