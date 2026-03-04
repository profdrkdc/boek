import fs from 'fs';
import path from 'path';

const BASE_DIRS = {
    'nl-ai': '../02-AI-Gegenereerd/Het-Boek-AI',
    'nl-simple': '../01-Manueel-Manuscript/Het-Boek-Eenvoudig',
    'nl-original': '../01-Manueel-Manuscript/Het-Boek-Origineel',
    'en-original': '../01-Manueel-Manuscript/The-Book-EN'
};

const OUTPUT_FILE = './src/data/book.json';

function getChapters(manuscriptDir) {
    if (!fs.existsSync(manuscriptDir)) {
        console.warn(`Directory not found: ${manuscriptDir}`);
        return [];
    }
    const chapters = [];
    const entries = fs.readdirSync(manuscriptDir).filter(f => fs.statSync(path.join(manuscriptDir, f)).isDirectory());

    // Sort chapters by name (Hoofdstuk-1, Chapter-1, etc.)
    entries.sort((a, b) => {
        const getNum = (s) => {
            const match = s.match(/\d+/);
            return match ? parseInt(match[0]) : 999;
        };
        // Special case for Nawoord/Epilogue
        if (a.toLowerCase().includes('nawoord') || a.toLowerCase().includes('epiloog')) return 1;
        if (b.toLowerCase().includes('nawoord') || b.toLowerCase().includes('epiloog')) return -1;
        return getNum(a) - getNum(b);
    }).forEach(dir => {
        const chapterPath = path.join(manuscriptDir, dir);
        const files = fs.readdirSync(chapterPath).filter(f => f.endsWith('.md'));
        
        let content = '';
        files.sort().forEach(file => {
            content += fs.readFileSync(path.join(chapterPath, file), 'utf-8') + '\n\n';
        });

        chapters.push({
            id: dir,
            title: dir.replace(/_/g, ' '),
            content: content.trim()
        });
    });

    return chapters;
}

const multiBookData = {};

for (const [key, dir] of Object.entries(BASE_DIRS)) {
    console.log(`Processing ${key} from ${dir}...`);
    multiBookData[key] = {
        title: key.startsWith('en') ? "The Competent Future" : "De Competente Toekomst",
        author: "Karel",
        chapters: getChapters(dir)
    };
}

if (!fs.existsSync('./src/data')) {
    fs.mkdirSync('./src/data', { recursive: true });
}

fs.writeFileSync(OUTPUT_FILE, JSON.stringify(multiBookData, null, 2));
console.log('Multi-book data generated successfully at', OUTPUT_FILE);
