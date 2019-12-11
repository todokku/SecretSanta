# Optimal Secret Santa
Go to http://optimal-secret-santa.herokuapp.com/ and have fun!

<!--
@Ken put a screenshot of the website and group creation here
-->

**Optimal Secret Santa** is a simple web application that allows a group of at least 3 people to generate gift exchange assignments.  
**Features**
* No account registration required! Just provide the names and emails of each member
* No spam! We encrypt and store your emails, and will never send you unnecessary emails (unlike some online Secret Santa apps...)
* Automatically emails each person their gift assignment (who to give to)
* Lets each member send a message, such as a wishlist, to the email of their Secret Santa without knowing who they are
* Each member's Secret Santa remains anonymous, you can't use math to guess who your Secret Santa is
* You will never be assigned to yourself
* If A is giving a gift to B, we won't generate a pairing where B is also giving to A

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See **Deployment** for notes on how to deploy the project on a live system.

### Prerequisites

The minimum requirements are `python-3.7.5` and `pip`.
The required packages are in `requirements.txt`.

### Installing

Clone the repository to your computer.

```
git clone https://github.com/benleone90/OptimalSecretSanta.git
```
Install `virtualenv` to create a Python virtual environment in this directory.
```
python -m pip install --user virtualenv
python -m venv venv
```
(**Optional**) Update your `venv` to the latest supported version of `python`.
```
python -m venv --upgrade YOUR_VENV_PATH
```
Activate the virtual environment then install all the requirements.
```
source venv/bin/activate
pip install -r requirements.txt
```
You will need to edit the environmental variables to the email account you are using. The `SECRET_KEY` will be used for the unique url token generation.
In `app.py`:
```
MAIL_USERNAME='put_your_email@address.com',
MAIL_PASSWORD='your_password',
SECRET_KEY='your_secret_key',
```
To run the website locally,
```
flask run
```
then navigate to http://localhost:5000/ or wherever the Flask website is running.

## Deployment

To deploy this app on Heroku, follow the instructions on how to [Deploy A Python Web App on Heroku](https://gist.github.com/bradtraversy/0029d655269c8a972df726ed0ac56b88).

## Built With

* [Flask](https://palletsprojects.com/p/flask/) - The web framework used
* [SQLAlchemy](https://www.sqlalchemy.org/) - Database toolkit
* [Heroku](https://www.heroku.com/) - Cloud hosting platform

## Authors

* **Ben Leone** - *Front End Development* - [benleone90](https://github.com/benleone90)
* **John Wiley Hunt** - *Email API* - [whunt1965](https://github.com/whunt1965)
* **Josh Goldberg** - *Database Engineer* - [jdg555666](https://github.com/jdg555666)
* **Ken Krebs** - *Front End Design* - [ken-krebs](https://github.com/ken-krebs)
* **Panat Taranat** - *Back End and Algorithm* - [ptaranat](https://github.com/ptaranat)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Acknowledgments

* [John Mikulskis](https://github.com/jkulskis)
* [Miguel Mark](https://github.com/mmark9)
* [Doug Densmore](https://github.com/ddensmore)
