# spotify-save-discover-weekly [![Save songs](https://github.com/RegsonDR/spotify-save-discover-weekly/actions/workflows/save.yaml/badge.svg)](https://github.com/RegsonDR/spotify-save-discover-weekly/actions/workflows/save.yaml) 

This script automatically saves your "Discover Weekly" playlist which is generated by Spotify and refreshed every Monday. The songs from your temporary playlist are saved into a permanent playlist, using the Spotify API ([Authorization Code Flow](https://developer.spotify.com/documentation/general/guides/authorization-guide/#authorization-code-flow)). The automation is powered by [Github Actions](https://docs.github.com/en/actions) and executes automatically on Mondays as defined in the [save.yaml](/.github/workflows/save.yaml).

## Initial Set Up (approx: 10 minutes)
You should not need to make any commits back to the repo. The files in [/setup](/setup) will help obtain the authorization information for setting up the environment variables in github secrets in order to allow `main.py` to execute properly. You need to fork this repo in order to have your own instance of github actions.

### (1) Create a Fork
Start off with simple fork by clicking on the "Fork" button. Once you've done that, you can use your favorite git client to clone your repo or use the command line:
```bash
# Clone your fork to your local machine
$ git clone https://github.com/<your-username>/spotify-save-discover-weekly.git
```

### (2) Librairies
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install all of the required librairies. You could use this with a [virtual environment](https://docs.python.org/3/library/venv.html) if required. 
```bash
$ pip install -r requirements.txt
```

### (3) Spotify API Credentials
1. Open the `.sample.env` file from the [/setup](/setup) folder on your local machine. 
2. Sign into your [Spotify API Dashboard](https://developer.spotify.com/dashboard/applications) and create a new application. You can use any uri for the redirect uri, this is the base uri you will be redirected to after authorizing the app to access your account. If you see a "INVALID_CLIENT: Invalid redirect URI", then edit settings of your app from the spotify dashboard and add your uri as a redirect uri.
3. Fill out the env file with the same Client ID, Secret and Redirect URI details used in step 2 and save this file as `.env`. **Do not post these details anywhere publically.**

Example:
```
CLIENT_ID=thisisanid
CLIENT_SECRET=thisisasecret
REDIRECT_URI=https://your.url/here
```
5. Execute [authorization.py](/setup/authorization.py) and open the URL generated. 
6. Authorize your app to access your Spotify account, this will then redirect you to your Redirect URI with a `?code=` parameter in the url.
7. Copy the whole url you were redirected to into the console and hit enter, this will then give you your refresh token. **Do not post this refresh token anywhere publically.**

Example:
 ```
$python authorization.py
Open this link in your browser: https://accounts.spotify.com/authorize?client_id=thisisanid&response_type=code&redirect_uri=https%3A%2F%2Fgithub.com%2FRegsonDR&scope=user-library-read+playlist-modify-public+playlist-modify-private+playlist-read-private+playlist-read-collaborative

Enter URL you was redirected to (after accepting authorization):
> https://your.url/here?code=somecodehere

Your refresh token is: somerefreshtokenhere
```

### (4) Github Actions
1. Go to the settings of your forked repo and click on secrets. 
2. You will need to create the following secrets:
  *  **CLIENT_ID** - Use the same Client ID from your `.env`.
  *  **CLIENT_SECRET** - Use the same Client Secret from your `.env`
  *  **REFRESH_TOKEN** - Use the refresh token generated in the [(3) Spotify API Credentials](#3-spotify-api-credentials) instructions above.
  *  **DISCOVER_WEEKLY_ID** - This is the ID of your Discover Weekly playlist, which can obtained using the [method](#obtaining-spotify-playlist-ids) described below.
  *  **SAVE_TO_ID** - This is the ID of your permanent playlist, which can be obtained using the [method](#obtaining-spotify-playlist-ids) described below. You will need to create a new playlist or use an existing playlist if there is somewhere you would like to already save the songs into.

![image](https://user-images.githubusercontent.com/32569720/113211160-0a7d3380-926d-11eb-97bc-0e17ef911336.png)

---

#### Obtaining Spotify Playlist IDs
1. Right click on a playlist > "Share" > Copy the Spotify URI (`spotify:playlist:c11M5VLWLMh66yW4gsl51S`). 
2. The ID is of this playlist is `c11M5VLWLMh66yW4gsl51S`, use this for the environment variable.

---

## Manual Execution via Github Actions
1. Go to Actions in your forked repo.
2. Click on "Save songs"
3. Click on "Run workflow" which will bring up a drop down menu.
4. Click on "Run Workflow" again, this will initiate the script. Within the next few minutes, the script should execute and your songs should be in your new playlist in spotify.

Any execution errors can be found from within the actions tab of your forked repo.

![image](https://user-images.githubusercontent.com/32569720/113211386-4fa16580-926d-11eb-94c9-ddb513a122a7.png)

## Local Execution 
Alternatively, you can store the **REFRESH_TOKEN**, **DISCOVER_WEEKLY_ID** & **SAVE_TO_ID** back into your `.env` file and execute `main.py` on your machine when required, maybe manually or using a task schedular. Make sure to have the `.env` and `main.py` files in the same directory for this.

 ```
$python main.py
```
---

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)
