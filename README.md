# LyricScope

LyricScope is an  web application that allows users to search for and display song lyrics. Built with Flask.
## Features

- Lyrics search powered by the Genius API
- Caching for improved performance
- Rate limiting to prevent abuse
- Error handling and logging
- RESTful API endpoint for lyrics retrieval

## Tech Stack

- Backend: Flask
- Frontend: HTML5, CSS3 (Tailwind CSS), JS
- APIs: Genius API for lyrics
- Additional libraries: GSAP for animations, Axios for AJAX requests

## Setup and Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/lyricscope.git
   cd lyricscope
   ```

2. Set up a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Fill in the required values in `.env`

5. Run the application:
   ```
   python main.py
   ```

6. Open your browser and navigate to `http://localhost:5000`

## API Usage

LyricScope provides a simple API endpoint for retrieving lyrics:

```
GET /api/lyrics?artist=<artist_name>&song=<song_name>
```



##