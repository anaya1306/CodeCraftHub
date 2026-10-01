CodeCraftHub is a beginner-friendly learning course tracker built with Python and Flask.

The application provides a REST API for creating, viewing, updating, and deleting courses. Course information is stored in a simple
courses.json
file instead of a database.

This project is designed to help beginners learn:

Flask basics
REST API concepts
HTTP methods
JSON request and response data
CRUD operations
Error handling
Reading and writing files with Python
Features
Create a new course
View all courses
View one course by ID
Update an existing course
Delete a course
Automatically generate numeric course IDs
Automatically record course creation timestamps
Validate required fields
Validate target dates
Validate course statuses
Store data in a local JSON file
Automatically create
courses.json
if it does not exist
Return helpful JSON error messages
Handle file read and write errors
Technologies Used
Python 3
Flask
JSON
curl
for API testing
No database is required.

Course Fields
Each course contains the following fields:

Field	Description
id
Automatically generated numeric ID
name
Course name
description
Course description
target_date
Target completion date in
YYYY-MM-DD
format
status
Course progress status
created_at
Automatically generated creation timestamp
The allowed status values are:

Not Started
In Progress
Completed
Example course:

{
  "id": 1,
  "name": "Flask REST API Fundamentals",
  "description": "Learn how to build REST APIs with Python and Flask.",
  "target_date": "2026-12-31",
  "status": "Not Started",
  "created_at": "2026-10-01T12:00:00+00:00"
}
The exact
created_at
value depends on when the course is created.

Installation
1. Check that Python is installed
Open a terminal or command prompt and run:

python --version
On some systems, you may need to use:

python3 --version
You should see a Python version such as:

Python 3.11.5
Python 3.8 or newer is recommended.

2. Clone or download the project
If the project is hosted in a Git repository, clone it with:

git clone https://github.com/your-username/codecrafthub.git
Move into the project directory:

cd codecrafthub
If you downloaded a ZIP file, extract it and open a terminal inside the extracted project folder.

3. Create a virtual environment
A virtual environment keeps this project's Python packages separate from other projects.

Windows
python -m venv venv
Activate it:

venv\Scripts\activate
macOS or Linux
python3 -m venv venv
Activate it:

source venv/bin/activate
After activation, your terminal may show
(venv)
at the beginning of the command prompt.

4. Install Flask
Install Flask with:

pip install flask
If your system uses
pip3
, run:

pip3 install flask
You can also create a
requirements.txt
file with:

Flask
Then install the dependencies with:

pip install -r requirements.txt
Running the Application
1. Activate the virtual environment
If it is not already active, activate it.

Windows
venv\Scripts\activate
macOS or Linux
source venv/bin/activate
2. Start the Flask application
Run:

python app.py
On macOS or Linux, you may need:

python3 app.py
You should see output similar to:

 * Running on http://127.0.0.1:5000
 * Debug mode: on
The API is now available at:

http://127.0.0.1:5000
Keep this terminal window open while testing the API.

3. Stop the application
To stop the Flask application, press:

Ctrl+C
API Overview
The base URL is:

http://127.0.0.1:5000
The API uses the following endpoints:

Method	Endpoint	Description
POST
/api/courses
Create a new course
GET
/api/courses
Get all courses
GET
/api/courses/
Get all courses
GET
/api/courses/<id>
Get one course
PUT
/api/courses/<id>
Update one course
DELETE
/api/courses/<id>
Delete one course
For requests containing JSON data, include this header:

Content-Type: application/json
API Endpoints
1. Create a Course
Request
POST /api/courses
Example using
curl
curl -i -X POST http://127.0.0.1:5000/api/courses \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Flask REST API Fundamentals",
    "description": "Learn how to build REST APIs with Python and Flask.",
    "target_date": "2026-12-31",
    "status": "Not Started"
  }'
Required fields
name
description
target_date
status
Successful response
Status:

201 Created
Response:

