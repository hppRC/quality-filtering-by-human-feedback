import os
import json
import re
import streamlit as st
from datasets import load_dataset

import utils

MAX_EXAMPLES = 10000
os.makedirs('annotations', exist_ok=True)

if "examples" not in st.session_state:
    mc4 = load_dataset("mc4", "ja", split="train", streaming=True)

    examples = []
    for i, example in enumerate(mc4):
        if i >= 1000:
            break
        examples.append(example)
    st.session_state["examples"] = examples

# Check if index.txt exists and load it
if os.path.exists('index.txt'):
    with open('index.txt', 'r') as f:
        index = int(f.read())
else:
    index = 0

# Create annotations directory if it does not exist
if not os.path.exists('annotations'):
    os.makedirs('annotations')

# Determine current good and bad file indices
good_file_index = index // MAX_EXAMPLES
bad_file_index = index // MAX_EXAMPLES

# Check if good file exists and load it
good_file = f'annotations/good_{good_file_index}.jsonl'
if os.path.exists(good_file):
    with open(good_file, 'r') as f:
        good = [json.loads(line) for line in f]
else:
    good = []

# Check if bad file exists and load it
bad_file = f'annotations/bad_{bad_file_index}.jsonl'
if os.path.exists(bad_file):
    with open(bad_file, 'r') as f:
        bad = [json.loads(line) for line in f]
else:
    bad = []

st.session_state["index"] = index
st.session_state["good"] = good
st.session_state["bad"] = bad

if st.button("許せる"):
    st.session_state["good"].append(st.session_state["examples"][st.session_state["index"]])
    utils.save_jsonl(st.session_state["good"], good_file)
    if len(st.session_state["good"]) >= MAX_EXAMPLES:
        st.session_state["good"] = []
        good_file_index += 1
        good_file = f'annotations/good_{good_file_index}.jsonl'
    st.session_state["index"] += 1
    with open('index.txt', 'w') as f:
        f.write(str(st.session_state["index"]))

if st.button("低クオリティ"):
    st.session_state["bad"].append(st.session_state["examples"][st.session_state["index"]])
    utils.save_jsonl(st.session_state["bad"], bad_file)
    if len(st.session_state["bad"]) >= MAX_EXAMPLES:
        st.session_state["bad"] = []
        bad_file_index += 1
        bad_file = f'annotations/bad_{bad_file_index}.jsonl'
    st.session_state["index"] += 1
    with open('index.txt', 'w') as f:
        f.write(str(st.session_state["index"]))

x = st.session_state["examples"][st.session_state["index"]]
x0 = x['text'].replace('\n', '\n\n')
x1 = x['timestamp'].replace('\n', '\n\n')
x2 = x['url'].replace('\n', '\n\n')
st.markdown(f"<div style='max-width: 800px;'>{x0}</div>", unsafe_allow_html=True)
st.markdown(f"<div style='max-width: 800px;'>{x1}</div>", unsafe_allow_html=True)
st.markdown(f"<div style='max-width: 800px;'>{x2}</div>", unsafe_allow_html=True)
