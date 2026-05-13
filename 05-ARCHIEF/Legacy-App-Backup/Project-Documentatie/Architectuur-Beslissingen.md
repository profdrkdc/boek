# Architectuur Beslissingen - De Competente Lezer

## 1. Data Management & Meertaligheid (Maart 2026)

### Context
Het project ondersteunt meerdere versies van het boek (Origineel, Eenvoudig, AI-gegenereerd) en meerdere talen (Nederlands, Engels). De data moet efficiënt worden geladen in de online reader.

### Beslissing
Vooralsnog worden alle boekversies gebundeld in één enkel JSON-bestand: `src/data/book.json`.

### Redenatie
1. **Snelheid:** Omdat tekst (Markdown) extreem efficiënt comprimeert, is het totale bestand momenteel klein (~350 KB). Door alles in één keer te laden, kan de gebruiker onmiddellijk schakelen tussen talen en versies zonder laadtijd of extra netwerkverzoek.
2. **Eenvoud:** De huidige implementatie van `App.tsx` en `generate-book.js` binnen de `De-Lezer-App` map blijft hierdoor overzichtelijk en vereist geen complexe asynchrone loading states voor de content.

### Toekomstige Schaalbaarheid (Wanneer splitsen?)
Zodra het `book.json` bestand groter wordt dan **5 MB** (door bijv. 10+ talen of extreem lange manuscripten), moet de architectuur worden aangepast naar **Dynamic Loading**:

1. **Splitsen:** `generate-book.js` moet aangepast worden om aparte bestanden te genereren (bijv. `nl-original.json`, `en-original.json`).
2. **On-demand Fetching:** `App.tsx` moet de content ophalen (`fetch`) op het moment dat de gebruiker een andere versie selecteert in de dropdown.
3. **Caching:** Gebruik maken van browser caching of een state management library om reeds geladen versies te bewaren.

---
*Gedocumenteerd op: 3 maart 2026*
