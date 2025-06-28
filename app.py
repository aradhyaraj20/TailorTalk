import streamlit as st
import requests

st.set_page_config(page_title="TailorTalk Booking Agent")
st.title("🧵 TailorTalk - AI Appointment Booking Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    st.chat_message(message["role"]).write(message["content"])

# User input
user_input = st.chat_input("Say something...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                res = requests.post(
                    "http://localhost:8000/chat",
                    json={"message": user_input}
                )

                # Validate response format
                if res.headers.get("Content-Type", "").startswith("application/json"):
                    data = res.json()
                    reply = data.get("response", "No 'response' key in JSON.")
                else:
                    reply = f"Error: Non-JSON response received:\n{res.text}"

            except requests.exceptions.RequestException as e:
                reply = f"❌ Request failed: {e}"
            except ValueError:
                reply = f"❌ Could not decode server response:\n{res.text}"

            st.write(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
