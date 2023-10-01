from typing import Optional
import openai
from langchain import LLMChain, PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate
from langchain.schema import SystemMessage, HumanMessage

from prompts import system_prompt, user_information
# from secret_key import OPEN_API_KEY
from utils import read_pdf

def get_cover_letter_langchain_normal_prompts(
        openai_api_key: str,
        model: str,
        resume: Optional[str] = None,
        job_description: Optional[str] = None,
        additional_information: Optional[str] = None
) -> str:
    """
    Generate a cover letter using LangChain's LLM Chain and Prompt Template.

    Args:
        resume (Optional[str]): The content of the resume.
        job_description (Optional[str]): The content of the job description.
        openai_api_key (str): The API key for OpenAI.
        model (str): The model to be used.
        additional_information (Optional[str]): Additional information to include in the cover letter.

    Returns:
        str: The generated cover letter.
    """
    # Create an instance of the ChatOpenAI class
    llm = ChatOpenAI(
        model=model,
        temperature=0.2,
        openai_api_key=openai_api_key
    )

    # Define the prompt structure
    system_prompt = "Your system prompt here"
    user_information = f"Resume: {resume}\nJob Description: {job_description}\nAdditional Information: {additional_information}"
    prompt = system_prompt + "\n---\n" + user_information + "\n---\nCover Letter:"

    # Create a PromptTemplate instance from the prompt
    prompt_template = PromptTemplate.from_template(prompt)

    # Create an instance of the LLMChain class
    llm_chain = LLMChain(
        llm=llm,
        prompt=prompt_template
    )

    # Set default values if arguments are None
    resume = resume if resume is not None else "None"
    job_description = job_description if job_description is not None else "None"
    additional_information = additional_information if additional_information is not None else "None"
    
    # Define the arguments for the llm_chain.run method
    args = {
        "resume": resume,
        "job_description": job_description,
        "additional_information": additional_information
    }

    # Run the llm_chain to generate the cover letter
    return llm_chain.run(args)

