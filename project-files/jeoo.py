import google.generativeai as genai
import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from deep_translator import GoogleTranslator
import time

# import the api-key from config.py
genai.configure(api_key=st.secrets["API_KEY"])
prompt = """You are Youtube video summarizer. Your task is to take the transcript
        text from a youtube video and create a concise summary, highlighting the key points
        in no more than 250 words. Please provide the summary for following text here:  """

st.set_page_config(
    page_title="Jeo4Summarizer.ai",
    page_icon="🦾",
)


def transcript_details(youtube_video_url):
    try:
        vid_id = youtube_video_url.split("=")[1]

        transcript_list = YouTubeTranscriptApi.list_transcripts(vid_id)

        result = ""
        for transcript in transcript_list:
            fetched_transcript = transcript.fetch()
            for item in fetched_transcript:
                result += ' ' + item['text']
        return result
    except Exception as e:
        raise e


def gen_gemini_content(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt + transcript_text)

    return response.text


def main():
    st.sidebar.title('Navigation')

    pages = st.sidebar.radio("Go to", ['About', 'Video Summarizer', 'Text Translator'])

    if pages == "About":
        st.markdown(
            """
            <div style="text-align:center;">
            <h1>Jeo4Summarify.ai 🦾</h1>
            <h3 style="margin-top: 20px; margin-bottom: 20px";>Revolutionizing the way you consume content by summarizing 
                and translating videos for maximum efficiency and accessibility.
            </h3>
            
            <p>Jeo4Y is an innovative project designed to revolutionize the way users consume
               YouTube content. This advanced tool leverages cutting-edge AI technologies to 
               summarize lengthy Youtube videos and translate the summarized text into multiple
               languages, making information more accessible and time-efficient for a global audience.
            </p>  
                     
            </div>
            """,
            unsafe_allow_html=True,

        )
        st.snow()
        st.markdown("####")
        st.markdown(
            """
            <div style="text-align: center;" class="footer">
                Made with 💛️ by Anirudh
            </div>
            """,
            unsafe_allow_html=True
        )

    if pages == "Video Summarizer":
        st.subheader("Summarize your video")
        youtube_link = st.text_input("Enter the YouTube Video Link:")

        if youtube_link:
            video_id = youtube_link.split("=")[1]
            st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

        if st.button("Get Summary"):
            with st.spinner('summarizing the video...'):
                time.sleep(22)
            transcript_text = transcript_details(youtube_link)

            if transcript_text:
                summary = gen_gemini_content(transcript_text, prompt)
                st.markdown("## Summary:")
                st.write(summary)

    elif pages == "Text Translator":
        Languages = {
            'afrikaans': 'af', 'albanian': 'sq', 'amharic': 'am', 'arabic': 'ar', 'armenian': 'hy', 'azerbaijani': 'az',
            'basque': 'eu', 'belarusian': 'be', 'bengali': 'bn', 'bosnian': 'bs', 'bulgarian': 'bg', 'catalan': 'ca',
            'cebuano': 'ceb', 'chichewa': 'ny', 'chinese (simplified)': 'zh-cn', 'chinese (traditional)': 'zh-tw',
            'corsican': 'co', 'croatian': 'hr', 'czech': 'cs', 'danish': 'da', 'dutch': 'nl', 'english': 'en',
            'esperanto': 'eo', 'estonian': 'et', 'filipino': 'tl', 'finnish': 'fi', 'french': 'fr', 'frisian': 'fy',
            'galician': 'gl', 'georgian': 'ka', 'german': 'de', 'greek': 'el', 'gujarati': 'gu', 'haitian creole': 'ht',
            'hausa': 'ha', 'hawaiian': 'haw', 'hebrew': 'he', 'hindi': 'hi', 'hmong': 'hmn', 'hungarian': 'hu',
            'icelandic': 'is', 'igbo': 'ig', 'indonesian': 'id', 'irish': 'ga', 'italian': 'it', 'japanese': 'ja',
            'javanese': 'jw', 'kannada': 'kn', 'kazakh': 'kk', 'khmer': 'km', 'korean': 'ko',
            'kurdish (kurmanji)': 'ku',
            'kyrgyz': 'ky', 'lao': 'lo', 'latin': 'la', 'latvian': 'lv', 'lithuanian': 'lt', 'luxembourgish': 'lb',
            'macedonian': 'mk', 'malagasy': 'mg', 'malay': 'ms', 'malayalam': 'ml', 'maltese': 'mt', 'maori': 'mi',
            'marathi': 'mr', 'mongolian': 'mn', 'myanmar (burmese)': 'my', 'nepali': 'ne', 'norwegian': 'no',
            'odia': 'or', 'pashto': 'ps', 'persian': 'fa', 'polish': 'pl', 'portuguese': 'pt', 'punjabi': 'pa',
            'romanian': 'ro', 'russian': 'ru', 'samoan': 'sm', 'scots gaelic': 'gd', 'serbian': 'sr', 'sesotho': 'st',
            'shona': 'sn', 'sindhi': 'sd', 'sinhala': 'si', 'slovak': 'sk', 'slovenian': 'sl', 'somali': 'so',
            'spanish': 'es', 'sundanese': 'su', 'swahili': 'sw', 'swedish': 'sv', 'tajik': 'tg', 'tamil': 'ta',
            'telugu': 'te',
            'thai': 'th', 'turkish': 'tr', 'turkmen': 'tk', 'ukrainian': 'uk', 'urdu': 'ur', 'uyghur': 'ug',
            'uzbek': 'uz',
            'vietnamese': 'vi', 'welsh': 'cy', 'xhosa': 'xh', 'yiddish': 'yi', 'yoruba': 'yo', 'zulu': 'zu'
        }

        st.subheader("Enter the summarized text to translate")
        text = st.text_area("Enter the text: ", height=None, max_chars=None, key=None, help="Enter your text here")
        lang_list = list(Languages.keys())
        input_language = st.selectbox('Source language', lang_list, index=lang_list.index('english'))
        output_language = st.selectbox('Target language', lang_list, index=lang_list.index('german'))

        source_lang = Languages[input_language]
        target_lang = Languages[output_language]

        if st.button('Translate Sentence'):
            if text == "":
                st.warning('**Enter the text** for translation please')
            else:
                try:
                    translate = GoogleTranslator(source_lang, target_lang).translate(text)
                    st.markdown("---")
                    st.container(border=True).write(translate)
                except Exception as e:
                    st.error(f"An error occurred: {e}")
        else:
            pass

if __name__ == "__main__":
    main()
