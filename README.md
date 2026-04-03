# Avatar4University API

API REST read-only per accedere ai dati di corsi universitari generati con avatar AI, costruita con FastAPI.

## Indice

- [Panoramica](#panoramica)
- [Gerarchia dei Dati](#gerarchia-dei-dati)
- [Installazione](#installazione)
- [Avvio](#avvio)
- [Autenticazione](#autenticazione)
- [Paginazione](#paginazione)
- [Filtri](#filtri)
- [Endpoint](#endpoint)
  - [Corsi](#corsi)
  - [Moduli](#moduli)
  - [Lezioni](#lezioni)
  - [Sezioni](#sezioni)
  - [Domande Aperte](#domande-aperte)
  - [Quiz](#quiz)
  - [Utenti](#utenti)
  - [Autenticazione Utente (Login)](#autenticazione-utente-login)
- [Errori](#errori)
- [Struttura del Progetto](#struttura-del-progetto)

---

## Panoramica

Questa API espone in sola lettura un database contenente corsi universitari completi, generati tramite avatar AI. Ogni corso è organizzato in una struttura gerarchica di moduli, lezioni, sezioni e slide. L'accesso è protetto tramite API key, e ogni chiave è associata a un'organizzazione: tutti i risultati sono filtrati per l'organizzazione corrispondente.

**Stack tecnologico:** FastAPI, SQLAlchemy, PostgreSQL/SQLite, Pydantic

---

## Gerarchia dei Dati

```
Organization
  ├── Course (via organization_id)
  │     └── Module
  │           └── Lesson
  │                 ├── Section
  │                 │     └── Slide (relazione 1:1 con Section)
  │                 ├── OpenQuestion
  │                 └── Quiz
  │                       └── QuizQuestion
  │                             └── QuizOption
  └── User (relazione N:N via user_organizations)
```

---

## Installazione

```bash
# Clona il repository
git clone https://github.com/micheleDibi/avatar4universityAPI.git
cd avatar4universityAPI

# Crea e attiva l'ambiente virtuale
python3 -m venv .venv
source .venv/bin/activate

# Installa le dipendenze
pip install -r requirements.txt

# Configura le API keys
cp .env.example .env
# Modifica il file .env e imposta API_KEYS con il mapping chiave → organization_id
```

---

## Avvio

```bash
source .venv/bin/activate
uvicorn app.main:app --reload
```

Il server sarà disponibile su `http://localhost:8000`.

La documentazione interattiva Swagger è accessibile su `http://localhost:8000/docs`.

---

## Autenticazione

Tutti gli endpoint (tranne il login) richiedono l'header `X-API-Key`. Ogni API key è associata a un `organization_id` tramite la variabile d'ambiente `API_KEYS` (JSON dict):

```bash
# .env
API_KEYS={"chiave-org1": 1, "chiave-org2": 2}
```

Tutti i risultati vengono automaticamente filtrati per l'organizzazione associata alla chiave utilizzata. Questo include corsi, utenti e tutte le risorse figlie (moduli, lezioni, sezioni, quiz).

```bash
curl -H "X-API-Key: chiave-org1" http://localhost:8000/api/v1/courses
```

### Risposte di errore autenticazione

**Header mancante** — `422 Unprocessable Entity`:
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["header", "x-api-key"],
      "msg": "Field required",
      "input": null
    }
  ]
}
```

**API key non valida** — `401 Unauthorized`:
```json
{
  "detail": "Invalid API key"
}
```

---

## Paginazione

Tutti gli endpoint che restituiscono liste supportano la paginazione tramite query parameter:

| Parametro | Tipo | Default | Descrizione |
|-----------|------|---------|-------------|
| `skip` | int | 0 | Numero di record da saltare |
| `limit` | int | 20 | Numero massimo di record da restituire (max: 100) |

**Esempio:**
```bash
curl -H "X-API-Key: la-tua-chiave" \
  "http://localhost:8000/api/v1/courses?skip=10&limit=5"
```

---

## Filtri

L'endpoint `/api/v1/courses` supporta i seguenti filtri:

| Parametro | Tipo | Descrizione | Valori esempio |
|-----------|------|-------------|----------------|
| `language` | string | Filtra per lingua del corso | `english`, `italian`, `spanish`, `german` |
| `course_type` | string | Filtra per tipologia di corso | `personal`, `organizational` |

**Esempio con filtri combinati:**
```bash
curl -H "X-API-Key: la-tua-chiave" \
  "http://localhost:8000/api/v1/courses?language=italian&course_type=personal&limit=5"
```

---

## Endpoint

### Corsi

#### `GET /api/v1/courses`

Restituisce la lista paginata dei corsi. Supporta filtri per `language` e `course_type`.

**Richiesta:**
```bash
curl -H "X-API-Key: la-tua-chiave" \
  "http://localhost:8000/api/v1/courses?limit=2"
```

**Risposta** — `200 OK`:
```json
[
  {
    "id": 1,
    "name": "Machine learning",
    "title": "Machine learning",
    "language": "english",
    "duration_minutes": 231,
    "banner_image_url": null,
    "slides_url": null,
    "slides_pdf_url": null,
    "creator_user_id": 1,
    "course_type": "personal",
    "created_at": "2025-12-16T02:21:44.758862",
    "updated_at": "2025-12-16T02:21:44.758931",
    "is_draft": null,
    "cfu": 0
  },
  {
    "id": 2,
    "name": "Machine Learning",
    "title": "Machine Learning",
    "language": "english",
    "duration_minutes": 115,
    "banner_image_url": "https://audios-avatar.s3.eu-north-1.amazonaws.com/audios/fe4b3124-91d0-4ac7-b912-89bd5a2f4d9d.png",
    "slides_url": null,
    "slides_pdf_url": null,
    "creator_user_id": 2,
    "course_type": "personal",
    "created_at": "2025-12-16T02:22:03.709718",
    "updated_at": "2025-12-16T02:22:03.709780",
    "is_draft": null,
    "cfu": 0
  }
]
```

**Con filtro per lingua:**
```bash
curl -H "X-API-Key: la-tua-chiave" \
  "http://localhost:8000/api/v1/courses?language=italian&limit=1"
```

```json
[
  {
    "id": 3,
    "name": "Machine learning2",
    "title": "Machine learning2",
    "language": "italian",
    "duration_minutes": 120,
    "banner_image_url": null,
    "slides_url": null,
    "slides_pdf_url": null,
    "creator_user_id": 1,
    "course_type": "personal",
    "created_at": "2025-12-16T10:24:34.235814",
    "updated_at": "2025-12-16T10:24:34.235876",
    "is_draft": null,
    "cfu": 0
  }
]
```

| Campo | Tipo | Descrizione |
|-------|------|-------------|
| `id` | int | Identificativo univoco del corso |
| `name` | string | Nome del corso |
| `title` | string \| null | Titolo del corso |
| `language` | string \| null | Lingua del corso |
| `duration_minutes` | int \| null | Durata totale in minuti |
| `banner_image_url` | string \| null | URL dell'immagine banner |
| `slides_url` | string \| null | URL delle slide |
| `slides_pdf_url` | string \| null | URL del PDF delle slide |
| `creator_user_id` | int \| null | ID dell'utente che ha creato il corso |
| `course_type` | string | Tipologia (`personal`, `organizational`) |
| `created_at` | datetime | Data di creazione |
| `updated_at` | datetime | Data di ultimo aggiornamento |
| `is_draft` | bool \| null | Se il corso è in bozza |
| `cfu` | int \| null | Crediti formativi universitari (CFU) |

---

#### `GET /api/v1/courses/{id}`

Restituisce il dettaglio di un singolo corso, inclusa la lista dei suoi moduli.

**Richiesta:**
```bash
curl -H "X-API-Key: la-tua-chiave" \
  http://localhost:8000/api/v1/courses/2
```

**Risposta** — `200 OK`:
```json
{
  "id": 2,
  "name": "Machine Learning",
  "title": "Machine Learning",
  "language": "english",
  "duration_minutes": 115,
  "banner_image_url": "https://audios-avatar.s3.eu-north-1.amazonaws.com/audios/fe4b3124-91d0-4ac7-b912-89bd5a2f4d9d.png",
  "slides_url": null,
  "slides_pdf_url": null,
  "creator_user_id": 2,
  "course_type": "personal",
  "created_at": "2025-12-16T02:22:03.709718",
  "updated_at": "2025-12-16T02:22:03.709780",
  "is_draft": null,
  "cfu": 0,
  "modules": [
    {
      "id": 6,
      "title": "Foundations of ML Algorithms",
      "duration_minutes": 20,
      "order": 0,
      "course_id": 2
    },
    {
      "id": 7,
      "title": "Classification and Regression Overview",
      "duration_minutes": 20,
      "order": 1,
      "course_id": 2
    },
    {
      "id": 8,
      "title": "Unsupervised Learning and Metrics",
      "duration_minutes": 35,
      "order": 2,
      "course_id": 2
    },
    {
      "id": 9,
      "title": "Theoretical ML: Algorithmic Concepts",
      "duration_minutes": 40,
      "order": 3,
      "course_id": 2
    }
  ]
}
```

**Corso non trovato** — `404 Not Found`:
```json
{
  "detail": "Course not found"
}
```

---

#### `GET /api/v1/courses/{id}/modules`

Restituisce la lista paginata dei moduli di un corso specifico, ordinati per campo `order`.

**Richiesta:**
```bash
curl -H "X-API-Key: la-tua-chiave" \
  http://localhost:8000/api/v1/courses/2/modules
```

**Risposta** — `200 OK`:
```json
[
  {
    "id": 6,
    "title": "Foundations of ML Algorithms",
    "duration_minutes": 20,
    "order": 0,
    "course_id": 2
  },
  {
    "id": 7,
    "title": "Classification and Regression Overview",
    "duration_minutes": 20,
    "order": 1,
    "course_id": 2
  },
  {
    "id": 8,
    "title": "Unsupervised Learning and Metrics",
    "duration_minutes": 35,
    "order": 2,
    "course_id": 2
  },
  {
    "id": 9,
    "title": "Theoretical ML: Algorithmic Concepts",
    "duration_minutes": 40,
    "order": 3,
    "course_id": 2
  }
]
```

| Campo | Tipo | Descrizione |
|-------|------|-------------|
| `id` | int | Identificativo univoco del modulo |
| `title` | string | Titolo del modulo |
| `duration_minutes` | int \| null | Durata in minuti |
| `order` | int \| null | Ordine di visualizzazione |
| `course_id` | int \| null | ID del corso di appartenenza |
| `created_at` | datetime | Data di creazione |
| `updated_at` | datetime | Data di ultimo aggiornamento |

---

### Moduli

#### `GET /api/v1/modules/{id}`

Restituisce il dettaglio di un modulo, inclusa la lista delle sue lezioni.

**Richiesta:**
```bash
curl -H "X-API-Key: la-tua-chiave" \
  http://localhost:8000/api/v1/modules/6
```

**Risposta** — `200 OK`:
```json
{
  "id": 6,
  "title": "Foundations of ML Algorithms",
  "duration_minutes": 20,
  "order": 0,
  "course_id": 2,
  "created_at": "2026-03-23T00:00:00",
  "updated_at": "2026-03-23T00:00:00",
  "lessons": [
    {
      "id": 7,
      "title": "Foundations of Machine Learning Theory",
      "objectives_json": "[\"Students will be able to define core machine learning concepts...\"]",
      "mandatory_topics_json": "[\"Origins and evolution of machine learning\", ...]",
      "duration_minutes": 20,
      "order": 0,
      "avatar_video_url": null,
      "mp4_video_url": null,
      "slides_pdf_url": "https://audios-avatar.s3.eu-north-1.amazonaws.com/.../slides.pdf.pdf",
      "slides_and_avatar_video_url": null,
      "slides_and_audio_video_url": "https://audios-avatar.s3.eu-north-1.amazonaws.com/.../slides_audio.mp4",
      "lesson_type": "CONTENT",
      "module_id": 6,
      "created_at": "2026-03-23T00:00:00",
      "updated_at": "2026-03-23T00:00:00"
    }
  ]
}
```

**Modulo non trovato** — `404 Not Found`:
```json
{
  "detail": "Module not found"
}
```

---

#### `GET /api/v1/modules/{id}/lessons`

Restituisce la lista paginata delle lezioni di un modulo, ordinate per campo `order`.

**Richiesta:**
```bash
curl -H "X-API-Key: la-tua-chiave" \
  "http://localhost:8000/api/v1/modules/6/lessons?limit=2"
```

**Risposta** — `200 OK`:
```json
[
  {
    "id": 7,
    "title": "Foundations of Machine Learning Theory",
    "objectives_json": "[\"Students will be able to define core machine learning concepts...\"]",
    "mandatory_topics_json": "[\"Origins and evolution of machine learning\", ...]",
    "duration_minutes": 20,
    "order": 0,
    "avatar_video_url": null,
    "mp4_video_url": null,
    "slides_pdf_url": "https://audios-avatar.s3.eu-north-1.amazonaws.com/.../slides.pdf.pdf",
    "slides_and_avatar_video_url": null,
    "slides_and_audio_video_url": "https://audios-avatar.s3.eu-north-1.amazonaws.com/.../slides_audio.mp4",
    "lesson_type": "CONTENT",
    "module_id": 6,
    "created_at": "2026-03-23T00:00:00",
    "updated_at": "2026-03-23T00:00:00"
  }
]
```

| Campo | Tipo | Descrizione |
|-------|------|-------------|
| `id` | int | Identificativo univoco della lezione |
| `title` | string | Titolo della lezione |
| `objectives_json` | string \| null | Obiettivi della lezione (JSON serializzato) |
| `mandatory_topics_json` | string \| null | Argomenti obbligatori (JSON serializzato) |
| `duration_minutes` | int \| null | Durata in minuti |
| `order` | int \| null | Ordine di visualizzazione |
| `avatar_video_url` | string \| null | URL del video con avatar AI |
| `mp4_video_url` | string \| null | URL del video MP4 |
| `slides_pdf_url` | string \| null | URL del PDF delle slide |
| `slides_and_avatar_video_url` | string \| null | URL del video slide + avatar |
| `slides_and_audio_video_url` | string \| null | URL del video slide + audio |
| `lesson_type` | string \| null | Tipologia della lezione (es. `CONTENT`) |
| `module_id` | int \| null | ID del modulo di appartenenza |
| `created_at` | datetime | Data di creazione |
| `updated_at` | datetime | Data di ultimo aggiornamento |

---

### Lezioni

#### `GET /api/v1/lessons/{id}`

Restituisce il dettaglio di una lezione, inclusa la lista delle sue sezioni, domande aperte e quiz.

**Richiesta:**
```bash
curl -H "X-API-Key: la-tua-chiave" \
  http://localhost:8000/api/v1/lessons/7
```

**Risposta** — `200 OK`:
```json
{
  "id": 7,
  "title": "Foundations of Machine Learning Theory",
  "objectives_json": "[\"Students will be able to define core machine learning concepts...\"]",
  "mandatory_topics_json": "[\"Origins and evolution of machine learning\", ...]",
  "duration_minutes": 20,
  "order": 0,
  "avatar_video_url": null,
  "mp4_video_url": null,
  "slides_pdf_url": "https://audios-avatar.s3.eu-north-1.amazonaws.com/.../slides.pdf.pdf",
  "slides_and_avatar_video_url": null,
  "slides_and_audio_video_url": "https://audios-avatar.s3.eu-north-1.amazonaws.com/.../slides_audio.mp4",
  "lesson_type": "CONTENT",
  "module_id": 6,
  "created_at": "2026-03-23T00:00:00",
  "updated_at": "2026-03-23T00:00:00",
  "sections": [
    {
      "id": 5,
      "uuid": "019106ee-9264-403c-8a6d-f4b73cb4ddba",
      "title": "Foundations of Machine Learning Concepts",
      "content": "Welcome, everyone! I'm glad you're here and ready to explore...",
      "duration_minutes": 3,
      "order": 0,
      "audio_url": "https://audios-avatar.s3.eu-north-1.amazonaws.com/audios/019106ee-...mp3",
      "audio_duration": 133.848,
      "raw_video_url": null,
      "avatar_video_url": null,
      "cloned_audio_url": null,
      "slides_and_avatar_video_url": null,
      "slide_audio_video_url": "https://audios-avatar.s3.eu-north-1.amazonaws.com/.../slides_audio.mp4",
      "section_pdf_url": null,
      "lesson_id": 7,
      "created_at": "2026-03-23T00:00:00",
      "updated_at": "2026-03-23T00:00:00"
    },
    {
      "id": 6,
      "uuid": "41ac959f-be37-4a3a-afb3-cb4f2900419e",
      "title": "Learning Paradigms and Terminology",
      "content": "Let's pick up where we left off and frame our discussion...",
      "duration_minutes": 3,
      "order": 1,
      "audio_url": "https://audios-avatar.s3.eu-north-1.amazonaws.com/audios/41ac959f-...mp3",
      "audio_duration": 152.856,
      "raw_video_url": null,
      "avatar_video_url": null,
      "cloned_audio_url": null,
      "slides_and_avatar_video_url": null,
      "slide_audio_video_url": "https://audios-avatar.s3.eu-north-1.amazonaws.com/.../slides_audio.mp4",
      "section_pdf_url": null,
      "lesson_id": 7,
      "created_at": "2026-03-23T00:00:00",
      "updated_at": "2026-03-23T00:00:00"
    }
  ]
}
```

**Lezione non trovata** — `404 Not Found`:
```json
{
  "detail": "Lesson not found"
}
```

---

#### `GET /api/v1/lessons/{id}/sections`

Restituisce la lista paginata delle sezioni di una lezione, ordinate per campo `order`.

**Richiesta:**
```bash
curl -H "X-API-Key: la-tua-chiave" \
  "http://localhost:8000/api/v1/lessons/7/sections?limit=2"
```

**Risposta** — `200 OK`:
```json
[
  {
    "id": 5,
    "uuid": "019106ee-9264-403c-8a6d-f4b73cb4ddba",
    "title": "Foundations of Machine Learning Concepts",
    "content": "Welcome, everyone! I'm glad you're here and ready to explore...",
    "duration_minutes": 3,
    "order": 0,
    "audio_url": "https://audios-avatar.s3.eu-north-1.amazonaws.com/audios/019106ee-...mp3",
    "audio_duration": 133.848,
    "raw_video_url": null,
    "avatar_video_url": null,
    "cloned_audio_url": null,
    "slides_and_avatar_video_url": null,
    "slide_audio_video_url": "https://audios-avatar.s3.eu-north-1.amazonaws.com/.../slides_audio.mp4",
    "section_pdf_url": null,
    "lesson_id": 7
  },
  {
    "id": 6,
    "uuid": "41ac959f-be37-4a3a-afb3-cb4f2900419e",
    "title": "Learning Paradigms and Terminology",
    "content": "Let's pick up where we left off...",
    "duration_minutes": 3,
    "order": 1,
    "audio_url": "https://audios-avatar.s3.eu-north-1.amazonaws.com/audios/41ac959f-...mp3",
    "audio_duration": 152.856,
    "raw_video_url": null,
    "avatar_video_url": null,
    "cloned_audio_url": null,
    "slides_and_avatar_video_url": null,
    "slide_audio_video_url": "https://audios-avatar.s3.eu-north-1.amazonaws.com/.../slides_audio.mp4",
    "section_pdf_url": null,
    "lesson_id": 7,
    "created_at": "2026-03-23T00:00:00",
    "updated_at": "2026-03-23T00:00:00"
  }
]
```

| Campo | Tipo | Descrizione |
|-------|------|-------------|
| `id` | int | Identificativo univoco della sezione |
| `uuid` | string | UUID univoco della sezione |
| `title` | string \| null | Titolo della sezione |
| `content` | string \| null | Contenuto testuale completo (script della lezione) |
| `duration_minutes` | int \| null | Durata in minuti |
| `order` | int \| null | Ordine di visualizzazione |
| `audio_url` | string \| null | URL dell'audio della sezione |
| `audio_duration` | float \| null | Durata dell'audio in secondi |
| `raw_video_url` | string \| null | URL del video raw |
| `avatar_video_url` | string \| null | URL del video con avatar AI |
| `cloned_audio_url` | string \| null | URL dell'audio clonato |
| `slides_and_avatar_video_url` | string \| null | URL del video slide + avatar |
| `slide_audio_video_url` | string \| null | URL del video slide + audio |
| `section_pdf_url` | string \| null | URL del PDF della sezione |
| `lesson_id` | int \| null | ID della lezione di appartenenza |
| `created_at` | datetime | Data di creazione |
| `updated_at` | datetime | Data di ultimo aggiornamento |

---

### Sezioni

#### `GET /api/v1/sections/{id}`

Restituisce il dettaglio di una sezione, inclusa la slide associata (relazione 1:1).

**Richiesta:**
```bash
curl -H "X-API-Key: la-tua-chiave" \
  http://localhost:8000/api/v1/sections/1
```

**Risposta** — `200 OK`:
```json
{
  "id": 1,
  "uuid": "c2eb9708-c1d2-40fb-bc48-5f5d2b65aef1",
  "title": "Foundations of Linear Models and Variants",
  "content": "Let's start by welcoming everyone warmly and setting the stage for what we'll explore today...",
  "duration_minutes": 5,
  "order": 0,
  "audio_url": null,
  "audio_duration": null,
  "raw_video_url": null,
  "avatar_video_url": null,
  "cloned_audio_url": null,
  "slides_and_avatar_video_url": null,
  "slide_audio_video_url": null,
  "section_pdf_url": null,
  "lesson_id": 8,
  "created_at": "2026-03-23T00:00:00",
  "updated_at": "2026-03-23T00:00:00",
  "slide": {
    "id": 8,
    "section_id": 1,
    "title": "Foundations of Linear Models",
    "type": "TEXT",
    "contents_json": "[\"Linear regression predicts a numerical outcome by assuming the response moves in a straight line...\", \"As you prepare data, scaling inputs helps penalties behave predictably...\"]",
    "created_at": "2026-03-23T00:00:00",
    "updated_at": "2026-03-23T00:00:00"
  }
}
```

**Sezione senza slide associata** — il campo `slide` sarà `null`:
```json
{
  "id": 123,
  "uuid": "...",
  "title": "...",
  "...": "...",
  "slide": null
}
```

**Sezione non trovata** — `404 Not Found`:
```json
{
  "detail": "Section not found"
}
```

| Campo Slide | Tipo | Descrizione |
|-------------|------|-------------|
| `id` | int | Identificativo univoco della slide |
| `section_id` | int | ID della sezione associata |
| `title` | string | Titolo della slide |
| `type` | string | Tipo di slide (es. `TEXT`) |
| `contents_json` | string \| null | Contenuto della slide (JSON serializzato) |
| `created_at` | datetime | Data di creazione |
| `updated_at` | datetime | Data di ultimo aggiornamento |

---

### Domande Aperte

#### `GET /api/v1/lessons/{id}/open-questions`

Restituisce la lista paginata delle domande aperte associate a una lezione.

**Richiesta:**
```bash
curl -H "X-API-Key: la-tua-chiave" \
  "http://localhost:8000/api/v1/lessons/249/open-questions?limit=2"
```

**Risposta** — `200 OK`:
```json
[
  {
    "id": 1,
    "question_text": "Analyze how the choice of tokenization granularity influences attention patterns...",
    "lesson_id": 249,
    "created_at": "2026-03-23T00:00:00",
    "updated_at": "2026-03-23T00:00:00"
  },
  {
    "id": 2,
    "question_text": "Design a small comparative study to evaluate BPE versus SentencePiece...",
    "lesson_id": 249,
    "created_at": "2026-03-23T00:00:00",
    "updated_at": "2026-03-23T00:00:00"
  }
]
```

| Campo | Tipo | Descrizione |
|-------|------|-------------|
| `id` | int | Identificativo univoco della domanda |
| `question_text` | string | Testo della domanda aperta |
| `lesson_id` | int \| null | ID della lezione di appartenenza |
| `created_at` | datetime | Data di creazione |
| `updated_at` | datetime | Data di ultimo aggiornamento |

---

### Quiz

#### `GET /api/v1/lessons/{id}/quizzes`

Restituisce la lista paginata dei quiz associati a una lezione.

**Richiesta:**
```bash
curl -H "X-API-Key: la-tua-chiave" \
  "http://localhost:8000/api/v1/lessons/249/quizzes"
```

**Risposta** — `200 OK`:
```json
[
  {
    "id": 1,
    "title": "Assessment Quiz - Foundations of Tokenization and GPT",
    "lesson_id": 249,
    "created_at": "2026-03-23T00:00:00",
    "updated_at": "2026-03-23T00:00:00"
  }
]
```

| Campo | Tipo | Descrizione |
|-------|------|-------------|
| `id` | int | Identificativo univoco del quiz |
| `title` | string | Titolo del quiz |
| `lesson_id` | int \| null | ID della lezione di appartenenza |
| `created_at` | datetime | Data di creazione |
| `updated_at` | datetime | Data di ultimo aggiornamento |

---

#### `GET /api/v1/quizzes/{id}`

Restituisce il dettaglio di un quiz, inclusa la lista delle sue domande.

**Richiesta:**
```bash
curl -H "X-API-Key: la-tua-chiave" \
  http://localhost:8000/api/v1/quizzes/1
```

**Risposta** — `200 OK`:
```json
{
  "id": 1,
  "title": "Assessment Quiz - Foundations of Tokenization and GPT",
  "lesson_id": 249,
  "created_at": "2026-03-23T00:00:00",
  "updated_at": "2026-03-23T00:00:00",
  "questions": [
    {
      "id": 1,
      "question_text": "Which statement best describes character-level tokenization compared to subword-level tokenization?",
      "difficulty": "EASY",
      "origin_lesson": 1,
      "quiz_id": 1,
      "created_at": "2026-03-23T00:00:00",
      "updated_at": "2026-03-23T00:00:00"
    }
  ]
}
```

**Quiz non trovato** — `404 Not Found`:
```json
{
  "detail": "Quiz not found"
}
```

---

#### `GET /api/v1/quizzes/{id}/questions`

Restituisce la lista paginata delle domande di un quiz.

**Richiesta:**
```bash
curl -H "X-API-Key: la-tua-chiave" \
  "http://localhost:8000/api/v1/quizzes/1/questions?limit=2"
```

**Risposta** — `200 OK`:
```json
[
  {
    "id": 1,
    "question_text": "Which statement best describes character-level tokenization compared to subword-level tokenization?",
    "difficulty": "EASY",
    "origin_lesson": 1,
    "quiz_id": 1,
    "created_at": "2026-03-23T00:00:00",
    "updated_at": "2026-03-23T00:00:00"
  }
]
```

| Campo | Tipo | Descrizione |
|-------|------|-------------|
| `id` | int | Identificativo univoco della domanda |
| `question_text` | string | Testo della domanda |
| `difficulty` | string | Difficoltà (`EASY`, `MEDIUM`, `HARD`) |
| `origin_lesson` | int \| null | ID della lezione di origine della domanda |
| `quiz_id` | int \| null | ID del quiz di appartenenza |
| `created_at` | datetime | Data di creazione |
| `updated_at` | datetime | Data di ultimo aggiornamento |

---

#### `GET /api/v1/questions/{id}`

Restituisce il dettaglio di una domanda di quiz, incluse le opzioni di risposta.

**Richiesta:**
```bash
curl -H "X-API-Key: la-tua-chiave" \
  http://localhost:8000/api/v1/questions/1
```

**Risposta** — `200 OK`:
```json
{
  "id": 1,
  "question_text": "Which statement best describes character-level tokenization compared to subword-level tokenization?",
  "difficulty": "EASY",
  "origin_lesson": 1,
  "quiz_id": 1,
  "created_at": "2026-03-23T00:00:00",
  "updated_at": "2026-03-23T00:00:00",
  "options": [
    {
      "id": 1,
      "option_text": "Character-level tokenization yields shorter sequences but loses ability to spell new words.",
      "is_correct": false,
      "quiz_question_id": 1,
      "created_at": "2026-03-23T00:00:00",
      "updated_at": "2026-03-23T00:00:00"
    },
    {
      "id": 2,
      "option_text": "Character-level tokenization yields longer sequences but can spell any word, including unseen ones.",
      "is_correct": true,
      "quiz_question_id": 1,
      "created_at": "2026-03-23T00:00:00",
      "updated_at": "2026-03-23T00:00:00"
    }
  ]
}
```

**Domanda non trovata** — `404 Not Found`:
```json
{
  "detail": "Question not found"
}
```

| Campo Opzione | Tipo | Descrizione |
|---------------|------|-------------|
| `id` | int | Identificativo univoco dell'opzione |
| `option_text` | string | Testo dell'opzione di risposta |
| `is_correct` | bool | Se l'opzione è la risposta corretta |
| `quiz_question_id` | int \| null | ID della domanda di appartenenza |
| `created_at` | datetime | Data di creazione |
| `updated_at` | datetime | Data di ultimo aggiornamento |

---

### Utenti

#### `GET /api/v1/users`

Restituisce la lista paginata degli utenti appartenenti all'organizzazione associata all'API key.

**Richiesta:**
```bash
curl -H "X-API-Key: la-tua-chiave" \
  "http://localhost:8000/api/v1/users?limit=2"
```

**Risposta** — `200 OK`:
```json
[
  {
    "id": 1,
    "email": "mario.rossi@email.com",
    "first_name": "Mario",
    "last_name": "Rossi",
    "phone": "+39123456789",
    "created_at": "2026-01-15T10:30:00",
    "updated_at": "2026-03-20T14:00:00"
  }
]
```

| Campo | Tipo | Descrizione |
|-------|------|-------------|
| `id` | int | Identificativo univoco dell'utente |
| `email` | string \| null | Email dell'utente |
| `first_name` | string \| null | Nome |
| `last_name` | string \| null | Cognome |
| `phone` | string \| null | Numero di telefono |
| `created_at` | datetime | Data di creazione |
| `updated_at` | datetime | Data di ultimo aggiornamento |

---

### Autenticazione Utente (Login)

#### `POST /api/v1/auth/login`

Verifica le credenziali di un utente tramite Clerk. Non richiede `X-API-Key`.

**Richiesta:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "mario.rossi@email.com", "password": "la-password"}'
```

**Credenziali corrette** — `200 OK`:
```json
{
  "status": "ok",
  "message": null
}
```

**Credenziali errate** — `200 OK`:
```json
{
  "status": "error",
  "message": "Invalid credentials"
}
```

| Campo | Tipo | Descrizione |
|-------|------|-------------|
| `status` | string | `"ok"` se autenticato, `"error"` altrimenti |
| `message` | string \| null | Messaggio di errore (null se ok) |

---

## Errori

L'API utilizza codici di stato HTTP standard:

| Codice | Descrizione | Quando |
|--------|-------------|--------|
| `200` | OK | Richiesta completata con successo |
| `401` | Unauthorized | API key non valida |
| `404` | Not Found | Risorsa non trovata |
| `422` | Unprocessable Entity | Header `X-API-Key` mancante o parametri non validi |

Tutte le risposte di errore seguono il formato:
```json
{
  "detail": "Messaggio di errore"
}
```

---

## Struttura del Progetto

```
avatar4universityAPI/
├── app/
│   ├── __init__.py
│   ├── main.py              # Entry point FastAPI, include routers e autenticazione
│   ├── config.py            # Configurazione da .env (API_KEYS, DATABASE_URL, CLERK_SECRET_KEY)
│   ├── database.py          # Engine SQLAlchemy e gestione sessioni
│   ├── auth.py              # Dependency di autenticazione tramite API key e scoping per organizzazione
│   ├── models/
│   │   ├── __init__.py
│   │   └── models.py        # Modelli ORM (Course, Module, Lesson, Section, Slide, OpenQuestion, Quiz, QuizQuestion, QuizOption, User, UserOrganization)
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── schemas.py       # Schemi Pydantic per le risposte
│   └── routers/
│       ├── __init__.py
│       ├── courses.py        # Endpoint corsi
│       ├── modules.py        # Endpoint moduli
│       ├── lessons.py        # Endpoint lezioni e domande aperte
│       ├── sections.py       # Endpoint sezioni
│       ├── quizzes.py        # Endpoint quiz e domande quiz
│       ├── users.py          # Endpoint lista utenti
│       └── auth.py           # Endpoint login (verifica password via Clerk)
├── add_timestamps.sql        # Migrazione timestamp per SQLite
├── add_timestamps_postgres.sql # Migrazione timestamp per PostgreSQL
├── .env.example              # Template variabili d'ambiente
├── .gitignore
├── requirements.txt
└── README.md
```
