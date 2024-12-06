import streamlit as st
import openai
import json
import pandas as pd
import io

# Get the API key from the sidebar called OpenAI API key
user_api_key = st.sidebar.text_input("OpenAI API key", type="password")
client = openai.OpenAI(api_key=user_api_key)

prompt = """ You are a language analysis assistant. You will receive a 
            passage. Analyze each word from the following English passage. Choose only beneficial words.List them and return in JSON,
            in json array has 2 fields.
            1. 'Words' : For each word has 4 fields:
            - 'Word' : English word
            - 'Translation' : Thai translation
            - 'Part of speech' : Noun, Verb, Adjective, Adverb, etc.
            - 'Difficulty level' : Easy, Medium, Hard

            2. 'Example Sentences': list of example sentences from words in passage.Each sentence for each word. Has 2 fields :
            - 'English' : English sentence
            - 'Thai' : The Thai sentence translated from English sentence
            
            Don't say anything at first. Wait for the user to say something.
        """    


st.title('English Vocabulary Analyzer')

user_input = st.text_area("Enter some text : ", "Your text here")


# submit button after text input
if st.button('Submit'):
    messages_so_far = [
        {"role": "system", "content": prompt},
        {'role': 'user', 'content': user_input},
    ]
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages_so_far
    )
    # Show the response from the AI in a box
    st.markdown('**AI response:**')
    st.empty() 
    st.markdown('**Vocabulary Table:**')

    suggestion_dictionary = response.choices[0].message.content
    print(suggestion_dictionary)

    sd = json.loads(suggestion_dictionary)

    
    print (sd)
    suggestion_df = pd.DataFrame.from_dict(sd['Words'])
    print(suggestion_df)
    st.table(suggestion_df)

    st.empty() 
    st.markdown('**Example Sentences:**')
    index = 1
    for sentence in sd['Example Sentences']:

        st.markdown(f"{index}. {sentence['English']}")
        st.markdown(f"  {sentence['Thai']}")
        index += 1


    
    st.empty()


   # Convert DataFrame to CSV format
    csv_data = suggestion_df.to_csv(index=False, encoding='utf-8-sig')  # index=False to avoid row indices

    # Create the download button
    st.download_button(
        label="Download Vocabulary CSV", 
        data=csv_data,
        file_name="data.csv", 
        mime="text/csv"
    )

