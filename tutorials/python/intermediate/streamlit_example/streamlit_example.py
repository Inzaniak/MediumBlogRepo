import streamlit as st

text_to_parse = "Hello world this is a test! Goodbye world!"

def find_word(text, word):
    """Find every occurrence of a word inside a text"""
    # Find the first occurrence of the word
    index = text.lower().find(word)
    # Keep searching until all occurrences have been found
    while index != -1:
        yield index
        # Find the next occurrence of the word
        index = text.find(word, index + 1)
        
st.title('Word Finder')
st.markdown("## Find")
text = st.text_area("Text to parse", text_to_parse)
word = st.text_input("Word to find", "world")

if st.button("Find"):
    # Find all occurrences of the word
    result = list(find_word(text, word))
    # Show the results
    st.markdown("## Results")
    st.markdown(f"Found **{word}** {len(result)} times")
    st.write(result)