#download large files from external source
import os
import requests
import streamlit as st

def download_large_file_with_progress(remote_url, local_path, chunk_size=8192):
    """
    Downloads a large file from remote_url to local_path in chunks,
    displaying a progress bar in the Streamlit app.
    """
    response = requests.get(remote_url, stream=True)
    response.raise_for_status()

    total_size = int(response.headers.get('content-length', 0))
    progress_bar = st.progress(0)
    bytes_downloaded = 0

    with open(local_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=chunk_size):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
                bytes_downloaded += len(chunk)
                progress = bytes_downloaded / total_size if total_size else 1.0
                progress_bar.progress(min(progress, 1.0))

    st.success("App setup complete")