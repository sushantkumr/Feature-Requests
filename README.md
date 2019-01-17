# Feature-Requests
App to create Feature Requests for Clients

## Steps to deploy
1. Clone the repository in your local machine.	
2. Install the dependencies by executing `pip3 install -r requirements.txt` at the root level of the repo.
3. Initialize the database by executing `python3 lib/devops/init_db.py`
4. Run the server by executing `python3 server.py` at the root level of the repo.
5. Access the application at this URL: [http://0.0.0.0:5000](http://0.0.0.0:5000)
6. To run the tests run `python3 tests_feature_requests.py`

### Additional Features
1. Drag and drop option to reorder priorities.
2. Selectize feature to type and filter options in drop down inputs.

### Tech Stack
- Python 3.6
- Flask
- SQLAlchemy
- Bootstrap 3
- jQuery
