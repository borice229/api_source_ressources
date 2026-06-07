from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#  Définition de l'emplacement de la base SQLite
DATABASE_URL = "sqlite:///ressources.db"

# Le moteur (Engine) : gère la communication avec le fichier .db
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# La Fabrique de Sessions : pour ouvrir/fermer les accès aux données
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# La Base : classe mère pour nos futurs modèles
Base = declarative_base()

if __name__=="__main__":
    try:
        with engine.connect() as connnexion:
            print("Connexion réussi ")
    
    except Exception as e:

        print(f"Echec : {e}")
