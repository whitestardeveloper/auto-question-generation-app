import nltk
nltk.download('punkt_tab')
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.lex_rank import LexRankSummarizer


def summarize_text(input_text):
    parser = PlaintextParser.from_string(input_text, Tokenizer("turkish"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, sentences_count=15)

    output_text = ''
    for sentence in summary:
        output_text += f"{sentence} "

    return output_text