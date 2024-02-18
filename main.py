from utils.video_processing import process_video
import sys

if __name__ == '__main__':
    try:
        base_file = sys.argv[sys.argv.index('-f') + 1]
    except Exception as e:
        print(f'Usage: python main.py -f <path_to_video>\n{e}')
        sys.exit()

    try:
        filename = process_video(base_file)
    except Exception as e:
        print(f'Error processing video or file was not found\n{e}')

    print(f"Processed video: {filename}")