{
  "id": 1,
  "name": "Flask REST API Fundamentals",
  "description": "Learn how to build REST APIs with Python and Flask.",
  "target_date": "2026-12-31",
  "status": "Not Started",
  "created_at": "2026-10-01T12:00:00+00:00"
}
The
id
and
created_at
fields are generated automatically by the application.

2. Get All Courses
Request
GET /api/courses
Example using
curl
curl -i http://127.0.0.1:5000/api/courses
The trailing-slash version also works:

curl -i http://127.0.0.1:5000/api/courses/
Successful response
Status:

200 OK
Response:

[
  {
    "id": 1,
    "name": "Flask REST API Fundamentals",
    "description": "Learn how to build REST APIs with Python and Flask.",
    "target_date": "2026-12-31",
    "status": "Not Started",
    "created_at": "2026-10-01T12:00:00+00:00"
  },
  {
    "id": 2,
    "name": "Python Data Structures",
    "description": "Learn lists, dictionaries, sets, and tuples.",
    "target_date": "2027-01-15",
    "status": "In Progress",
    "created_at": "2026-10-01T12:05:00+00:00"
  }
]
If there are no courses, the response is:

[]
3. Get One Course
Request
GET /api/courses/<id>
Replace
<id>
with a course ID.

For example:

GET /api/courses/1
Example using
curl
curl -i http://127.0.0.1:5000/api/courses/1
Successful response
Status:

200 OK
Response:

{
  "id": 1,
  "name": "Flask REST API Fundamentals",
  "description": "Learn how to build REST APIs with Python and Flask.",
  "target_date": "2026-12-31",
  "status": "Not Started",
  "created_at": "2026-10-01T12:00:00+00:00"
}
4. Update a Course
Request
PUT /api/courses/<id>
The current implementation expects all editable fields in the request:

name
description
target_date
status
The
id
and
created_at
values cannot be changed.

Example JSON payload
{
  "name": "Advanced Flask REST APIs",
  "description": "Build and test REST APIs using Flask.",
  "target_date": "2027-02-28",
  "status": "In Progress"
}
Example using
curl
curl -i -X PUT http://127.0.0.1:5000/api/courses/1 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Advanced Flask REST APIs",
    "description": "Build and test REST APIs using Flask.",
    "target_date": "2027-02-28",
    "status": "In Progress"
  }'
Successful response
Status:

200 OK
Response:

{
  "id": 1,
  "name": "Advanced Flask REST APIs",
  "description": "Build and test REST APIs using Flask.",
  "target_date": "2027-02-28",
  "status": "In Progress",
  "created_at": "2026-10-01T12:00:00+00:00"
}
Notice that the
id
and
created_at
values remain unchanged.

5. Delete a Course
Request
DELETE /api/courses/<id>
Example using
curl
curl -i -X DELETE http://127.0.0.1:5000/api/courses/1
Successful response
Status:

200 OK
Response:

{
  "message": "Course with id 1 was deleted"
}
After deleting the course, requesting it again returns a
404 Not Found
response.

HTTP Status Codes
The API uses the following status codes:

Status code	Meaning
200 OK
The operation completed successfully
201 Created
A new course was created
400 Bad Request
The request contains invalid or missing data
404 Not Found
The course or endpoint does not exist
500 Internal Server Error
The server encountered a file or unexpected error
Testing the API
Test the complete CRUD workflow
1. Create a course
curl -i -X POST http://127.0.0.1:5000/api/courses \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Learn Flask",
    "description": "Learn Flask fundamentals and routing.",
    "target_date": "2026-12-31",
    "status": "Not Started"
  }'
Expected status:

201 Created
2. Get all courses
curl -i http://127.0.0.1:5000/api/courses
Expected status:

200 OK
3. Get course ID 1
curl -i http://127.0.0.1:5000/api/courses/1
Expected status:

200 OK
4. Update course ID 1
curl -i -X PUT http://127.0.0.1:5000/api/courses/1 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Learn Flask REST APIs",
    "description": "Learn Flask routing, JSON responses, and REST API design.",
    "target_date": "2027-01-31",
    "status": "In Progress"
  }'
