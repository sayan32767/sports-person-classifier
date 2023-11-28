import streamlit as st
import util
import os
import glob
import json

_names = {}

def main():
    st.title("This App Can Recognize These Persons 👇")
    show_images()
    uploaded_file = st.file_uploader("Choose a file", type=['jpg', 'jpeg', 'png'])

    if uploaded_file is not None:
        st.write("File Details:")
        file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type, "FileSize": uploaded_file.size}
        st.write(file_details)

        # Copies file to current directory.
        uploaded_file_path = copy_to_current_directory(uploaded_file)
        classify_image(uploaded_file_path)

def show_images():
    image_paths = ['./images/' + str(file) for file in os.listdir('./images')]
   
    with open("./artifacts/class_dictionary.json", "r") as f:
        global _names
        _names = {str(v):k.replace('_', ' ').title() for k,v in json.load(f).items()}

    st.image(image_paths, width=140, caption=[_names[f"{name.split('/')[2].split('.')[0]}"] for name in image_paths])

def classify_image(uploaded_file_path):
    result = util.classify_image(uploaded_file_path)
    if result == []:
        st.title("Sorry! coundn't recognize this person!")
        return
    recog = result[0]['class']
    id = result[0]['class_dictionary'][recog]
    probab = max(result[0]['class_probability'])
    st.title(f"There is a {probab}% chance that the uploaded image is of 👇")
    st.image(f"./images/{id}.png", width=140, caption=[_names[str(id)]])

def copy_to_current_directory(uploaded_file):
    file_name = uploaded_file.name

    # Create a new file path in the current directory
    new_file_path = os.path.join(os.getcwd(), '.cache', file_name)

    # Clear cache
    files = glob.glob('./.cache/*')
    for f in files:
        os.remove(f)

    # Copy the file to the current directory
    with open(new_file_path, "wb") as f:
        f.write(uploaded_file.read())
    
    return new_file_path

if __name__ == "__main__":
    main()
