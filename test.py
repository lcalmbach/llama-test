import time
import numpy as np
import pandas as pd
import streamlit as st

_LOREM_IPSUM = """
1. Lorem ipsum dolor sit amet, 
2. consectetur adipiscing elit, sed do eiusmod tempor
3. incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis
4. nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
"""


def stream_data():
    for word in _LOREM_IPSUM.split():
        yield word + " "
        time.sleep(0.02)

    yield pd.DataFrame(
        np.random.randn(5, 10),
        columns=["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"],
    )

    for word in _LOREM_IPSUM.split():
        yield word + " "
        time.sleep(0.02)


if st.button("Stream data"):
    st.markdown(stream_data)