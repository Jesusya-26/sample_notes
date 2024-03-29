# Notes API

This is a simple note-taking service based on **FastAPI**, **SQLAlchemy** (AsyncPG) and **Keycloak**.

## preparation

1. To install python dependencies
  run `poetry install`. You may also want to use `venv` before that.
2. Prepare a PostgreSQL Server to store the database.
3. Go to ./test_fastapi/db and run `alembic upgrade head` to apply migrations. Do not forget to set environment variables
  `DB_ADDR`, `DB_PORT`, `DB_NAME`, `DB_USER` and `DB_PASS` (or list them in .env file) if they are different from
  default values.

## configuring keycloak

1. From a terminal, enter the following command to start Keycloak: 

`docker run -p 8080:8080 -e KEYCLOAK_ADMIN=admin -e KEYCLOAK_ADMIN_PASSWORD=admin quay.io/keycloak/keycloak:24.0.2 start-dev`

2. Go to the [Keycloak Admin Console](http://localhost:8080) and log in with the username and password you created earlier.
3. Create realm **Test** in the top-left corner and go to it.
4. Click **Users** in the left-hand menu and **Add user**. Fill in the form with any values.
5. To set the initial password: click **Credentials** at the top of the page, fill in the **Set password** form with a password and toggle **Temporary** to **Off** so that the user does not need to update this password at the first login.
6. To secure the first application, you start by registering the application with your Keycloak instance:

- click **Clients** and then **Create client**. 
- **Client type**: OpenID Connect 
- **Client ID**: notesAPI
- Click **Next**
- Confirm that **Standard flow** is enabled.
- Click **Next**
- Set **Valid redirect URIs** to http://127.0.0.1:8000/* and http://localhost:8000/*
- Set **Web origins** to *
- Click Save

7. Create roles *admin* and *user* in **Realm roles**.
8. Go to the created user, click **Role mapping**, **Assign role** and select one of the roles you created earlier.

## launching

Run backend locally with `poetry launch_notes_api` or `poetry launch_notes_api --debug`.

You can open [localhost:8000](http://localhost:8000) (or different host/port if you configured it) to get a redirect to Swagger UI with endpoints list.