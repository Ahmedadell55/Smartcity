import os
from pydantic_settings import BaseSettings  # reads config from environment variables and .env file
class Settings(BaseSettings):
    SUPABASE_URL:str="https://jgoizofoygoewtdrxatx.supabase.co"
    SUPABASE_KEY:str="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Impnb2l6b2ZveWdvZXd0ZHJ4YXR4Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3NzAwNjAwNywiZXhwIjoyMDkyNTgyMDA3fQ.8_pIw5RWLfNJoSXDEzWJtmQitj76gBaA5ywZ0SfgzhE"
    PROJECTS_DIR: str = "saved_projects"
    APP_NAME: str = "SmartCity API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    ALLOWED_ORIGINS: list[str] = [
    "http://localhost:3000",
    "http://127.0.0.1:3000"
    ]
    # model_config = {
    #  "env_file": ".env"
    #  }
    def ensure_directories(self):
        os.makedirs(self.PROJECTS_DIR, exist_ok=True)

    # class Config:  #Convention over configuration
    #     env_file = ".env"
   
    
    #change name  no in Pydantic v1:
    #yes in Pydantic v2 if 
    model_config = {
     "env_file": ".env"
     }
settings = Settings()