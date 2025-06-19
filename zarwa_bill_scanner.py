
import streamlit as st
from PIL import Image
import pytesseract

st.set_page_config(page_title="Zarwa Bill Scanner", layout="centered")
st.title("📄 Zarwa Bill Scanner (OCR + Total Calculator)")

st.markdown("Upload scanned bills (images), and this demo will extract the amount and calculate the total automatically.")

uploaded_files = st.file_uploader("Upload Bill Images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

total_amount = 0.0
bills = []

if uploaded_files:
    st.subheader("🧾 Extracted Bills:")
    for uploaded_file in uploaded_files:
        try:
            image = Image.open(uploaded_file)
            text = pytesseract.image_to_string(image)

            # Try to find the first number that looks like an amount
            amount = 0.0
            lines = text.splitlines()
            for line in lines:
                for word in line.split():
                    if word.replace(".", "", 1).isdigit():
                        amount = float(word)
                        break
                if amount:
                    break

            bills.append((uploaded_file.name, amount))
            total_amount += amount

            st.image(image, caption=uploaded_file.name, width=300)
            st.success(f"Extracted Amount from {uploaded_file.name}: SAR {amount:.2f}")

        except Exception as e:
            st.error(f"Failed to process {uploaded_file.name}: {e}")

    st.markdown("---")
    st.subheader("✅ Total Amount from All Bills:")
    st.write(f"💰 **SAR {total_amount:.2f}**")
else:
    st.info("Please upload one or more bill images to begin.")
