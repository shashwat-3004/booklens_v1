import os
from google import genai
import pandas as pd
import numpy as np
from PIL import Image
from pathlib import Path
from google.genai.types import FileState
from google.genai import types 
import streamlit as st
import io

from pydantic import BaseModel, Field

class BookInfo(BaseModel):
    title: str = Field(description="The title of the book")
    author: str = Field(description="The author of the book")
    year: int = Field(description="The year the book was published")
    genre: str = Field(description="The genre of the book")
    book_summary: str = Field(description="A brief summary of the book (max 200 words)")
    reviews: list[str] = Field(description="A list of reviews for the book")


def get_book_info(image=Image.Image, api_key=str) -> BookInfo | None:

    try:
        client=genai.Client(api_key=api_key)

    except Exception as e:
        st.error(f"Error initializing GenAI client: {e}")
        return None

    prompt_text = (
        "You are an expert literary analyst and book identifier. Your task is to analyze the "
        "user-provided image of a book cover and get structured information about the book. "
        "Do not guess. If a piece of information is not visible, use your knowledge base to provide "
        "it accurately. The final output must strictly adhere to the provided JSON schema."
    )

    model_name = "gemini-2.5-flash"

    config=types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=BookInfo)
    
    st.info("Generating book information...")

    try:
        response = client.models.generate_content(
            model=model_name,
            contents=[prompt_text, image],
            config=config)
    except Exception as e:
        st.error(f"API Call Error: An exception occurred during the API call: {e}")
        return None

    if response.parsed:
        return response.parsed
    else:
        st.error("AI Generation Failed: Received a non-structured or empty response.")
        st.code(response.text)
        return None
    
    


