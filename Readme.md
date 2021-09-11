# Krypto
## Price Trigger for Krypto 

The repo contains price triggger application for BTC.
## Features

- Admin and user accounts are there. Admin can create new user accounts.
- Password are stored after hashing in database.
- User accounts can create, delete or fetch price triggers.
- Authentication takes place with JWT. Once authentication token is generated it is given to the user. The token is stored in user **cookies** and send automatically or the user could send the authentication token with **"x-access-token"** header. Token validity 30 min.
- Pagination is also available for fetch_all API.
- JWT tokens are created with a dynamicaly generated key file.
- While rumnning the application requires the user to enter  gmail-id and password once.
- The application uses google smtp serverto send emails. SMTP server string could be modified in **emailconf.py** file to change SMTP server.
- The user needs to enable access in his/her gmail account to send emails. [Allow less secure apps to ON](https://myaccount.google.com/lesssecureapps)
- Once a alert is triggered it can only trigger after 6 hrs. This is done to avoid multiple alerts if the price is fluctuaing near the trigger price.

## Running the application
- Install all python packages in requirments.txt
- Install reddis server in Linux or windows (Linux or WSL preferable).
- Run redis-server in one tab or terminal.
- Open new tab, navigate to the Krypto folder in terminal, run **RQWORKER** by using the command `rqworker`. Make sure *"Listening on default status is displaying"*.
- In another new terminal or tab run the main python file by `python3 main.py`.
- The application should create a new key and ask for your gmail-id and password.
- Enable less secure app in gmail from the following link: [Allow less secure apps to ON](https://myaccount.google.com/lesssecureapps)

## API

| API | ACCESSLINK | TYPE |PARAMETERS|
| ------ | ------ | ----- | ----- |
| Login | [http://127.0.0.1:5000/login][PlGh]| GET, Basic Auth| username: e-mail, password: password
| Create User | [http://127.0.0.1:5000/user][PlGh] | POST | email: email, password: password
| Create Alerts | [http://127.0.0.1:5000/alerts/create][PlGd] | POST (JSON)| value: numeric type
| Delete Alerts | [http://127.0.0.1:5000/alerts/delete][PlOd] | DELETE (JSON)| value: numeric type
| Fetch Alerts | [http://127.0.0.1:5000/alerts/fetch][PlMe] | GET (URL Param)| page: numeric, per_page: numeric, status: 'created', 'triggered', 'deleted'

## Default accounts
| Account | Password |Type|
| ------ | ------ | ----- |
|admin123@gmail.com| admin123| Admin|
|ayushkumar1221@gmail.com| ayush123| User|

# Login
Login can be done through  [http://127.0.0.1:5000/login][PlGh] url. It requires basic auth to generate token. The token is stored in user **cookies** and send automatically or the user could send the authentication token with **"x-access-token"** header. Token validity 30 min.
Example:
![image](https://i.ibb.co/7SbBBwX/image.png)

# Creating new user
New User can be created through  [http://127.0.0.1:5000/user][PlGh] url. It requires email and passord in JSON format to be POST 'ed.

![image](https://i.ibb.co/2tfRJXK/image.png)

# Creating new alert
New Alerts can be created through  [http://127.0.0.1:5000/alerts/create][PlGh] url. It requires value to be POSTED in JSON format. Currently it creates only for BTC price but can be easily expanded.

![image](https://i.ibb.co/sFVWP1q/image.png)

## Fetching all alerts
Alerts can be fetched through  [http://127.0.0.1:5000/alerts/fetch][PlGh] url. It has page, per_page, status as optional parameter. Default valuefor page in 1 and per_page is 10.
![image](https://i.ibb.co/QjS7WgK/image.png)

## Deleting alerts
Alerts can be fetched through  [http://127.0.0.1:5000/alerts/delete][PlGh] url. It has value as default parameter.
![image](https://i.ibb.co/Y3jS46P/image.png)

## Bonus
- While I coludn't do bonus section but there could be a few different ways I could have approached the problem.
- Making a table of alerts witth limit 300. The alerts would be first searched in that table and then the main table. Alerts which are not in cache can be added to it and previous one deleted, so that it could maintain 300 record limit.
- Another better approach could be to use database like Mongodb to store and fetch the alerts as it would remove the requirment of searching for alerts completely. Therefore fetch alert could be server through mongodb and rest could be done with conventional database.