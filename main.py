import streamlit as st
from datasets import load_dataset

import utils

if "examples" not in st.session_state:
    mc4 = load_dataset("mc4", "ja", split="train", streaming=True)

    examples = []
    for i, example in enumerate(mc4):
        if i >= 1000:
            break
        examples.append(example)
    st.session_state["examples"] = examples

index = st.session_state.get("index", 0)
x = st.session_state["examples"][index]

good = st.session_state.get("good", [])
bad = st.session_state.get("bad", [])


if st.button("許せる"):
    good.append(st.session_state["examples"][st.session_state["index"] - 1])
    st.session_state["good"] = good
    utils.save_jsonl(good, "good.jsonl")
    st.session_state["index"] = index + 1

if st.button("低クオリティ"):
    bad.append(st.session_state["examples"][st.session_state["index"] - 1])
    st.session_state["bad"] = bad
    utils.save_jsonl(bad, "bad.jsonl")
    st.session_state["index"] = index + 1


st.write(x["text"])
st.write(x["timestamp"])
st.write(x["url"])
st.session_state["index"] = index + 1
