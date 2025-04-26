# RAKN - Smart Parking Management System

This project is a web-based system that uses AI to automate parking management, violation detection, and employee access control.

## Project Structure
- **Backend**: Built with FastAPI (Python), handles authentication, violation logging, notifications, and AI models (Face Recognition, License Plate Recognition, Violation Detection).
- **Frontend**: Static website (HTML, CSS, JavaScript) for security staff and management use.
- **Database**: Firebase Firestore for data storage and Firebase Storage for images.

## Deployment
The backend and frontend are deployed together on Azure App Service. The application listens on port 8000.

## Running Instructions (locally)
```bash
uvicorn app.main:app --reload
