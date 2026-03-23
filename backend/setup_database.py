#!/usr/bin/env python3
"""
Script para criar tabelas no PostgreSQL usando credenciais do .env
"""
import os
import sys
from pathlib import Path

# Carregar .env
sys.path.insert(0, str(Path(__file__).parent))

from app.config import get_settings

try:
    import psycopg2
    
    settings = get_settings()
    print(f"[*] DATABASE_URL: {settings.database_url}")
    print("[*] Conectando ao PostgreSQL...")
    
    # Extrair credenciais da DATABASE_URL
    # postgresql://user:password@host:port/database
    db_url = settings.database_url
    
    # Parse simples
    if db_url.startswith("postgresql://"):
        db_url = db_url.replace("postgresql://", "")
        # user:password@host:port/database
        creds, rest = db_url.split("@")
        user, password = creds.split(":")
        host_port, database = rest.split("/")
        host, port = host_port.split(":")
        port = int(port)
    else:
        print("[ERRO] DATABASE_URL deve estar em formato postgresql://")
        sys.exit(1)
    
    print(f"[*] User: {user}, Host: {host}, DB: {database}")
    
    conn = psycopg2.connect(
        user=user,
        password=password,
        host=host,
        port=port,
        database=database
    )
    
    cur = conn.cursor()
    print("[OK] Conectado ao PostgreSQL!")
    
    # Criar tabelas
    cur.execute("DROP TABLE IF EXISTS attempts CASCADE")
    cur.execute("DROP TABLE IF EXISTS games CASCADE")
    cur.execute("DROP TABLE IF EXISTS users CASCADE")
    
    cur.execute("""CREATE TABLE users (
        id VARCHAR(36) PRIMARY KEY,
        email VARCHAR(255) UNIQUE NOT NULL,
        username VARCHAR(100) UNIQUE NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")
    print("[OK] Tabela 'users' criada")
    
    cur.execute("""CREATE TABLE games (
        id VARCHAR(36) PRIMARY KEY,
        user_id VARCHAR(36) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        secret_code TEXT NOT NULL,
        status VARCHAR(20) NOT NULL,
        started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        ended_at TIMESTAMP,
        final_score FLOAT,
        attempts_count INTEGER DEFAULT 0
    )""")
    print("[OK] Tabela 'games' criada")
    
    cur.execute("""CREATE TABLE attempts (
        id VARCHAR(36) PRIMARY KEY,
        game_id VARCHAR(36) NOT NULL REFERENCES games(id) ON DELETE CASCADE,
        guess TEXT NOT NULL,
        correct_positions INTEGER,
        correct_colors INTEGER,
        attempt_number INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")
    print("[OK] Tabela 'attempts' criada")
    
    # Indices
    cur.execute("CREATE INDEX idx_users_email ON users(email)")
    cur.execute("CREATE INDEX idx_users_username ON users(username)")
    cur.execute("CREATE INDEX idx_games_user_id ON games(user_id)")
    cur.execute("CREATE INDEX idx_attempts_game_id ON attempts(game_id)")
    print("[OK] Indices criados")
    
    conn.commit()
    cur.close()
    conn.close()
    
    print("\n[SUCESSO] PostgreSQL inicializado com sucesso!\n")
    
except Exception as e:
    print(f"[ERRO] {e}")
    import traceback
    traceback.print_exc()