Expected status:

200 OK
5. Delete course ID 1
curl -i -X DELETE http://127.0.0.1:5000/api/courses/1
Expected status:

200 OK
6. Confirm that course ID 1 was deleted
curl -i http://127.0.0.1:5000/api/courses/1
Expected status:

404 Not Found
Error Testing
Missing required field
This request is missing
name
:

curl -i -X POST http://127.0.0.1:5000/api/courses \
  -H "Content-Type: application/json" \
  -d '{
    "description": "This course does not have a name.",
    "target_date": "2026-12-31",
    "status": "Not Started"
  }'
Expected response:

400 Bad Request
{
  "error": "Missing required field(s): name"
}
Invalid status
curl -i -X POST http://127.0.0.1:5000/api/courses \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Invalid Status Course",
    "description": "This course has an invalid status.",
    "target_date": "2026-12-31",
    "status": "Started"
  }'
Expected response:

400 Bad Request
{
  "error": "status must be one of: Completed, In Progress, Not Started"
}
Invalid date format
curl -i -X POST http://127.0.0.1:5000/api/courses \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Invalid Date Course",
    "description": "This course has an invalid date.",
    "target_date": "12/31/2026",
    "status": "Not Started"
  }'
Expected response:

400 Bad Request
{
  "error": "target_date must use YYYY-MM-DD format"
}
Empty name
curl -i -X POST http://127.0.0.1:5000/api/courses \
  -H "Content-Type: application/json" \
  -d '{
    "name": "",
    "description": "The course name is empty.",
    "target_date": "2026-12-31",
    "status": "Not Started"
  }'
Expected response:

400 Bad Request
{
  "error": "name must be a non-empty string"
}
Course not found
curl -i http://127.0.0.1:5000/api/courses/9999
Expected response:

404 Not Found
{
  "error": "Course with id 9999 was not found"
}
Invalid JSON body
curl -i -X POST http://127.0.0.1:5000/api/courses \
  -H "Content-Type: application/json" \
  -d '{"name": "Invalid JSON"'
Expected response:

400 Bad Request
{
  "error": "Request body must be a JSON object"
}
Testing with Postman or Insomnia
You can also test the API using an API client such as Postman or Insomnia.

Create a course
Create a new
POST
request.

Use this URL:

http://127.0.0.1:5000/api/courses
Select the
Body
tab.

Select
raw
.

Choose
JSON
.

Enter:

{
  "name": "Python Testing",
  "description": "Learn how to test Python applications.",
  "target_date": "2027-03-01",
  "status": "Not Started"
}
Send the request.

The response should have status
201 Created
.

Get all courses
Create a
GET
request.

Use:

http://127.0.0.1:5000/api/courses
Send the request.

The response should have status
200 OK
.

Project Structure
A simple project structure is:

codecrafthub/
├── app.py
├── courses.json
└── README.md
app.py
This is the main Flask application.

It contains:

Flask configuration
API routes
Course validation
JSON file reading
JSON file writing
ID generation
Error handling
courses.json
This file stores all course data.

When the application starts or receives a request, it creates the file automatically if it does not exist.

An empty file contains:

[]
After adding courses, it may look like:

[
  {
    "id": 1,
    "name": "Flask REST API Fundamentals",
    "description": "Learn how to build REST APIs with Python and Flask.",
    "target_date": "2026-12-31",
    "status": "Not Started",
    "created_at": "2026-10-01T12:00:00+00:00"
  }
]
README.md
This file contains the project documentation, setup instructions, API examples, and troubleshooting information.

How JSON Storage Works
The application stores courses as a JSON list.

When a request needs course data, the application:

Opens
courses.json
.
Reads the JSON contents.
Converts the JSON into a Python list.
Uses the list in the API operation.
When a course is created, updated, or deleted, the application:

Reads the current courses.
Changes the Python list.
Writes the complete list back to
courses.json
.
For example, a JSON file containing:

[]
becomes:

