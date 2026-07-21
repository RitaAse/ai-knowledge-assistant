import streamlit as st

from api.client import get_document
from streamlit_autorefresh import st_autorefresh


def document_status_tracker():

    document_id = st.session_state.get(
        "uploaded_document_id"
    )


    if not document_id:
        return


    document = get_document(
        document_id
    )

    if document is None:

        del st.session_state[
            "uploaded_document_id"
        ]
    

        return

    if document["processing_status"] in [
        "UPLOADED",
        "PROCESSING",
    ]:
        st_autorefresh(
            interval=3000,
            key="status_refresh",
        )


    status = document[
        "processing_status"
    ]


    st.subheader(
        document["filename"]
    )


    if status == "UPLOADED":

        st.info(
            "Document received..."
        )


    elif status == "PROCESSING":

        st.warning(
            "Preparing document..."
        )


    elif status == "COMPLETED":

        st.success(
            "Document ready ✅"
        )


    elif status == "FAILED":

        st.error(
            "Document processing failed."
        )