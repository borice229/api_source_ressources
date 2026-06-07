from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
from pydantic import BaseModel
from typing import List , Optional
from fastapi import FastAPI, Query, Depends
from sqlalchemy.orm import Session



#  Définition de l'emplacement de la base SQLite
DATABASE_URL = "sqlite:///ressources.db"

# Le moteur (Engine) : gère la communication avec le fichier .db
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# La Fabrique de Sessions : pour ouvrir/fermer les accès aux données
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# La Base : classe mère pour nos futurs modèles
Base = declarative_base()


# =========================================
# Model  Ressources
#==========================================

class RessourcesModel(Base):
    __tablename__="ressources"

    Matricule = Column(Integer, primary_key=True)
    Date_presence = Column(String, primary_key=True)
    Lieu_travail = Column(String)
    Population = Column(String)
    Site = Column(String)
    Type_de_contrat = Column(String)
    Duree_travail = Column(Float)
    Temps_travail = Column(Integer)
    Experience = Column(Integer)



class RessourceSchema(BaseModel):
    Matricule: int
    Date_presence: str
    Lieu_travail: Optional[str] = None
    Population: Optional[str] = None
    Site: Optional[str] = None
    Type_de_contrat: Optional[str] = None
    Duree_travail: Optional[float] = None
    Temps_travail: Optional[int] = None
    Experience: Optional[int] = None

    class Config:
        from_attributes = True


class PaginatedResponse(BaseModel):
    total_records: int           # Le nombre total de lignes dans la table (ex: 389 353)
    page: int                    # Le numéro de la page demandée
    size: int                    # Le nombre de lignes par page
    data: List[RessourceSchema]  # Les données réelles de la page




app = FastAPI(title="API ressources")

@app.get("/")
def root():
    return {"message": "Welcome to ressource API"}

#  Dépendance pour ouvrir/fermer proprement la session de la base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# L'endpoint de lecture avec pagination
@app.get("/api/ressources", response_model=PaginatedResponse)
def get_ressources(
    page: int = Query(1, ge=1, description="Numéro de la page"),
    size: int = Query(100, ge=1, le=1000, description="Nombre de lignes par page"),
    db: Session = Depends(get_db)
):
    # Calcul de l'index de départ (offset)
    offset = (page - 1) * size
    
    # Récupération du nombre total de lignes 
    total_records = db.query(RessourcesModel).count()
    
    # Requête paginée avec LIMIT et OFFSET
    ressources = db.query(RessourcesModel).offset(offset).limit(size).all()
    
    # Retour de la réponse qui respecte le schéma PaginatedResponse
    return {
        "total_records": total_records,
        "page": page,
        "size": size,
        "data": ressources
    }