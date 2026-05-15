// Dit is de bridge naar de Gemini API
const API_KEY = "JOUW_GEMINI_API_KEY_HIER"; // Vul dit later in in Google AI Studio
const MODEL_NAME = "gemini-3.0-flash"; // Of gemini-2.0-flash afhankelijk van je toegang

export async function askArchitect(question: string, chapterContent: string, systemPrompt: string) {
  if (API_KEY === "JOUW_GEMINI_API_KEY_HIER") {
    return "Systeemmelding: Geen API-sleutel gevonden. Configureer je API-sleutel in src/lib/architect.ts om met de Architect te praten.";
  }

  const prompt = `
    ${systemPrompt}

    HUIDIGE CONTEXT (Het hoofdstuk dat de gebruiker nu leest):
    ---
    ${chapterContent}
    ---

    GEBRUIKER VRAAGT: ${question}
  `;

  try {
    const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/${MODEL_NAME}:generateContent?key=${API_KEY}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        contents: [{ parts: [{ text: prompt }] }],
      }),
    });

    const data = await response.json();
    return data.candidates[0].content.parts[0].text;
  } catch (error) {
    console.error("Architect Error:", error);
    return "Er is een systeemfout opgetreden bij het raadplegen van de Architect.";
  }
}
