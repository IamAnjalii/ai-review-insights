import streamlit as st
import os
from groq import Groq

# ---- PAGE TITLE ----
st.title("AI Customer Review Intelligence Tool")
st.write("Turn messy customer reviews into clear product insights.")

# ---- LOAD API KEY SECURELY ----
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("API key not found. Please set GROQ_API_KEY as an environment variable.")
    st.stop()

client = Groq(api_key=api_key)

# ---- REVIEW INPUT ----
reviews = st.text_area("Paste customer reviews (one per line, max 20)")

# ---- ANALYZE REVIEWS ----
if st.button("Analyze Reviews"):
    if not reviews.strip():
        st.warning("Please paste some reviews.")
    else:
        prompt = f"""
You are a product analyst. Analyze the customer reviews below and give structured product insights.

Reviews:
{reviews}

Please provide:
1. Top 5 Customer Pain Points
2. Top 5 Most Loved Features
3. Feature Requests or Missing Expectations
4. Overall Sentiment (Positive / Mixed / Negative + short reason)
5. What the Product Team Should Fix First (with reasoning)

Keep answers concise and in bullet points.
"""

        with st.spinner("Analyzing reviews..."):
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=500,
            )

            st.subheader("AI Product Insights")
            st.write(response.choices[0].message.content)
