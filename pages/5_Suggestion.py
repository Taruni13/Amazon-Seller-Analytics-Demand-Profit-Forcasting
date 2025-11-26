import streamlit as st
from datetime import datetime
import pandas as pd
from pathlib import Path
from src.theme import add_custom_css

st.set_page_config(page_title="Suggestion", layout="wide")
add_custom_css()

st.title("Suggestions")
st.write("We welcome suggestions to improve the dashboard. Submit feedback below.")

with st.form("suggestion_form"):
    name = st.text_input("Your name")
    email = st.text_input("Email")
    suggestion = st.text_area("Suggestion / Feedback", height=200)
    send = st.form_submit_button("Submit")

if send:
    if not suggestion.strip():
        st.error("Please enter a suggestion before submitting.")
    else:
        out_dir = Path("data")
        out_dir.mkdir(parents=True, exist_ok=True)
        out_file = out_dir / "suggestions.csv"
        row = {
            "timestamp": datetime.utcnow().isoformat(),
            "name": name,
            "email": email,
            "suggestion": suggestion,
        }
        # Append to CSV (create if missing)
        if out_file.exists():
            df = pd.read_csv(out_file)
            df = df.append(row, ignore_index=True)
        else:
            df = pd.DataFrame([row])
        df.to_csv(out_file, index=False)
        st.success("Thanks — your suggestion was saved.")
        st.balloons()

# Show recent suggestions (admin view)
if st.checkbox("Show recent suggestions"):
    f = Path("data/suggestions.csv")
    if f.exists():
        df = pd.read_csv(f)
        st.dataframe(df.sort_values("timestamp", ascending=False).head(50))
    else:
        st.info("No suggestions submitted yet.")
