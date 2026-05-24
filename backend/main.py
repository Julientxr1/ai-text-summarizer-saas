"""
API FastAPI pour le résumé de texte.
"""

import os
import time
import logging
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from anthropic import Anthropic

# ---------------------------------------------------------------------------
# Configuration des logs
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("summarizer")

# ---------------------------------------------------------------------------
# Chargement de l'environnement
# ---------------------------------------------------------------------------
load_dotenv()

MODEL = "claude-opus-4-6"

# CORS : lecture depuis .env, fallback sur localhost uniquement
_raw_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000")
ALLOWED_ORIGINS: list[str] = [o.strip() for o in _raw_origins.split(",") if o.strip()]

# ---------------------------------------------------------------------------
# Application
# ---------------------------------------------------------------------------
app = FastAPI(
    title="Text Summarizer API",
    description="Une API simple pour résumer du texte",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info("CORS configuré pour : %s", ALLOWED_ORIGINS)


# ---------------------------------------------------------------------------
# Modèles Pydantic
# ---------------------------------------------------------------------------
class SummarizeRequest(BaseModel):
    """Modèle pour la requête de résumé."""
    text: str


class SummarizeResponse(BaseModel):
    """Modèle pour la réponse de résumé."""
    summary: str


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.get("/")
def read_root() -> dict[str, str]:
    """Route de test pour vérifier que l'API fonctionne."""
    return {"message": "API Text Summarizer est en ligne"}


@app.post("/summarize")
def summarize(request: SummarizeRequest, req: Request) -> SummarizeResponse:
    """
    Route pour résumer du texte.

    Args:
        request: Objet contenant le texte à résumer
        req: Requête HTTP (pour les logs)

    Returns:
        Objet contenant le texte résumé
    """
    client_ip = req.client.host if req.client else "inconnu"
    text_length = len(request.text.strip())

    logger.info(
        "Requête reçue | ip=%s | taille_texte=%d caractères | modèle=%s",
        client_ip,
        text_length,
        MODEL,
    )

    # Validation
    if not request.text or not request.text.strip():
        logger.warning("Requête rejetée | ip=%s | raison=texte vide", client_ip)
        raise HTTPException(status_code=400, detail="Le texte ne peut pas être vide")

    # Clé API
    api_key: str | None = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        logger.error("Clé API Anthropic manquante (ANTHROPIC_API_KEY non définie)")
        raise HTTPException(
            status_code=500,
            detail="La clé API Anthropic n'est pas configurée. Veuillez définir ANTHROPIC_API_KEY dans le fichier .env",
        )

    # Appel à l'API
    start = time.perf_counter()
    try:
        client = Anthropic(api_key=api_key)
        message = client.messages.create(
            model=MODEL,
            max_tokens=1024,
            system="Tu es un expert en synthèse, résume le texte suivant de manière concise",
            messages=[{"role": "user", "content": request.text}],
        )

        summary: str = message.content[0].text
        duration_ms = (time.perf_counter() - start) * 1000

        logger.info(
            "Résumé généré | ip=%s | taille_texte=%d car. | taille_résumé=%d car. | modèle=%s | durée=%.0fms",
            client_ip,
            text_length,
            len(summary),
            MODEL,
            duration_ms,
        )

        return SummarizeResponse(summary=summary)

    except Exception as e:
        duration_ms = (time.perf_counter() - start) * 1000
        logger.error(
            "Erreur API | ip=%s | modèle=%s | durée=%.0fms | erreur=%s",
            client_ip,
            MODEL,
            duration_ms,
            str(e),
        )
        raise HTTPException(status_code=500, detail=f"Erreur lors du résumé: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
