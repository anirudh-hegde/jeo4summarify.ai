import unittest
from unittest.mock import patch, MagicMock
import jeoo


class Test_Jeoo(unittest.TestCase):

    @patch('jeoo.YouTubeTranscriptApi')
    def test_transcript_details(self, mock_youtube_api):
        mock_youtube_api.list_transcripts.return_value = [
            MagicMock(fetch=lambda: [{'text': 'Hey, whassup'}])
        ]

        youtube_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        result = jeoo.transcript_details(youtube_url)
        self.assertEqual(result,' Hey, whassup')

    @patch('jeoo.genai.GenerativeModel')
    def test_gen_gemini_content(self, mock_gen_model):
        mock_model_instance = mock_gen_model.return_value
        mock_model_instance.generate_content.return_value.text = 'This is a summary.'

        transcript_text = "This is a transcript"
        prompt = "Summarize the following: "
        result = jeoo.gen_gemini_content(transcript_text, prompt)
        self.assertEqual(result, 'This is a summary.')

    @patch('jeoo.st')
    @patch('jeoo.transcript_details')
    @patch('jeoo.gen_gemini_content')
    def test_main_video_summarizer(self, mock_gen_content, mock_transcript_details, mock_streamlit):
        mock_streamlit.sidebar.radio.return_value = 'Video Summarizer'
        mock_streamlit.text_input.return_value = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
        mock_streamlit.button.return_value = True

        mock_transcript_details.return_value = 'Mock transcript'
        mock_gen_content.return_value = 'Mock summary'

        jeoo.main()

        mock_transcript_details.assert_called_with('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
        mock_gen_content.assert_called_with('Mock transcript', jeoo.prompt)
        mock_streamlit.write.assert_called_with('Mock summary')

    @patch('jeoo.st')
    @patch('jeoo.GoogleTranslator')
    def test_main_text_translator(self, mock_translator, mock_streamlit):
        mock_streamlit.sidebar.radio.return_value = 'Text Translator'
        mock_streamlit.text_area.return_value = 'Wine'
        mock_streamlit.selectbox.side_effect = ['english', 'german']
        mock_streamlit.button.return_value = True

        mock_translator.return_value.translate.return_value = 'Wien'

        jeoo.main()

        mock_translator.return_value.translate.assert_called_with('Wine')
        mock_streamlit.container().write.assert_called_with('Wien')


if __name__ == '__main__':
    unittest.main()

