import streamlit as st
import httpx
import asyncio

st.title("Resume Semantic Search")

query = st.text_input("Enter your search query:")

async def fetch_results(query):
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:3000/search", params={"query": query})
        return response

if st.button("Search"):
    if query:
        response = asyncio.run(fetch_results(query))
        if response.status_code == 200:
            results = response.json()
            for result in results:
                st.write(result['payload'])
        else:
            st.error("Failed to fetch results. Please try again.")
    else:
        st.warning("Please enter a search query.")
