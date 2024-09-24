# app.py
import os
from flask import Flask, render_template, request, jsonify, session
from flask_caching import Cache
import lyricsgenius as lg
from dotenv import load_dotenv
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# Configure caching
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

# Configure rate limiting
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)

# Configure logging
logging.basicConfig(filename='app.log', level=logging.INFO)
api_key=os.getenv('GENIUS_API_KEY')
# LyricsGenius setup
genius = lg.Genius(api_key)
genius.remove_section_headers = True
genius.skip_non_songs = True

@cache.memoize(timeout=3600)
def get_lyrics(artist, song):
    try:
        song_info = genius.search_song(song, artist)
        if song_info:
            return song_info.lyrics

        else:
            return None
    except Exception as e:
        logging.error(f"Error fetching lyrics: {str(e)}")
        return None

@app.route('/', methods=['GET', 'POST'])
@limiter.limit("10 per minute")
def index():
    if request.method == 'POST':
        artist = request.form['artist']
        song = request.form['song']
        if not artist or not song:
            return render_template('index.html', error="Please enter both artist and song name")
        
        lyrics = get_lyrics(artist, song)
        if lyrics:
            session['lyrics'] = lyrics
            session['artist'] = artist
            session['song'] = song
            return render_template('index.html', lyrics=lyrics, artist=artist, song=song)
        else:
            return render_template('index.html', error="Lyrics not found. Please check the artist and song name.")
    
    return render_template('index.html')

@app.route('/api/lyrics', methods=['GET'])
@limiter.limit("30 per minute")
def api_lyrics():
    artist = request.args.get('artist')
    song = request.args.get('song')
    if not artist or not song:
        return jsonify({"error": "Please provide both artist and song parameters"}), 400
    
    song_info = get_lyrics(artist, song)
    if song_info:
        return jsonify(song_info)
    else:
        return jsonify({"error": "Lyrics not found"}), 404

@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify(error="Rate limit exceeded. Please try again later."), 429

if __name__ == '__main__':
    app.run()