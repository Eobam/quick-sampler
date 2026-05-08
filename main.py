#!/usr/bin/env python3
"""
YouTube to WAV downloader using yt-dlp
Downloads audio from YouTube URLs and saves them as .wav files in a "samples" folder.
"""

import os
import sys
import argparse
from pathlib import Path
import yt_dlp


def create_samples_folder():
    """Create the 'samples' folder if it doesn't exist."""
    samples_dir = Path("samples")
    samples_dir.mkdir(exist_ok=True)
    return samples_dir


def download_youtube_audio(urls, output_dir="samples"):
    """
    Download audio from YouTube URLs and save as WAV files.
    
    Args:
        urls (list): List of YouTube URLs to download
        output_dir (str): Directory to save WAV files (default: "samples")
    """
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Configure yt-dlp options
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [
            {
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
                'preferredquality': '192',
            }
        ],
        'outtmpl': str(output_path / '%(title)s.%(ext)s'),
        'quiet': False,
        'no_warnings': False,
    }
    
    successful = 0
    failed = 0
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for url in urls:
            try:
                print(f"\n📥 Downloading: {url}")
                info = ydl.extract_info(url, download=True)
                title = info.get('title', 'Unknown')
                print(f"✅ Successfully saved: {title}.wav")
                successful += 1
            except Exception as e:
                print(f"❌ Error downloading {url}: {str(e)}")
                failed += 1
    
    # Print summary
    print("\n" + "="*50)
    print(f"Download Complete!")
    print(f"✅ Successful: {successful}")
    print(f"❌ Failed: {failed}")
    print(f"📁 Saved to: {output_path.absolute()}")
    print("="*50)


def main():
    parser = argparse.ArgumentParser(
        description='Download YouTube videos as WAV audio files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python youtube_to_wav.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
  python youtube_to_wav.py "https://youtu.be/dQw4w9WgXcQ" "https://youtu.be/jNQXAC9IVRw"
  python youtube_to_wav.py -o audio_files "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        """
    )
    
    parser.add_argument(
        'urls',
        nargs='+',
        help='YouTube URL(s) to download'
    )
    
    parser.add_argument(
        '-o', '--output',
        default='samples',
        help='Output directory (default: samples)'
    )
    
    args = parser.parse_args()
    
    # Validate URLs
    if not args.urls:
        parser.print_help()
        sys.exit(1)
    
    # Download audio
    download_youtube_audio(args.urls, args.output)


if __name__ == '__main__':
    main()