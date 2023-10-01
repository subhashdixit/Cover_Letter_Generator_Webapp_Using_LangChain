import os
import streamlit as st
from dotenv import load_dotenv
from llm_chain import get_cover_letter_langchain_normal_prompts
from utils import read_docx, write_string_to_word, read_pdf
# from secret_key import OPEN_API_KEY

load_dotenv()

chat_model_dict = {
    'LangChain Prompt Template': get_cover_letter_langchain_normal_prompts
}

def build_streamlit_app():

    st.set_page_config(
        page_title="Your Page Title",
        page_icon="✅",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Specify the static directory
    st.markdown(
        """
        <style>
        .reportview-container {
            background: url('static/background_image.jpg');
            background-size: cover;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Set the title of the Streamlit app to 'Cover Letter Generator'
    st.title('Cover Letter Generator using LangChain')

    # # Create an input box in the sidebar of the app for the OpenAI API key
    openai_api_key = None
    if openai_api_key is None:
        openai_api_key = st.sidebar.text_input('OpenAI API Key')
        st.sidebar.markdown("Visit [OpenAI's Website](https://www.openai.com/) to create your Open API key.")

    cover_letter_type = st.sidebar.selectbox(
        'Select the cover letter generation method',
        tuple(chat_model_dict.keys())
    )

    model = st.sidebar.selectbox(
        'Select the model you wish to use',
        (
            'gpt-3.5-turbo',
            'gpt-4'
        )
    )
    
    # Create a file uploader widget for uploading a document (the user's resume)
    allowed_file_types = ['txt', 'pdf', 'docx']
    resume = st.file_uploader("(Optional) Upload your Resume", type=allowed_file_types)
    resume_text = None
    
    # Taking Input for all the parameters 
    if resume is not None:
        # Check if the file type is allowed
        file_extension = resume.name.split('.')[-1].lower()
        if file_extension in allowed_file_types:
            if file_extension == 'docx':
                # For docx files
                resume_text = read_docx(resume)

            elif file_extension == 'pdf':
                # For pdf files (using PyMuPDF library)
                resume_text = read_pdf(resume)

            else:
                # For txt files
                resume_text = resume.read().decode('utf-8')

            # Display or process the resume_text as needed
            st.text(resume_text)
        else:
            st.warning(f"Invalid file type. Allowed types: {', '.join(allowed_file_types)}")


    # Create a text input area for pasting the company description
    job_description = st.text_area('(Optional) Paste the job description here')

    # Create a text input area for pasting any additional company information
    additional_information = st.text_area('(Optional) Paste additional company information here')

    # Create a button for generating the cover letter
    if st.button('Generate Cover Letter'):
        # Check if the OpenAI key, resume, and company description are provided
        if not openai_api_key or not openai_api_key.startswith('sk-'):
            # Display a warning if the OpenAI API key is not provided or is invalid
            st.warning('Please enter your correct OpenAI API key!', icon='⚠️')
        elif resume is None and not job_description and not additional_information:
            # Display a warning if the resume has not been uploaded
            st.warning('Please provide any of the information!', icon='⚠️')
        with st.spinner('Generating your cover letter...'):
            result = chat_model_dict[cover_letter_type](
                resume=resume_text,
                job_description=job_description,
                additional_information=additional_information,
                openai_api_key=openai_api_key,
                model=model
            )

        # Display a success message when the cover letter generation is completed
        st.success('Cover letter generation completed!')

        # Write the generated cover letter to the app
        st.write('**Your Generated Cover Letter:**')
        st.write(result)

        # Create a Word document
        write_string_to_word(result, filename="cover_letter.docx")
        # Create a download button for the cover letter document
        with open("cover_letter.docx", "rb") as file:
            btn = st.download_button(
                "Download Cover Letter",
                file,
                file_name="Cover_Letter.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )

if __name__ == '__main__':
    build_streamlit_app()