import streamlit as st

from api.client import search_documents

def chat_interface():

    if "messages" not in st.session_state:

        st.session_state.messages = []

    st.header("💬 Ask Questions")

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.write(message["content"])


            if message["role"] == "assistant":

                if "sources" in message:

                    st.write("##### Evidence")

                    for source in message["sources"]:

                        st.write(
                            f"📄 {source['document']} (Page {source['page']})"
                        )

                        st.caption(
                            f"Source relevance: {source['relevance']}%"
                        )

                        with st.expander(
                            "Read supporting passage"
                        ):

                            st.write(
                                source["preview"]
                            )

    question = st.chat_input(
        "Ask about your uploaded documents..."
    )

    if question:
        st.session_state.messages.append(
            {
                "role": "user",
                "content": question,
            }
        )  

        if not question.strip():

            st.warning(
                "Please enter a question."
            )

            return

        with st.spinner(
            "Thinking..."
        ):

            result = search_documents(
                question
            )

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": result["answer"],
                "sources": result["sources"],
            }
        )


        st.rerun()

           