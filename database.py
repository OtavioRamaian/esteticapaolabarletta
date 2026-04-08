import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

def get_connection():
    """Cria e retorna a conexão segura com o Neon DB"""
    try:
        return psycopg2.connect(os.getenv("DATABASE_URL"))
    except Exception as e:
        print(f"Erro ao conectar no banco: {e}")
        return None

def run_query(query, params=None, fetch=True):
    """
    Executa qualquer query SQL.
    - query: O texto do comando SQL.
    - params: Tupla com os dados para evitar SQL Injection.
    - fetch: True para SELECT (retorna dados), False para INSERT/UPDATE/DELETE.
    """
    conn = get_connection()
    if not conn:
        return None if fetch else False

    # RealDictCursor faz com que os resultados tenham os nomes das colunas
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute(query, params)
        
        if fetch:
            result = cursor.fetchall()
            conn.commit()
            return result
            
        conn.commit()
        return True
    except Exception as e:
        print(f"Erro na execução da query: {e}")
        conn.rollback()
        return None if fetch else False
    finally:
        cursor.close()
        conn.close()