import streamlit as st
import cv2
import numpy as np
import base64
import zlib
from PIL import Image
import io

st.title("Complex QR Code Scanner")

uploaded_image = st.file_uploader("Choose an image", type=["png", "jpg", "jpeg"])

if uploaded_image is not None:
    # Read the image into a numpy array first
    image_stream = io.BytesIO(uploaded_image.read())
    file_bytes = np.asarray(bytearray(image_stream.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)
    
    # Display the image
    st.image(img, caption="Uploaded Image", use_column_width=True, channels="BGR")
    
    # Add a button to scan the QR Code
    if st.button("Scan QR Code"):
        # Detect QR code
        qr_code_detector = cv2.QRCodeDetector()
        val, pts, qr_code = qr_code_detector.detectAndDecode(img)

        if val == "":
            st.write("No QR Code detected")
        else:
            # Attempt to decode as base64
            try:
                base64_bytes = base64.b64decode(val)
                decompressed_data = zlib.decompress(base64_bytes).decode('utf-8')
                st.write(f"Stored Information in QR Code (Base64 and zlib Decoded): {decompressed_data}")
            except Exception as e:
                st.write(f"Could not decode the base64/zlib string. Raw text: {val}")
