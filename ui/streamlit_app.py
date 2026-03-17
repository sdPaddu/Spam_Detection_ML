import streamlit as st
import requests

st.title("📩 Spam Detection App")

message = st.text_input("Enter SMS Message")

if st.button("Predict"):

    if message.strip() == "":
        st.warning("Please enter a message")
    else:
        url = "https://spam-detection-api-k6xp.onrender.com/predict"

        try:
            response = requests.post(url, json={"text": message})

            if response.status_code == 200:
                result = response.json()

                if result["prediction"] == "Spam":
                    st.error("🚨 This message is SPAM")
                else:
                    st.success("✅ This message is HAM (Not Spam)")

            else:
                st.error(f"API Error: {response.text}")

        except Exception as e:
            st.error(f"Server not reachable: {e}")