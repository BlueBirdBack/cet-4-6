"""Convert SRT file to transcript"""

import re
import argparse
import os
import spacy


def srt_to_transcript(srt_file_path, transcript_file_path, spacy_model):
    """Convert SRT file content to a transcript file"""
    with open(srt_file_path, "r", encoding="utf-8") as srt_file:
        srt_content = srt_file.read()

    # Regular expression to match and remove timestamps and sequence numbers
    cleaned_content = re.sub(
        r"\d+\s+\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}\s+", "", srt_content
    )

    # Remove remaining sequence numbers
    cleaned_content = re.sub(r"\n\d+\s*\n", "\n", cleaned_content)

    # Remove HTML tags like <i>, <b>, etc.
    cleaned_content = re.sub(r"<[^>]+>", "", cleaned_content)

    # Process the text with spaCy
    doc = spacy_model(cleaned_content)

    # Join sentences and remove extra newlines
    processed_text = "\n".join([sent.text for sent in doc.sents])

    # Write the cleaned content to the transcript file
    with open(transcript_file_path, "w", encoding="utf-8") as transcript_file:
        transcript_file.write(processed_text)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert SRT file to transcript")
    parser.add_argument("srt_file_path", help="Path to the SRT file")
    args = parser.parse_args()

    # Load spaCy model
    nlp = spacy.load("en_core_web_sm")

    output_file_path = os.path.splitext(args.srt_file_path)[0] + ".txt"
    srt_to_transcript(args.srt_file_path, output_file_path, nlp)

    print(f"Transcript saved to {output_file_path}")
