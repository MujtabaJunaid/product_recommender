import streamlit as st
from graph import graph

st.title("Product Recommendation System")

product_query = st.text_input("Enter product (e.g., 'Sony WH-1000XM5 headphones'):")

if st.button("Analyze"):
    with st.spinner("Processing..."):
        result = graph.invoke({"product_query": product_query})
        
        st.subheader("Results")
        st.metric("Recommendation", result["recommendation"])
        st.metric("Sentiment Score", f"{result['sentiment_score']:.2f}")
        
        st.subheader("Video Summaries")
        for summary in result["summaries"]:
            with st.expander(summary['title']):
                st.write(summary['summary'])