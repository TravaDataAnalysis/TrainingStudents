# MongoDB Course

- Training:
  - Use [crud_with_mongodb_shell.md](crud_with_mongodb_shell.md) to interact with MongoDB through MongoDB Shell.
  - Use [crud_with_pymongo.py](crud_with_pymongo.py) to interact with MongoDB through Python.
    - How to run:
      - Prerequisites:
        - mongodb is installed, example on host: *localhost*, port: *27017*
        - create a readwrite user, example username: *admin*, password: *admin123*
      - Copy file [.env.example](.env.example) to .env and change to:
        ```
        MONGODB_HOST=localhost
        MONGODB_PORT=27017
        MONGODB_USERNAME=admin
        MONGODB_PASSWORD=admin123
        ```
      - Install dependencies:
        - Create venv (optional)
        - Run `pip3 install -r requirements.txt`
      - Run file [crud_with_pymongo.py](crud_with_pymongo.py):
        - `python3 crud_with_pymongo.py`
- Test:
  - Write MongoDB query to answer 20 tasks in file [crud_with_mongodb_shell.md](crud_with_mongodb_shell.md).
  - Write a file like [crud_with_pymongo.py](crud_with_pymongo.py) to answer 20 tasks in the file [crud_with_mongodb_shell.md](crud_with_mongodb_shell.md).