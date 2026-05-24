"""
API FastAPI pour le résumé de texte.
"""

import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from anthropic import Anthropic

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Initialiser l'application FastAPI
app = FastAPI(
    title="Text Summarizer API",
    description="Une API simple pour résumer du texte",
    version="1.0.0"
)

# Configuration CORS pour permettre les requêtes du frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Modèles Pydantic pour la validation
class SummarizeRequest(BaseModel):
    """Modèle pour la requête de résumé."""
    text: str


class SummarizeResponse(BaseModel):
    """Modèle pour la réponse de résumé."""
    summary: str


# Routes
@app.get("/")
def read_root() -> dict[str, str]:
    """Route de test pour vérifier que l'API fonctionne."""
    return {"message": "API Text Summarizer est en ligne"}


@app.post("/summarize")
def summarize(request: SummarizeRequest) -> SummarizeResponse:
    """
    Route pour résumer du texte.
    
    Args:
        request: Objet contenant le texte à résumer
        
    Returns:
        Objet contenant le texte résumé
    """
    # Vérifier que le texte n'est pas vide
    if not request.text or not request.text.strip():
        raise HTTPException(status_code=400, detail="Le texte ne peut pas être vide")
    
    # Récupérer la clé API depuis les variables d'environnement
    api_key: str | None = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="La clé API Anthropic n'est pas configurée. Veuillez définir ANTHROPIC_API_KEY dans le fichier .env"
        )
    
    try:
        # Initialiser le client Anthropic
        client: Anthropic = Anthropic(api_key=api_key)
        
        # Envoyer la requête à l'API Anthropic avec un prompt système
        message = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=1024,
            system="Tu es un expert en synthèse, résume le texte suivant de manière concise",
            messages=[
                {
                    "role": "user",
                    "content": request.text
                }
            ]
        )
        
        # Extraire le texte du résumé
        summary: str = message.content[0].text
        
        return SummarizeResponse(summary=summary)
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors du résumé: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
