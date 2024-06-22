# resume-parser
The project is a resume parser for robota.ua and work.ua, designed to filter resumes based on keywords and score candidates according to specified parameters. Additionally, it includes a Telegram bot integrated with the parser for keyword-based candidate filtering.
## Features
*  Parsing: Capability to extract candidate data from robota.ua and work.ua websites.
* Keyword Filtering: Ability to screen resumes based on specific keywords or phrases.
* Candidate Scoring: Integration of additional scoring parameters to evaluate candidates.
* Telegram Integration: Development of a Telegram bot allowing users to search and filter candidates directly within chat.
##  Installation:
Python3 must be already installed

### 1.Clone the Repository:
```shell
git clone  https://github.com/svitlana-savikhina/resume-parserr.git
cd resume-parser
```

### 2.Activate venv:
```shell
python -m venv venv
source venv/bin/activate (Linux/Mac)
venv\Scripts\activate (Windows)
```
### 3.Install Dependencies:
```shell
pip install -r requirements.txt
```
### 4.Get Telegram notifications:
* Create bot using BotFather and get token as TELEGRAM_BOT_TOKEN
* Users can interact with the bot by initiating commands such as 

-/start to begin,

-/help for command listings, 

-/sites to select job search platforms, 

-/search to search candidates by keywords.
### 5.Environment Configuration: 
Create a .env file in the root directory with the following content, define environment variables in it (example you can find in .env_sample)

TELEGRAM_BOT_TOKEN=TELEGRAM_BOT_TOKEN
