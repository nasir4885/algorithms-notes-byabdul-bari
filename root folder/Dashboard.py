import streamlit as st
import json
import os

# Set page config
st.set_page_config(page_title="Algorithms Study Dashboard", layout="wide")

# Load the JSON data
def load_data():
    with open('Abdul Bari - Video List.json', 'r') as f:
        return json.load(f)

data = load_data()

st.title("🎓 Abdul Bari Algorithms - Study Tracker")
st.markdown("---")

# Sidebar for Navigation
st.sidebar.header("Course Progress")
completed = st.sidebar.multiselect("Mark as Completed", [v['Title'] for v in data])
progress = len(completed) / len(data)
st.sidebar.progress(progress)
st.sidebar.write(f"**Progress: {progress*100:.1f}%**")

# Main Dashboard Layout
col1, col2 = st.columns([1, 2])

with col1:
    st.header("Select Lesson")
    selected_title = st.selectbox("Choose a video:", [v['Title'] for v in data])
    
    # Find selected video data
    video = next(v for v in data if v['Title'] == selected_title)
    
    st.image(video['Thumbnail url'], use_container_width=True)
    st.write(f"**Duration:** {video['Duration']}")
    st.write(f"**Views:** {video['Views']:,}")

with col2:
    st.header(video['Title'])
    st.video(video['Video url'])
    
    with st.expander("Show Lesson Description"):
        st.write(video['Description'])
    
    # Note taking section
    st.subheader("Your Notes")
    user_notes = st.text_area("Write your insights here...", height=200, key=video['Title'])
    
    if st.button("Save Notes to GitHub"):
        # This creates a markdown file locally
        filename = f"notes/{video['Title'].replace(' ', '_')}.md"
        os.makedirs("notes", exist_ok=True)
        with open(filename, "w") as f:
            f.write(f"# {video['Title']}\n\n{user_notes}")
        st.success(f"Saved to {filename}!")