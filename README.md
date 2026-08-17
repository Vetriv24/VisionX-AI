# Vision X - VR Therapy AI

Vision X is a VR therapy AI assistant built with a Flask backend and a lightweight HTML/CSS/JavaScript frontend. It analyzes user trauma descriptions, detects the most relevant mental health condition, and generates a personalized virtual reality therapy schedule.

## 🚀 Features

- AI-driven therapy condition detection based on user input
- Personalized VR therapy schedules for anxiety, depression, PTSD, social anxiety, phobias, and stress
- Week-by-week session planning with immersive VR techniques
- Date selection and scheduling for therapy sessions
- Simple web interface with chat-style interaction and schedule preview

## 📁 Project Structure

- `app.py` - Flask backend with schedule generation and session scheduling endpoints
- `requirements.txt` - Python dependencies for the backend
- `index.html` - Frontend interface for user input and schedule display
- `script.js` - Frontend behavior, API calls, and schedule rendering
- `styles.css` - UI styling for the web interface

## ⚙️ Requirements

- Python 3.8+
- `pip`
- Web browser

## 📦 Installation

1. Open a terminal in `vr-therapy-ai`.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## ▶️ Run the App

1. Start the Flask backend:

```bash
python app.py
```

2. Serve the frontend files from the project folder.

Option A: Use a simple local server:

```bash
python -m http.server 5500
```

Then open:

```
http://localhost:5500/index.html
```

Option B: Open `index.html` directly in your browser. For best compatibility, use a local HTTP server.

## 🔧 Usage

1. Enter trauma details or describe your mental health concerns in the chat input.
2. Click `Send` to generate a personalized VR therapy schedule.
3. Pick dates using the calendar.
4. Click `Schedule Sessions` to map the generated sessions onto your selected dates.

## 🧠 Backend Endpoints

- `POST /generate-schedule`
  - Request body: `{ "trauma_details": "..." }`
  - Returns: generated therapy schedule, detected condition, and response message

- `GET /health`
  - Returns: health status

## 📝 Notes

- The backend uses condition keyword detection to pick the best therapy path.
- The generated schedule combines session descriptions, technique recommendations, and VR setup guidance.
- The frontend uses `fetch` to call the Flask API at `http://localhost:5000`.

## 💡 Suggestions

- Add support for additional VR therapy scenarios and immersive goals.
- Extend the app with user authentication and saved therapy plans.
- Improve model-based understanding by integrating a machine learning or NLP service.

## 📌 License

Feel free to add your preferred open source license when publishing on Git and GitHub.
