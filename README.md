# SE-Project

## Project Title
Lost-Found-Sell web application with object detection features

## Abstract
Trust is a major issue when it comes to purchasing a used good from an unknown, sometimes the product in advertisement is entirely different from the original one. Our web application verifies the legitimacy and extracts various features of the product from its uploaded picture using computer vision techniques, so that users can have a seamless experience in carrying out their desired actions. The application also handles lost/found based issues i.e posts of found objects are efficiently matched to the posts of lost objects by using computer vision techniques, and the users are notified once the quality match is found, thus saving them from going through the feed every minute. In order to speed up the process of finding the product our application uses reward system for the finders which they can later redeem, and the selection of the set of finders (one's who are interested) is carried out by using the current location of finders and the last found location of the lost object, and those finders are then notified. Issues (if raised) regarding the ownership of the lost objects is supposed to be solved by the finder (using extensive details provided in our application) and related parties.

## How to Run the Flask Server
1. Create a virtual environment (recommended)

2. Install the requirements: 
    ```
    pip install -r requirements.txt
    ```
3. Set environment variable `FLASK_APP=main.py`

4. Now run the server
   ```
   flask run --host=0.0.0.0
   ```
   
## How to Run Tests

* To run all tests :
    ```
    python -m unittest application.tests
    ```

* To run a single test Module, eg: 
    ```
    python -m unittest application.tests.LoginTests
    ```
  
* To run a single test, eg: 
    ```
    python -m unittest application.tests.LoginTests.test_user_login_form_displays
    ```
 