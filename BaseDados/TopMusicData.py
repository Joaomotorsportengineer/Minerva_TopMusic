import sqlite3
import warnings

import billboard

# Anos suportados pelo year-end hot-100-songs (2006–2025)
ANO_INICIAL = 2006
ANO_FINAL = 2025
MUSICAS_POR_ANO = 10
ARQUIVO_DB = "top_musicas.db"
TABELA = "top_musicas"


def main():
    warnings.filterwarnings("ignore", category=UserWarning, module="billboard")

    conn = sqlite3.connect(ARQUIVO_DB)
    conn.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {TABELA} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_musica TEXT NOT NULL,
            ano INTEGER NOT NULL,
            autor TEXT NOT NULL
        )
        """
    )
    conn.execute(f"DELETE FROM {TABELA}")

    for year in range(ANO_INICIAL, ANO_FINAL + 1):
        try:
            chart = billboard.ChartData("hot-100-songs", year=year)
            for i, entry in enumerate(chart):
                if i >= MUSICAS_POR_ANO:
                    break
                conn.execute(
                    f"INSERT INTO {TABELA} (nome_musica, ano, autor) VALUES (?, ?, ?)",
                    (entry.title, year, entry.artist),
                )
            print(f"Ano {year}: ok")
        except Exception as e:
            print(f"Ano {year}: erro - {e}")

    conn.commit()
    total = conn.execute(f"SELECT COUNT(*) FROM {TABELA}").fetchone()[0]
    conn.close()

    print(f"Salvo: {ARQUIVO_DB} (tabela {TABELA}, {total} linhas)")


if __name__ == "__main__":
    main()