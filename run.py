import argparse
import sys

from application.main import run, stylize_video, list_styles
from application.config import DEFAULT_PORT


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')

    application_parser = subparsers.add_parser('application', help='Run the application')
    application_parser.add_argument('--port', type=int, help='port to run the GUI server on', default=DEFAULT_PORT)

    video_parser = subparsers.add_parser('video', help='Stylize a video file')
    video_parser.add_argument('--fg-style', help='style of the foreground', required=True)
    video_parser.add_argument('--bg-style', help='style of the background')
    video_parser.add_argument('--background', help='mode of segmentation', choices=[0, 1, 2], default=0)
    video_parser.add_argument('--scaling', help='downscale the video by a factor', type=int, default=1)
    video_parser.add_argument('infile', help='Video file to stylize')
    video_parser.add_argument('outfile', help='File to write result to')

    list_parser = subparsers.add_parser('list', help='list all available styles')

    args = parser.parse_args()

    sys.argv = [sys.argv[0]]

    if args.command == 'application':
        run(
            port=args.port
        )
    elif args.command == 'video':
        stylize_video(
            input_path=args.infile,
            output_path=args.outfile,
            fg_style=args.fg_style,
            background=args.background,
            scaling=args.scaling,
            bg_style=args.bg_style
        )
    elif args.command == 'list':
        print('The available styles are: ')
        for style in list_styles():
            print(' - ' + style)
    else:
        parser.print_usage()
    # stylize_video('in.mp4', 'out.avi')
