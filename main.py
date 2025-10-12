from ai_summary_reviews import get_book_info
from PIL import Image
import streamlit as st


st.set_page_config(page_title="BookLens: AI Book Summary & Reviews", page_icon="📚",    layout="centered", 
    initial_sidebar_state="expanded")

st.title("📚 Book Lens: Instant Information")
st.markdown("Upload/Take a picture of a book cover to instantly get its summary, author, key themes and reviews.")

if 'GEMINI_API_KEY' in st.secrets:
    api_key = st.secrets['GEMINI_API_KEY']
    st.sidebar.success("🔑 API Key Loaded Securely!")
else:
    api_key = None
    st.error("🚨 API Key not found!")
radio_option = st.radio("Choose:", ["Use Camera :camera:", "Upload Image ⬇️"], horizontal=True)
if radio_option == "Upload Image ⬇️":
    image_file = st.file_uploader("Upload the book cover image...", type=["png", "jpg", "jpeg"])
else:
    image_file = st.camera_input("Take a picture of the book cover...")
    

if image_file and api_key:
    image = Image.open(image_file)
    st.image(image, caption='Book Cover Uploaded', use_container_width=True)

    # 3. Process Button
if st.button("Analyze Book"):
    if not api_key:
        st.error("Please enter your Gemini API Key in the sidebar.")
    else:
        with st.spinner("Talking to the Gemini Model..."):
                # Call the core logic function
            book_object = get_book_info(image, api_key)
                
            if book_object:
                st.success("Analysis Complete!")
                    
                    # 4. Display Results in a Clean Format
                st.header(f"📖 {book_object.title}")
                st.subheader(f"🖋️ {book_object.author}")
                    
                st.write(f"**Genre:** {book_object.genre} | **Published:** {book_object.year}")
                    
                st.markdown("---")
                    
                st.header("Quick Summary")
                st.write(book_object.book_summary)
                    
                st.header("Review")
                st.markdown(
                    "\n\n".join(
                        [f"- {review}" for review in book_object.reviews]
                    )
                )



