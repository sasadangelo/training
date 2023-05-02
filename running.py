from app import db
from app.athlete_api import app
from app.athlete import Athlete 

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Athlete=Athlete)
