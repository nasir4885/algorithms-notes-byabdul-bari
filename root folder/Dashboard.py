import streamlit as st
import json
import os
from datetime import datetime

# Set page configuration
st.set_page_config(page_title="Algorithms Study Dashboard", layout="wide")

# 1. Load the JSON data
def load_data():
    with open('Abdul Bari - Video List.json', 'r', encoding='utf-8') as f:
        return json.load(f)

try:
    data = load_data()
except FileNotFoundError:
    st.error("JSON file not found. Ensure 'Abdul Bari - Video List.json' is in the root folder.")
    st.stop()

# 2. Smart Template Generator
# This makes the draft "better" by creating structure based on the lesson type
def generate_smart_template(title, description):
    # Base structure
    template = f"## 📖 Lesson Overview\n{description}\n\n"
    
    # Template for Complexity & Analysis
    if any(x in title for x in ["Complexity", "Analysis", "Notation"]):
        template += "## 📈 Complexity Analysis\n"
        template += "- **Worst Case (Big Oh):** $O()$\n"
        template += "- **Best Case (Omega):** $\Omega()$\n"
        template += "- **Average Case (Theta):** $\Theta()$\n\n"
        template += "### Frequency Count Table\n"
        template += "| Statement | Frequency | Time |\n| :--- | :--- | :--- |\n| `line_1` | 1 | $O(1)$ |\n\n"
    
    # Template for Sorting and Searching
    elif any(x in title for x in ["Sort", "Search", "Algorithm"]):
        template += "## ⚙️ Algorithm Logic\n"
        template += "- **Strategy:** (e.g., Divide & Conquer)\n"
        template += "- **Logic Steps:** \n  1. \n  2. \n\n"
        template += "### Python Implementation\n```python\n# Implementation for " + title + "\n\n```\n\n"
    
    # Generic section for insights
    template += "## 💡 Key Takeaways\n* \n* \n"
    template += f"\n---\n*Notes generated during Master's in AI & Data Science session on {datetime.now().strftime('%Y-%m-%d')}*"
    return template

# 3. Sidebar
st.sidebar.header("🎓 Course Progress")
completed = st.sidebar.multiselect("Mark as Completed", [v['Title'] for v in data])
if len(data) > 0:
    progress = len(completed) / len(data)
    st.sidebar.progress(progress)
    st.sidebar.write(f"**Overall Progress: {progress*100:.1f}%**")

# 4. Main UI
st.title("📚 Abdul Bari Algorithms - Study Tracker")
st.markdown("---")

col1, col2 = st.columns([1, 2])

with col1:
    st.header("Select Lesson")
    selected_title = st.selectbox("Choose a video:", [v['Title'] for v in data])
    video = next(v for v in data if v['Title'] == selected_title)
    
    st.image(video['Thumbnail url'], use_container_width=True)
    st.write(f"⏱ **Duration:** {video['Duration']}")
    st.write(f"👁 **Views:** {video['Views']:,}")
    
    with st.expander("Watch Original Description"):
        st.write(video['Description'])

with col2:
    st.header(video['Title'])
    st.video(video['Video url'])
    
    st.markdown("---")
    
    # 5. Smart Study Notes Area
    st.subheader("📝 Study Notes")
    
    # Generate the draft dynamically
    smart_draft = generate_smart_template(video['Title'], video['Description'])
    
    # The note box is now pre-filled with the smart draft
    user_notes = st.text_area(
        "Edit and refine your insights below:", 
        value=smart_draft, 
        height=500, 
        key=f"note_{video['Title']}"
    )
    
    if st.button("Save Notes to GitHub Folder"):
        notes_dir = "notes"
        os.makedirs(notes_dir, exist_ok=True)
        
        # Format filename
        clean_title = video['Title'].replace(" ", "_").replace("/", "-").replace(".", "_")
        file_path = os.path.join(notes_dir, f"{clean_title}.md")
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"# {video['Title']}\n\n{user_notes}")
        
        st.success(f"✅ Saved to `{file_path}`! Use Git to push to GitHub.")