from flask import Flask, request, url_for, session, redirect
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time

app = Flask(__name__)


app.secret_key = "slkansfa"
app.config['SESSION_COOKIE_NAME'] = 'Mason Drabik'
TOKEN_INFO = "token_info"

@app.route('/')
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/redirect')
def redirectPage():
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session["token_info"] = token_info
    return redirect(url_for('getArtists', _external=True))


@app.route('/getArtists')
def getArtists():
    try:
        token_info = get_token()
    except:
        print("user not logged")
        return redirect(url_for("login", _external=False))
    sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))
    all_artists = []
    for i in range(10): 
        item = sp.current_user_top_artists(time_range='long_term', limit=10)['items'][i]['name']
        #print(str(item))
        all_artists += str(item)
    return all_artists
  


def get_token():
    token_valid = False
    token_info = session.get("token_info", {})

    if not (session.get('token_info', False)):
        token_valid = False
        return token_info, token_valid

    now = int(time.time())
    is_token_expired = session.get('token_info').get('expires_at') - now < 1

    if (is_token_expired):
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(session.get('token_info').get('refresh_token'))

    token_valid = True
    return token_info, token_valid


@app.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect('/')

def create_spotify_oauth():
    return SpotifyOAuth(
        client_id = "a2f4b2f43ce949828d350c7d201876c1",
        client_secret = "f610f9ecb2984f80a36624aebda34090",
        redirect_uri= url_for('redirectPage', _external=True),
        scope="user-top-read"
    )


if __name__== '__main__':
    app.run()
