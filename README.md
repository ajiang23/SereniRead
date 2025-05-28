# SereniRead

**An AI-powered reading companion** that helps users discover books, filter out unwanted content, and get instant summaries.

![image](https://github.com/user-attachments/assets/17782909-304c-4603-9f80-b2d64ef5c68c)

---

## Project Overview

SereniRead gives readers control and clarity:

1. **Content Warnings**  
   Users add custom “content warning” keywords (e.g. violence, abuse).  
   Books whose metadata contain any warning are hidden in real time.

2. **Theme Filtering**  
   Browse by one or more themes (Fantasy, Mystery, Self-Help, etc.).  
   Tags on each book card update instantly as you toggle themes.

3. **AI Summaries**  
   Click “Generate Summary” on any book to see a one-click synopsis powered by an AI backend.  
   Helps readers decide which book to pick up next.

---

## Key Features

- **Start Page**: Choose themes, add content warnings, enter a search term, then click **Search**.  
- **Theme Filters**: Multi-select genre buttons; selected tags show on both controls and book badges.  
- **Content Warnings**: Add keywords to flag; warning tags appear in yellow; toggle hide/show.  
- **AI Synopsis**: Generate in-page summaries with a single click; styled with a calming gradient box.

---

## Tech Stack & Architecture

- **Frontend**  
  - React (v19.x) & Bootstrap 5  
  - Axios for HTTP calls  
  - Custom CSS with variables, gradients, and Google Fonts (Roboto + Playfair Display)  
- **Backend (prototype)**  
  - FastAPI (Python)  
  - Integrates Google Books API + OpenAI API  

---

## APIs & Integrations

- **Google Books API** for book metadata (titles, authors, images, categories)  
- **OpenAI API** for on-demand AI-generated summaries  
- **Client-side content-warning logic** for instant filtering  

---

## Getting Started Locally

### Prerequisites  
- Node.js ≥ 16 & npm  
- Python ≥ 3.8 & pip  

### 1. Clone the repo  
```
git clone https://github.com/ajiang23/SereniRead.git
cd SereniRead
```

### 2. Backend setup
```
cd backend
python -m venv venv
source venv/bin/activate      for mac/linux
(or: venv\Scripts\activate    for Windows)
pip install -r requirements.txt
uvicorn main:app --reload

Once Uvicorn is running, open your browser to:
API root: http://localhost:8000
Interactive docs: http://localhost:8000/docs
```
### 3. Frontend setup
```
cd ../frontend
npm install
npm start                       

Once it’s running, open your browser to:
http://localhost:3000

The React app will read REACT_APP_API_BASE_URL from .env and send its requests there (default: http://localhost:8000).
```

## Dependencies
- axios — HTTP client
- bootstrap — UI framework
- react, react-dom, react-scripts — Core UI
- fastapi, uvicorn — Python API server
- openai — AI integration

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Built with ❤️ by Alicia Jiang
