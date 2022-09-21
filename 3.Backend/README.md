# Training Backend

## Purpose

* Providing basic knowledge of Web Application and Web Development
* Knowing how to use different types of HTTP Request and HTTP Response
* Building a full basic functionality Web Server

## Require

* Object-oriented programming skills with `Python`
* Library management with `Pip`
* Basic knowledge of `MongoDB` database and `PyMongo` library

## Theory

*Reference: [HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP)*

### MVC Architecture

MVC is an architectural pattern which means it rules the whole architecture of the applications.

[//]: # (![MVC Architecture]&#40;images/mvc.png&#41;)

<p align="center">
    <img src="docs/images/mvc.png" alt="MVC Architecture" width="400"/>
</p>

* Model: Contains all the objects that describe the data such as classes, data processing methods, and is responsible for accessing data on the database.
* View: A collection of user interface files.
* Controller: Keeping the task of handling user requests, Controller will call Model to manipulate the database and return the user interface through View.

> *Task 1: Descript MVC model operation flow*

*Reference: [Đôi điều về mô hình MVC](https://viblo.asia/p/doi-dieu-ve-mo-hinh-mvc-E375z0vJZGW)*

### HTTP Request

[//]: # (![HTTP Request]&#40;images/http_request.png&#41;)

<p align="center">
    <img src="docs/images/http_request.png" alt="HTTP Request" width="500"/>
</p>

Requests consist of the following elements:

* `HTTP method`: Defines the operation the client wants to perform. Typically, a client wants to fetch a resource (using GET) or post the value of an HTML form (using POST).
* `Path`: The path of the resource to fetch.
* `Version`: The version of the HTTP protocol.
* `Headers`: That convey additional information for the servers.
* `Body`: (optional) For some methods like POST, which contain the resource sent.

> *Task 2: List HTTP methods and their usage*

*Reference: [Requests](https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview#requests)*

### HTTP Response

[//]: # (![HTTP Response]&#40;images/http_response.png&#41;)

<p align="center">
    <img src="docs/images/http_response.png" alt="HTTP Response" width="500"/>
</p>

Responses consist of the following elements:

* `Version`: The version of the HTTP protocol.
* `Status Code`: Indicating if the request was successful or not, and why.
* `Status Message`: A non-authoritative short description of the status code.
* `Headers`: That convey additional information for the servers.
* `Body`: (optional) Containing the fetched resource.

> *Task 3: List HTTP response status codes and their meanings*

*Reference: [Responses](https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview#responses)*

### RESTful API with CRUD

| Action                 | Method | Path           |
|------------------------|--------|----------------|
| Get all entities       | GET    | /entities      |
| Create an entity       | POST   | /entities      |
| Get an entity by ID    | GET    | /entities/{id} |
| Update an entity by ID | PUT    | /entities/{id} |
| Delete an entity by ID | DELETE | /entities/{id} |

*Reference: [RESTful API là gì ?](https://viblo.asia/p/restful-api-la-gi-1Je5EDJ4lnL)*

## Practice

> Follow the instructions in the project [TrainingAPI](TrainingAPI)
