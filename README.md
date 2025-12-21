# Visualizzazione consumi Iliad

Uno script Python che si collega a https://www.iliad.it/account/ usando le credenziali specificate dinamicamente oppure in `.env` e ritorna la quantità di GB consumati rispetto alla propria offerta.

Lo script è stato creato interamente guidando la IA di Claude da zero dando opportuni prompt di input. In questo caso il lavoro di sviluppo è stato quello di ispezionare la pagina di login coi developer tools per guidare meglio il prompt della IA nelle richieste di ciò che si voleva ottenere.

La creazione iniziale del repository è stata fatta usando i prompt specificati in [claude-creation-prompt.txt](claude-creation-prompt.txt) ed ha richiesto all'incirca un paio d'ore.

## Installazione

```bash
poetry install
```

## Configurazione

Copiare il file `.env.example` in `.env` e inserire le proprie credenziali:

```bash
cp .env.example .env
```

Contenuto del file `.env`:

```
ILIAD_USER_ID=12345678
ILIAD_PASSWORD=your_password_here
ILIAD_DATA_GB=150
```

- `ILIAD_USER_ID`: ID utente Iliad (8 cifre)
- `ILIAD_PASSWORD`: Password dell'account
- `ILIAD_DATA_GB`: GB totali disponibili nella propria offerta

## Utilizzo

```bash
poetry run iliad_account
```

Output di esempio:

```
Logging in...
Login successful!

Fetching progress value...

Data usage: 8.08 GB / 250 GB (3.23%)
```

Se le credenziali non sono presenti nel file `.env`, verranno richieste interattivamente.

## Debug

Per abilitare l'output di debug:

```bash
DEBUG=1 poetry run iliad_account
```
