import re
import argparse
import os


def srt_to_transcript(srt_file_path, transcript_file_path):
    with open(srt_file_path, "r", encoding="utf-8") as srt_file:
        srt_content = srt_file.read()

    # # Regular expression to match and remove timestamps and sequence numbers
    cleaned_content = re.sub(
        r"\d+\n\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}\n", "", srt_content
    )

    # Remove remaining sequence numbers
    cleaned_content = re.sub(r"\n\d+\n", "\n", cleaned_content)

    # Write the cleaned content to the transcript file
    with open(transcript_file_path, "w", encoding="utf-8") as transcript_file:
        transcript_file.write(cleaned_content)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert SRT file to transcript")
    parser.add_argument("srt_file_path", help="Path to the SRT file")

    args = parser.parse_args()

    # transcript_file_path = args.srt_file_path + ".txt"
    transcript_file_path = os.path.splitext(args.srt_file_path)[0] + ".txt"
    srt_to_transcript(args.srt_file_path, transcript_file_path)

    print(f"Transcript saved to {transcript_file_path}")
