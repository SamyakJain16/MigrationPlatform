"""
This file stores configuration settings like Supabase keys, secret keys, and debug settings. You can also load environment variables here using python-dotenv.


"""

import os


class Config:
    SUPABASE_URL = os.getenv(
        "SUPABASE_URL", "https://kcayvmqcpzraswwffsgl.supabase.co")
    SUPABASE_KEY = os.getenv(
        "SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtjYXl2bXFjcHpyYXN3d2Zmc2dsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjgxODc3NTgsImV4cCI6MjA0Mzc2Mzc1OH0.BqPH1Ve6DrDSvmU2TyDBMXQ03swfcLl2N92eexd6FQM")
    JWT_SECRET_KEY = '22ee696d7c829940c04578d782be2ac739601e84034769aeeb378494e276f15c'
