import fs from 'fs';
import path from 'path';

const MANUSCRIPT_DIR = '../DeCompetenteToekomst_Manuscript';
const OUTPUT_FILE = './src/data/book.json';

function getChapters() {
    const chapters = [];
    const dirs = fs.readdirSync(MANUSCRIPT_DIR).filter(f => fs.statSync(path.join(MANUSCRIPT_DIR, f)).isDirectory());

    dirs.sort().forEach(dir => {
        const chapterPath = path.join(MANUSCRIPT_DIR, dir);
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

const bookData = {
    title: "De Competente Toekomst",
    author: "Karel",
    chapters: getChapters()
};

if (!fs.existsSync('./src/data')) {
    fs.mkdirSync('./src/data', { recursive: true });
}

fs.writeFileSync(OUTPUT_FILE, JSON.stringify(bookData, null, 2));
console.log('Book data generated successfully at', OUTPUT_FILE);
