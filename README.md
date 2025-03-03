# 📷 MemoVision a Conversational Memory Bot – AI-Powered Photo Gallery Assistant

## 📝 Project Overview

Conversational Memory Bot is an AI-powered chatbot that helps users interact with their personal photo galleries using natural language. The system allows users to query, retrieve, and explore their photos using textual descriptions and visual features.

## 🎯 Core Functionalities

- **📖 Natural Language Querying**: Users can ask questions like *"Show me photos of a dog playing in the park"* or *"Find pictures from my trip to Italy in 2021."*
- **🖼️ Contextual Image Retrieval**: The bot retrieves relevant photos based on semantic understanding of queries.
- **📝 Image Descriptions**: Generates detailed captions for selected images.
- **🔍 Visual Similarity Search**: Finds images visually similar to a selected one based on color, objects, and scene similarity.
- **🏷️ Automatic Tagging (Optional)**: Tags images with keywords like *"beach"*, *"sunset"*, or *"dog"*, for easier searching.

## 🏛️ Folder Structure

30177_memovision/

    │── memovision_backend/ 
        │── app/  
            ├── main.py 
            │── constants.py
            │── models.py
            │── question.csv
            │── .env 
            ├── api/ 
                │──  gallery.py
                │── query.py
                │── upload.py
                │── viewer.py
            ├── chroma_db_storage/ 
            │── images/
                │── uploaded_images/
                │── new_folder/
            │── services/
                │── ask_llama.py
                │── delete_image.py
                │── filtering_query_results.py
                │── handling_images.py
                │── ques_category.py
                │── vectordb.py

        │── project_venv/ # Virtual environment 
        │── multimodal_rag.ipynb # Notebook for R&D 
        │── requirements.txt # Backend dependencies  

    │── memovision_frontend/
        │── src/ 
            ├── components/
                │── BatchUploader.jsx
                │── ChatBot.jsx
                │── Gallery.jsx 
                │── Homepage.jsx 
                │── ImageViewer.jsx 
                │── Navbar.jsx
            ├── assets/ 
            │── api.js
            │── App.jsx
            │── index.css
            │── main.jsx
        │── public/ 
        │── node_modules/ 
        │── .idea/  
        │── package.json 
        │── index.html
        │── postcss.config.js
        │── tailwind.config.js 
        │── vite.config.js 
    │── README.md 



## 🔧 Technologies Used

### Backend (FastAPI)
- **🧠 NLP & AI**: Vision-based Large Language Models (LLMs), CLIP embeddings
- **📂 Database**: ChromaDB (for image-text retrieval)
- **🖥️ Backend Framework**: FastAPI
- **🖼️ Image Processing**: Multimodal Retrieval-Augmented Generation (RAG)

### Frontend (React)
- **💻 UI Framework**: React.js
- **🎨 Styling**: TailwindCSS
- **📜 State Management**: React Hooks
- **📸 Image Viewer**: Custom gallery components

## 🚀 Features Breakdown

| Feature                 | Description |
|-------------------------|------------|
| 📖 **Natural Language Querying** | Users can search for images using natural language. |
| 🖼️ **Contextual Image Retrieval** | Retrieves relevant images using embeddings and similarity search. |
| 📝 **Image Descriptions** | Generates detailed captions for selected images. |
| 🔍 **Visual Similarity Search** | Finds images visually similar to a selected one. |
| 🏷️ **Automatic Tagging (Optional)** | AI-based image tagging for better organization. |

## 🏗️ System Workflow

1. **User Query** 🗣️ → User asks for images using natural language.
2. **Query Processing** 🧠 → NLP model interprets the query and extracts embeddings.
3. **Image Retrieval** 🖼️ → The system finds the most relevant images based on text-image similarity.
4. **RAG Pipeline** 🔄 → The retrieved images are enriched with AI-generated descriptions.
5. **Output Display** 🎨 → Results are shown in an interactive image gallery.

## 📜 Installation & Setup

### 🔹 Backend Setup (FastAPI)
```
cd memovision_backend
python -m venv project_venv
project_venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 🔹 Frontend Setup (React)
```
cd memovision_frontend
npm install react-router-dom @fortawesome/react-fontawesome @fortawesome/free-solid-svg-icons @fortawesome/free-regular-svg-icons @fortawesome/free-brands-svg-icons
npm install -D tailwindcss@3.3 postcss autoprefixer
npx tailwindcss init -p
npm run dev

```

## Deliverables

📜 SRS, WBS
🌐 Web UI (Pages: Homepage, Gallery, Batch Image Uploader, Image Viewer, Chat)
🎤 Presentation (PPT)
💻 Codebase (GitHub Repository)
