import fs from 'fs/promises';
import path from 'path';
import { GoogleGenAI } from '@google/genai';

// Initialize the Google Gen AI client
// It automatically picks up the GEMINI_API_KEY from the environment
const ai = new GoogleGenAI({});

const DUTCH_DIR = '../02-MANUSCRIPT/01-Teksten/01-Nederlands';
const ENGLISH_DIR = '../02-MANUSCRIPT/01-Teksten/02-English';

const FOLDER_TRANSLATIONS = {
    'H01_Inleiding': 'H01_Introduction',
    'H02_De-Mens-als-Instrument': 'H02_Man-as-Instrument',
    'H03_De-Anatomie-van-Incompetentie': 'H03_The-Anatomy-of-Incompetence',
    'H04_De-Dierlijke-Erfenis': 'H04_The-Animal-Legacy',
    'H05_Hierarchie-van-Competentie': 'H05_Hierarchy-of-Competence',
    'H06_De-Maakbare-Mens-en-AI': 'H06_The-Malleable-Man-and-AI',
    'H07_Het-Masterplan': 'H07_The-Masterplan',
    'H08_Nawoord': 'H08_Afterword'
};

async function translateText(text) {
    const prompt = `You are a professional translator and a deep philosophical thinker.
Translate the following text from Dutch to English.
CRITICAL INSTRUCTIONS:
- Preserve the exact markdown formatting (headings, bold, italics, bullet points).
- Maintain the deeply authoritative, philosophical, and "human" tone of the original text.
- Do NOT add any extra commentary, greetings, or conclusions. Output ONLY the translated text.
- The tone should read as a definitive manifesto on the nature of reality, human limitations, and the necessity of structural alignment.

TEXT TO TRANSLATE:
${text}`;

    try {
        const response = await ai.models.generateContent({
            model: 'gemini-pro-latest',
            contents: prompt,
            config: {
                temperature: 0.2
            }
        });

        // Strict Gemini 3.0 Compliance parsing
        const parts = response.candidates?.[0]?.content?.parts || [];
        const textPart = parts.find(p => p.text);
        const translatedText = textPart ? textPart.text : (response.text ? response.text() : "");

        return translatedText;
    } catch (error) {
        console.error("Error during translation:", error);
        return null;
    }
}

async function processDirectory() {
    try {
        const folders = await fs.readdir(DUTCH_DIR);
        
        for (const folder of folders) {
            const folderPath = path.join(DUTCH_DIR, folder);
            const stat = await fs.stat(folderPath);
            
            if (stat.isDirectory()) {
                const targetFolderName = FOLDER_TRANSLATIONS[folder] || folder;
                const targetFolderPath = path.join(ENGLISH_DIR, targetFolderName);
                
                await fs.mkdir(targetFolderPath, { recursive: true });
                console.log(`Created folder: ${targetFolderPath}`);
                
                const files = await fs.readdir(folderPath);
                
                for (const file of files) {
                    if (file.endsWith('.md')) {
                        const filePath = path.join(folderPath, file);
                        const content = await fs.readFile(filePath, 'utf-8');
                        
                        console.log(`Translating: ${folder}/${file}...`);
                        const translatedContent = await translateText(content);
                        
                        if (translatedContent) {
                            // Translate the filename too
                            const translatedFilename = file
                                .replace('Onze-Werkelijkheid', 'Our-Reality')
                                .replace('Symptoombestrijding', 'Symptom-Management')
                                .replace('Illusie-van-Controle', 'Illusion-of-Control')
                                .replace('Mechanismen-van-Lijden', 'Mechanisms-of-Suffering')
                                .replace('Noodzaak-van-Orde', 'Necessity-of-Order')
                                .replace('Geboorte-van-Sovereign-Reality', 'Birth-of-Sovereign-Reality')
                                .replace('Uitvoering', 'Execution')
                                .replace('Slot', 'Conclusion');
                                
                            const targetFilePath = path.join(targetFolderPath, translatedFilename);
                            await fs.writeFile(targetFilePath, translatedContent);
                            console.log(`Saved: ${targetFilePath}`);
                        }
                    }
                }
            }
        }
        console.log("Translation complete!");
    } catch (error) {
        console.error("Fatal error processing directory:", error);
    }
}

processDirectory();
