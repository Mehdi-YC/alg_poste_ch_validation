from fastapi import FastAPI, Form, File, UploadFile, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Base, Cheque, Person
import shutil
import os

# Initialisation de l'application
app = FastAPI()

# Configuration de la base de données
DATABASE_URL = "sqlite:///./database.db"
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Ajouter le dossier statique
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configurer les templates
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/upload/")
async def upload_cheque(file: UploadFile = File(...)):
    """
    Route pour téléverser un chèque, traiter les données et retourner les résultats.
    """
    session = SessionLocal()

    # Sauvegarder l'image téléchargée
    upload_path = f"static/uploads/{file.filename}"
    with open(upload_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Simuler un traitement (à personnaliser selon vos besoins)
    modified_path = f"static/uploads/processed_{file.filename}"
    shutil.copy(upload_path, modified_path)  # Simuler l'image traitée

    # Rechercher une personne associée (données factices pour l'exemple)
    person = session.query(Person).first()  # Exemple : première personne dans la base

    # Simulation de validité (valide ou invalide)
    validity = "Valide" if person else "Invalide"

    # Insérer le chèque dans la base
    cheque = Cheque(
        original_image=upload_path,
        modified_image=modified_path,
        validity=validity,
        person_id=person.id if person else None,
    )
    session.add(cheque)
    session.commit()

    # Réponse JSON pour afficher les résultats
    response = {
        "original_image": upload_path,
        "modified_image": modified_path,
        "person": {"name": person.name, "signature": person.signature} if person else None,
        "validity": validity,
    }

    session.close()
    return response

history_data = [
    {"image": "uploads/cheque1.jpg", "name": "John Doe", "status": "Valid", "date": "2024-11-29"},
    {"image": "uploads/cheque2.jpg", "name": "Jane Smith", "status": "Invalid", "date": "2024-11-28"},
    {"image": "uploads/cheque3.jpg", "name": "Alice Brown", "status": "Valid", "date": "2024-11-27"},
    {"image": "uploads/cheque4.jpg", "name": "Bob White", "status": "Invalid", "date": "2024-11-26"},
    {"image": "uploads/cheque5.jpg", "name": "Michael Black", "status": "Valid", "date": "2024-11-25"},
    {"image": "uploads/cheque6.jpg", "name": "Mary Green", "status": "Valid", "date": "2024-11-24"},
]

# Route to get the "Historique"
@app.get("/historique")
async def get_historique(request: Request):
    return templates.TemplateResponse("historique.html", {"request": request, "history_data": history_data})
