# Standard imports
import io
from datetime import datetime

# Related third party imports
import pandas as pd
import streamlit as st

# Local application/library specific imports
from text_miner import api


class StreamLitView:
    def __init__(self):
        self.files = []

    def run(self):
        st.title("Text Miner")

        with st.form("upload_form", clear_on_submit=True):
            uploaded_files = st.file_uploader(
                "Upload PDF files", type="pdf", accept_multiple_files=True
            )

            submit_button = st.form_submit_button("Submit")

        if submit_button and uploaded_files:
            self.files = [(file.name, file.getvalue()) for file in uploaded_files]

            if self.files:
                results, errors = api.extract_text(self.files)

                for error in errors.values():
                    st.error(f"Oops! Something went wrong: {error}", icon="❌")

                self._download(results)
                self.files = []

    def _download(self, result: list[dict[str, str]]):
        if not result:
            return
        
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer) as writer:
            pd.DataFrame(result).sort_values("frequency", ascending=False).to_excel(
                writer, index=False
            )
        
        buffer.seek(0)
        
        filename = f"TextMiner_{datetime.now().strftime("%Y-%m-%dT%H-%M-%S-%fZ")}.xlsx"

        st.download_button(
            label="Download",
            data=buffer,
            file_name=filename,
        )



def main():
    view = StreamLitView()
    view.run()


if __name__ == "__main__":
    main()

