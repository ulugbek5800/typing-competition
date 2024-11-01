# WebsterType API

This is the backend API for **WebsterType** (formerly *Typing Competition*), a web application where users can test their typing speed, view leaderboards, and manage their profiles. The backend is deployed on PythonAnywhere, while the frontend is hosted on Vercel.

## Overview

The WebsterType API provides backend functionality for:
- **User Authentication**: Secure registration and login.
- **Typing Game**: Players can submit typing test scores.
- **Leaderboard**: Tracks top scores in different game modes.
- **Profile Management**: Allows users to upload and manage profile pictures.

## Technologies Used

- **Backend**: Python, Flask, SQLAlchemy, Flask-JWT-Extended
- **Database**: SQLite (for simplicity and easy deployment)

## Project Deployment

- **Backend**: Deployed on PythonAnywhere at [https://ulugbek5800.pythonanywhere.com](https://ulugbek5800.pythonanywhere.com).
- **Frontend**: Deployed on Vercel, available at [https://type-com.vercel.app/](https://type-com.vercel.app/).
  - Frontend GitHub Repository: [Frontend GitHub](https://github.com/gitfromnfsheatxaxa/typeCom)

## How to Use the Application

To use the WebsterType application, visit the live site hosted on Vercel: [https://type-com.vercel.app/](https://type-com.vercel.app/). 

Here, you can register, log in, and start testing your typing skills!

## API Endpoints

| Endpoint                         | Method | Description                                                                                   | Authentication |
|----------------------------------|--------|-----------------------------------------------------------------------------------------------|----------------|
| `/api/signup`                    | POST   | Register a new user account with a username and password.                                     | No             |
| `/api/login`                     | POST   | Log in to receive a JWT token for authenticated access.                                       | No             |
| `/api/submit-score`              | POST   | Submit a typing test score, specifying the game mode (e.g., `normal` or `hard`).              | No             |
| `/api/leaderboard?mode=<mode>`   | GET    | Retrieve the leaderboard for the specified mode (`normal` or `hard`).                         | No             |
| `/api/profile`                   | GET    | Retrieve profile information, including username and scores.                                  | Yes            |
| `/api/profile/upload-picture`    | POST   | Upload a profile picture (only `png`, `jpg`, and `jpeg` formats are allowed).                 | Yes            |
| `/api/profile/delete-picture`    | DELETE | Delete the current profile picture from the account.                                          | Yes            |

## Usage

All protected routes require JWT authentication. Ensure the access token is included in the `Authorization` header as `Bearer <token>`.

---

For more details, visit the [frontend repository](https://github.com/gitfromnfsheatxaxa/typeCom) or explore the live deployment on [Vercel](https://type-com.vercel.app/).

## License

This project is open-source and licensed under the MIT License.
