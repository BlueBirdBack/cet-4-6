"""Filter out CET-4 and CET-6 vocabulary, along with more advanced words, from a transcript"""

import os
import re
import argparse
import spacy


def lemmatize_words(words, nlp):
    """Lemmatize a list of words using a spacy model."""
    doc = nlp(" ".join(words))
    return {token.lemma_.lower() for token in doc}


def load_word_list(file_path, nlp):
    """Load and lemmatize word list from a file."""
    with open(file_path, "r", encoding="utf-8") as f:
        words = set()
        for line in f:
            split_words = re.split(r"[ /]+", line.strip())
            words.update(word.lower() for word in split_words if word.isalpha())
    return lemmatize_words(list(words), nlp)


def tokenize_text(text, nlp):
    """Tokenize and lemmatize text using spacy model to handle contractions."""
    doc = nlp(text)
    # return [
    #     token.lemma_
    #     for token in doc
    #     if token.text not in nlp.Defaults.stop_words and token.is_alpha
    # ]
    return [
        token.lemma_.lower()
        for token in doc
        if token.text.lower() not in nlp.Defaults.stop_words
        and token.is_alpha
        and len(token.text) >= 3
    ]


def main(input_file):
    """Load and process input file, filtering out words."""
    nlp = spacy.load("en_core_web_sm")

    current_dir = os.path.dirname(__file__)
    parent_dir = os.path.dirname(current_dir)
    words_dir = os.path.join(parent_dir, "words")

    cet_4_words = load_word_list(os.path.join(words_dir, "cet_4_words.txt"), nlp)
    cet_6_words = load_word_list(os.path.join(words_dir, "cet_6_words.txt"), nlp)

    print(f"Number of lemmatized CET-4 words: {len(cet_4_words)}")
    print(f"Number of lemmatized CET-6 words: {len(cet_6_words)}")

    with open(input_file, "r", encoding="utf-8") as f:
        input_text = f.read()

    lemmatized_words = set(tokenize_text(input_text.lower(), nlp))

    cet_4_set = {word for word in lemmatized_words if word in cet_4_words}
    cet_6_set = {word for word in lemmatized_words if word in cet_6_words}
    advanced_words = lemmatized_words - cet_4_set - cet_6_set

    print("More advanced words (not in CET-4 or CET-6):")
    print(f"Total: {len(advanced_words)}")
    for word in sorted(advanced_words):
        print(word)

    print("\nCET-6 words:")
    print(f"Total: {len(cet_6_set)}")
    for word in sorted(cet_6_set):
        print(word)

    print("\nCET-4 words:")
    print(f"Total: {len(cet_4_set)}")
    for word in sorted(cet_4_set):
        print(word)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="List CET-4 and CET-6 words used in a .txt file"
    )
    parser.add_argument("input_file", help="Input .txt file")
    args = parser.parse_args()
    main(args.input_file)
