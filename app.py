import streamlit as st

# NLP
import spacy
nlp = spacy.load('en_core_web_sm')
from spacy import displacy
HTML_WRAPPER = """<div style="overflow-x: auto; border: 1px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem">{}</div>"""

# summary pkgs
from gensim.summarization import summarize
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

def sumy_summarizer(docx):
    parser = PlaintextParser.from_string(docx, Tokenizer("english"))
    lex_summarizer = LexRankSummarizer()
    summary = lex_summarizer(parser.document,3)
    summary_list = [str(sentence) for sentence in summary]
    result = ' '.join(summary_list)
    return result

# nlp function
# @st.cache(allow_output_mutation=True)
def analyze_text(text):
    return nlp(text)

from bs4 import BeautifulSoup
from urllib.request import urlopen

@st.cache
def get_text(raw_url):
    page = urlopen(raw_url)
    soup = BeautifulSoup(page)
    fetched_text = " ".join(map(lambda p:p.text,soup.find_all('p')))
    return fetched_text

# web scrapping pkgs
def main():
    """
    Summary and Entity Checker
    """

    st.title("Sumanalyzer")

    activities = ["Summarizer", "Name Checker", "URL Analyzer"]
    choice = st.sidebar.selectbox("Select Activity", activities)

    if choice == "Summarizer":
        st.subheader("Summarize and analyze your text")
        raw_text = st.text_area("Paste Your Text Here")
        summary_choice = st.selectbox('Summary Choice', ['Gensim', 'Lex Rank'])
        # summary_length = st.slider("Length of summary to extract", 50, 100)
        if st.button("Summarize"):
            if summary_choice == "Gensim":
                summary_result = summarize(raw_text)
            elif summary_choice == "Lex Rank":
                summary_result = sumy_summarizer(raw_text)
            # len_of_summary = round(len(summary_result)/summary_length)
            # st.write(summary_result[:len_of_summary])
            st.write(summary_result)


    if choice == "Name Checker":
        st.subheader("Check your text entity")
        raw_text = st.text_area('Paste Your Text Here')
        if st.button("analyze"):
            #nlp
            docx = analyze_text(raw_text)
            html = displacy.render(docx, style='ent')
            html = html.replace('\n\n','\n')
            st.write(html, unsafe_allow_html=True)

    if choice == "URL Analyzer":
        st.subheader("Extract Text From URL")
        raw_url = st.text_input('Paste Your URL Here', 'Paste Here')
        text_length = st.slider("Length of words to extract", 50, 100)
        if st.button("Extract"):
            if raw_url != 'Paste Here':

                result = get_text(raw_url)
                len_of_full_text = len(result)
                len_of_short_text = round(len(result)/text_length)
                st.info("Length::Full Text::{}".format(len_of_full_text))
                st.info("Length::Short Text::{}".format(len_of_short_text))
                st.write(result[:len_of_short_text])
                summary_docx = sumy_summarizer(result)
                docx = analyze_text(summary_docx)
                html = displacy.render(docx, style='ent')
                html = html.replace('\n\n','\n')
                st.write(html, unsafe_allow_html=True)


if __name__ == '__main__':
    main()
