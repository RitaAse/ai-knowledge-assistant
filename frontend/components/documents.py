import streamlit as st

from streamlit_autorefresh import st_autorefresh

from api.client import (
    get_documents,
    delete_document,
)


def document_list():

    documents = get_documents()


    if any(
        document["processing_status"] == "PROCESSING"
        for document in documents
    ):

        st_autorefresh(
            interval=3000,
            key="document_status_refresh",
        )

    if not documents:

        st.info(
            "No documents uploaded yet."
        )

        return


    for document in documents:

        st.write(
            f"📄 {document['filename']}"
        )

        st.write(
            f"Type: {document['file_type']}"
        )

        st.write(
            f"Size: {document['file_size']} bytes"
        )


        status = document[
            "processing_status"
        ]


        if status == "COMPLETED":

            st.success(
                "Ready ✅"
            )


        elif status == "PROCESSING":

            st.warning(
                "Preparing document..."
            )


        elif status == "FAILED":

            st.error(
                "Processing failed"
            )


        else:

            st.info(
                "Uploaded"
            )


        if st.button(
            "Delete",
            key=f"delete_{document['id']}",
        ):

            delete_document(
                document["id"]
            )

            st.rerun()


        st.divider()

