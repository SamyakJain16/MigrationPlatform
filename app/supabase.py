"""
This file handles the Supabase client setup. Any interaction with the Supabase database should go through here.


"""


from supabase import create_client
from .config import Config

# Initialize Supabase client
supabase_client = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)
