import streamlit as st
import matplotlib.pyplot as plt
from collections import Counter

# Utility Functions

def format_sequence(seq):
    return seq.upper().replace("\n", "").replace(" ", "")

def calculate_gc_content(seq):
    if not seq:
        return 0
    gc = seq.count('G') + seq.count('C')
    return round((gc / len(seq)) * 100, 2)

def get_reverse_complement(seq):
    mapping = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    return ''.join([mapping[n] for n in reversed(seq)])

def transcribe_dna(seq):
    return seq.replace('T', 'U')

def compute_kmers(seq, k):
    return dict(Counter(seq[i:i+k] for i in range(len(seq) - k + 1)))

# Streamlit Interface

st.title("🧬 DNA Sequence Toolkit")
st.caption("Analyze DNA sequences directly in your browser.")

file_input = st.file_uploader("Upload a .txt file containing DNA sequence", type=["txt"])

if file_input:
    sequence = file_input.read().decode("utf-8")
else:
    sequence = st.text_area("Or paste your DNA sequence below:", height=150)

if st.button("Run Analysis"):
    if not sequence.strip():
        st.warning("Please provide a DNA sequence to analyze.")
    else:
        cleaned = format_sequence(sequence)

        if not set(cleaned).issubset({'A', 'T', 'C', 'G'}):
            st.error("Sequence contains invalid characters. Only A, T, G, C are allowed.")
        else:
            st.success("Analysis complete.")
            st.write(f"**Total Length:** {len(cleaned)} bases")
            st.write(f"**GC Content:** {calculate_gc_content(cleaned)}%")
            st.code(get_reverse_complement(cleaned), language='text', line_numbers=False)
            st.write("**RNA Transcription:**")
            st.code(transcribe_dna(cleaned), language='text')

            k_val = st.slider("Select k-mer size", min_value=1, max_value=6, value=3)
            kmer_result = compute_kmers(cleaned, k_val)

            st.subheader("k-mer Frequencies")
            st.json(kmer_result)

            st.subheader("k-mer Bar Chart")
            fig, ax = plt.subplots()
            ax.bar(kmer_result.keys(), kmer_result.values(), color="#1f77b4")
            ax.set_xlabel("k-mers")
            ax.set_ylabel("Count")
            plt.xticks(rotation=45)
            st.pyplot(fig)