[
  {
    "id": 1,
    "name": "Learn Python",
    "description": "Learn Python programming fundamentals.",
    "target_date": "2026-12-31",
    "status": "Not Started",
    "created_at": "2026-10-01T12:00:00+00:00"
  }
]
This approach is convenient for learning and small local projects. A database would be more suitable for a larger application with many users or simultaneous requests.

Troubleshooting
python
command is not recognized
Try:

python3 --version
If that works, use
python3
instead of
python
:

python3 app.py
On Windows, reinstall Python and select:

Add Python to PATH
during installation.

pip
command is not recognized
Try:

python -m pip install flask
or:

python3 -m pip install flask
Flask is not installed
If you see:

ModuleNotFoundError: No module named 'flask'
Install Flask:

pip install flask
If you are using a virtual environment, activate it first.

The virtual environment does not activate
Windows
Use:

venv\Scripts\activate
If PowerShell blocks the command, you may need to update the execution policy:

Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
Then try activating the environment again.

macOS or Linux
Use:

source venv/bin/activate
Port 5000 is already in use
Another application may already be using port
5000
.

You can change the port in
app.py
:

if __name__ == "__main__":
    app.run(debug=True, port=5001)
Then run the application and use:

http://127.0.0.1:5001
courses.json
is missing
The application is designed to create the file automatically.

You can also create it manually in the same directory as
app.py
:

[]
Make sure the filename is exactly:

courses.json
courses.json
contains invalid JSON
The file must contain valid JSON.

A valid empty file looks like:

[]
If the file has become corrupted, back it up and replace its contents with:

[]
Be aware that replacing the file will remove the existing course data.

A request returns
400 Bad Request
Check that:

The request uses the
Content-Type: application/json
header.
The JSON syntax is valid.
All required fields are present.
target_date
uses
YYYY-MM-DD
.
status
is one of the allowed values.
name
and
description
are not empty.
Valid statuses are:

Not Started
In Progress
Completed
A request returns
404 Not Found
Check that:

The Flask application is running.
The URL is correct.
The course ID exists.
The course ID is a number.
For example:

curl http://127.0.0.1:5000/api/courses/1
If course
1
does not exist, the API correctly returns
404 Not Found
.

A request returns
500 Internal Server Error
Check:

The terminal where Flask is running.
Whether
courses.json
can be read.
Whether the application has permission to write to the project folder.
Whether
courses.json
contains valid JSON.
The terminal usually contains more detailed information about the error.

REST API Concepts Used
Resource
A resource is something managed by an API.

In CodeCraftHub, the main resource is:

courses
HTTP methods
Different HTTP methods represent different actions:

HTTP method	Purpose
POST
Create data
GET
Read data
PUT
Update data
DELETE
Delete data
Together, these operations are called CRUD:

Create
Read
Update
Delete
JSON
JSON is the format used to send and receive course data.

Example:

{
  "name": "Learn Flask",
  "description": "Build applications with Flask.",
  "target_date": "2026-12-31",
  "status": "Not Started"
}
Status codes
HTTP status codes tell the client whether a request succeeded.

For example:

201
means a resource was created.
200
means the request succeeded.
400
means the request data was invalid.
404
means the requested resource was not found.
500
means the server encountered an error.
Limitations
This project intentionally uses a JSON file instead of a database to keep the code simple for beginners.

A JSON file is appropriate for:

Learning projects
Small local applications
Simple demonstrations
Single-user use
A database would be better for:

Multiple users
Large amounts of data
Many simultaneous requests
Advanced searching and filtering
Production deployments
Reliable transaction handling
Authentication and user management are not included in this project.

Future Improvements
Possible improvements include:

Add a web interface
Add course filtering by status
Add course search
Add pagination
Add automated unit tests
Add authentication
Add user-specific course lists
Replace JSON storage with SQLite or PostgreSQL
Deploy the API to a cloud platform
Add API documentation with Swagger or OpenAPI
License
This project is intended for educational purposes. You may modify and extend it as you learn more about Python, Flask, and REST APIs.

