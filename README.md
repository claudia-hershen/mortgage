# Mortgage Calculator


## Required packages:
* Flask
* requests
* Python version 2.7

## Usage:
* To start the localhost server go to the main git folder and type: ```python main.py```.
* For testing purposes there are 4 wrapper routes. Each wrapper roure sends a hard coded json object named json_obj to the proccess routes.
* The four routes are:
  * http://127.0.0.1:5000/run/payment-amount
  * http://127.0.0.1:5000/run/mortgage-amount-full
  * http://127.0.0.1:5000/run/mortgage-amount-partial
  * http://127.0.0.1:5000/run/interest-rate
* In order to change the json object - change the json_obj param in blueprints/run_wrapper_blueprint.py as desired in order to test with other parameters.
* The json that is returned by each wrapper route will be displayed in the browser.
