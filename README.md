![Made with love in Romania](https://madewithlove.now.sh/ro?heart=true)

# :space_invader: Code Session 

Code session is a web application made with Flask, python designed for Romanian students to compete with other people by solving informatics problems. After each solution is submitted, a "professor" (who has a administrator type account) has to review the code for each person and give points based on that. Each participant get awarded points, medals and thropies for representing either number of solutions submitted or number of wins.

## :gear: Installation

- Install python 3 (if not already installed). You can either install python by command line or from [here](https://www.python.org/downloads/)
- Install pip3

Make sure python3 and pip are installed by running `python3 --version` and `pip3 --version`

- Clone the repository `git clone https://github.com/alexmarginean16/codesession.git`
- Change directory to repo `cd codesession/`
- Create and activate a python3 virtualenv 
        
        python3 -m venv venv
        . /venv/bin/activate
        
- Install requirements `pip install -r requirements.txt`
- In `mongo_connect.py` Replace the API KEYS, DB URI/NAME, etc. listed below:

        twitter_blueprint = make_twitter_blueprint(api_key='', api_secret='')
        'RECAPTCHA_SITE_KEY': "",
        'RECAPTCHA_SECRET_KEY': ""
        app.config['MONGO_DBNAME'] = ''
        app.config['MONGO_URI'] = ''
        
- Run the application `python mongo_connect.py`
- The app is running on PORT 5000. Go to `http://127.0.0.1:5000`


## Contributors

    [![](https://sourcerer.io/fame/alexmarginean16/alexmarginean16/codesession/images/0)] 
   (https://sourcerer.io/fame/alexmarginean16/alexmarginean16/codesession/links/0)[![] 
   (https://sourcerer.io/fame/alexmarginean16/alexmarginean16/codesession/images/1)] 
   (https://sourcerer.io/fame/alexmarginean16/alexmarginean16/codesession/links/1)[![] 
   (https://sourcerer.io/fame/alexmarginean16/alexmarginean16/codesession/images/2)] 
   (https://sourcerer.io/fame/alexmarginean16/alexmarginean16/codesession/links/2)[![] 
   (https://sourcerer.io/fame/alexmarginean16/alexmarginean16/codesession/images/3)] 
   (https://sourcerer.io/fame/alexmarginean16/alexmarginean16/codesession/links/3)[![] 
   (https://sourcerer.io/fame/alexmarginean16/alexmarginean16/codesession/images/4)] 
   (https://sourcerer.io/fame/alexmarginean16/alexmarginean16/codesession/links/4)[![] 
   (https://sourcerer.io/fame/alexmarginean16/alexmarginean16/codesession/images/5)] 
   (https://sourcerer.io/fame/alexmarginean16/alexmarginean16/codesession/links/5)[![] 
   (https://sourcerer.io/fame/alexmarginean16/alexmarginean16/codesession/images/6)] 
   (https://sourcerer.io/fame/alexmarginean16/alexmarginean16/codesession/links/6)[![] 
   (https://sourcerer.io/fame/alexmarginean16/alexmarginean16/codesession/images/7)] 
   (https://sourcerer.io/fame/alexmarginean16/alexmarginean16/codesession/links/7)
