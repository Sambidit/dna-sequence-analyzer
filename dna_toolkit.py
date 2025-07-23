import streamlit as st
import matplotlib.pyplot as plt
from collections import Counter

# -------------------------------
# DNA Tools
# -------------------------------

def clean_dna(seq):
    return seq.upper().replace(" ", "").replace("\n", "")

def gc_content(seq):
    gc_count = seq.count('G') + seq.count('C')
    return round((gc_count / len(seq)) * 100, 2)

def reverse_complement(seq):
    complement = {'A':'T', 'T':'A', 'G':'C', 'C':'G'}
    return ''.join(complement[base] for base in reversed(seq))

def transcribe(seq):
    return seq.replace("T", "U")

def kmer_count(seq, k=3):
    return dict(Counter(seq[i:i+k] for i in range(len(seq)-k+1)))

# -------------------------------
# Streamlit UI
# -------------------------------

st.title("🧬 DNA Sequence Analyzer")
st.markdown("Upload a **.txt file** or paste DNA sequence manually:")

# File upload
uploaded_file = st.file_uploader("Upload DNA file", type=["txt"])

if uploaded_file:
    dna = uploaded_file.read().decode("utf-8")
else:
    dna = st.text_area("...or paste your DNA sequence here:", height=150)

if st.button("Analyze"):
    if not dna:
        st.warning("Please upload or paste a DNA sequence.")
    else:
        seq = clean_dna(dna)

        if not all(base in "ATGC" for base in seq):
            st.error("Invalid sequence: Use only A, T, G, and C.")
        else:
            st.success("✅ DNA Analysis Complete")

            st.markdown(f"**Length:** {len(seq)} bases")
            st.markdown(f"**GC Content:** {gc_content(seq)}%")
            st.markdown(f"**Reverse Complement:** `{reverse_complement(seq)}`")
            st.markdown(f"**Transcribed RNA:** `{transcribe(seq)}`")

            k = st.slider("Choose k for k-mer analysis", 1, 6, 3)
            kmer_freq = kmer_count(seq, k)

            st.markdown("### 🔢 k-mer Frequencies:")
            st.json(kmer_freq)

            # Plot
            st.markdown("### 📊 k-mer Frequency Plot")
            fig, ax = plt.subplots()
            ax.bar(kmer_freq.keys(), kmer_freq.values(), color="skyblue")
            plt.xticks(rotation=45)
            plt.xlabel("k-mers")
            plt.ylabel("Frequency")
            st.pyplot(fig)
