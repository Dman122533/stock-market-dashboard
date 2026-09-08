import streamlit as st

from src.ai.assistant import ask_financial_assistant


def render_ai_assistant():
    st.header("AI Financial Assistant")

    st.write(
        "Ask questions about stocks, investing concepts, "
        "portfolio metrics, and financial analysis."
    )

    if "ai_messages" not in st.session_state:
        st.session_state.ai_messages = []

    for message in st.session_state.ai_messages:
        with st.chat_message(message["role"]):

            display_message = (
                message["content"]
            .   replace("$", r"\$")
            )

        st.markdown(display_message)

    user_message = st.chat_input("Ask AI a question...")

    if user_message:
        st.session_state.ai_messages.append(
            {"role": "user", "content": user_message}
        )

        with st.chat_message("user"):
            st.markdown(user_message)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = ask_financial_assistant(user_message, user_id=st.session_state.user["id"])

            if response:
                display_response = response.replace("$", r"\$")
                st.markdown(display_response)
            else:
                st.error("The AI assistant did not return a response.")

            st.session_state.ai_messages.append(
                {"role": "assistant", "content": response}
            )