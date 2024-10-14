# app.py

import streamlit as st
from PIL import Image
import exifread
import numpy as np
import cv2
import matplotlib.pyplot as plt

# Function to extract EXIF data
def extract_exif_data(uploaded_file):
    try:
        # Read EXIF data
        with uploaded_file as f:
            tags = exifread.process_file(f)
            if not tags:
                return "No EXIF metadata found."
            exif_data = {tag: str(tags[tag]) for tag in tags}
            return exif_data
    except Exception as e:
        return f"Error extracting EXIF data: {str(e)}"

# Function for JPEG Ghost Detection
def detect_ghosts(image):
    # Convert to NumPy array
    img_array = np.array(image)

    # Convert RGB to BGR for OpenCV
    img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)

    # Process the image (e.g., detect ghosts)
    edges = cv2.Canny(img_array, 100, 200)

    # Create a figure for matplotlib
    fig, ax = plt.subplots()
    ax.imshow(edges, cmap='gray')
    ax.axis('off')  # Hide axes
    plt.tight_layout()  # Adjust layout to make room for the figure

    return fig

# Title and Logo
st.title("Digital Image Forensics Tool")
st.image("logo.jpg", width=200)

# Sidebar for navigation
st.sidebar.title("Navigation")
option = st.sidebar.selectbox("Select Analysis Type", ["EXIF Metadata Extraction", "JPEG Ghost Detection"])

# Image upload
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    
    if option == "EXIF Metadata Extraction":
        # EXIF Metadata Extraction
        st.subheader("EXIF Metadata")
        exif_data = extract_exif_data(uploaded_file)
        # Display EXIF data
        if isinstance(exif_data, dict):
            for key, value in exif_data.items():
                st.write(f"{key}: {value}")
        else:
            st.write(exif_data)

    elif option == "JPEG Ghost Detection":
        # JPEG Ghost Detection
        st.subheader("JPEG Ghost Detection Results")
        ghost_detection_results = detect_ghosts(image)
        st.pyplot(ghost_detection_results)
