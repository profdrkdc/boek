# De Lezer Ecosystem

Dit project is georganiseerd volgens een "Deep Ecosystem" structuur om maximale helderheid en schaalbaarheid te garanderen.

## 🏛️ De 7 Pijlers

### 00-GEREEDSCHAP
De "motor" van het project. Bevat de actieve tools voor productie.
- `nlm_venv/`: Python omgeving voor media-generatie (audio/video).

### 01-PLATFORM
Bevat de functionele applicatie en technische tools.
- `01-PLATFORM/`: De React/Vite applicatie.
- `01-PLATFORM/generate-book.js`: Script om manuscripten om te zetten naar app-data.

### 02-MANUSCRIPT
Het hart van het project. Bevat alle teksten en media.
- `01-Teksten/`: 
    - `01-Nederlands`: De menselijke Master-versie (Basis voor de site).
    - `02-English`: De menselijke Master-versie (Basis voor de site).
- `02-Media/`: 
    - `00-Productie-Assets`: AI-geoptimaliseerde versies voor media-generatie.
    - `Audio/`: NL en EN submappen.
    - `Beeld/`: Illustraties en assets.
    - `Video/`: NL en EN submappen.

### 03-STRATEGIE
Het fundament en de visie.
- `01-Manifest`: De 13 kernprincipes van het Ethisch Fundament.
- `02-Identiteit`: Huisstijl en design tokens.
- `03-Kern-Filosofie`: Diepgaande filosofische uitwerking (Sovereign Reality).

### 04-EVOLUTIE
De historische ontwikkeling van het project.
- `v1-Oorsprong`, `v2-Synthese`, `v3-Sovereign`.

### 05-ARCHIEF
Veilige opslag van legacy bestanden en technische logs.

### lessons-learned
Documentatie van ervaringen en lessen voor continue zelf-verbetering (Auto-Self-Improvement).
- Persoonlijke groei en project-specifieke lessen.

---

## 🚀 Aan de slag
Om de webapp te draaien:
1. `cd 01-PLATFORM`
2. `pnpm install`
3. `pnpm dev`

Om de data te verversen na tekstwijzigingen:
`node 01-PLATFORM/generate-book.js`
