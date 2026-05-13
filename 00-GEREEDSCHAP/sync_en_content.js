import fs from 'fs';
import path from 'path';

const BOOK_PATH = '/home/kareltestspecial/0-boek/01-PLATFORM/src/data/book.json';
const MANUSCRIPT_ROOT = '/home/kareltestspecial/0-boek/02-MANUSCRIPT/02-Media/00-Productie-Assets/EN';

const mapping = [
  {
    sectionIndex: 0,
    files: ['Chapter-1/01_Our-Reality.md']
  },
  {
    sectionIndex: 1,
    files: [
      'Chapter-2/01_The-Shared-Ground-of-Ethics.md',
      'Chapter-2/02_The-Human-as-Instrument.md',
      'Chapter-2/03_From-Salvation-to-Responsibility.md'
    ]
  },
  {
    sectionIndex: 2,
    files: [
      'Chapter-3/01_Definition-of-Incompetence.md',
      'Chapter-3/02_Cognitive-Pitfalls.md',
      'Chapter-3/03_Emotional-Barriers.md',
      'Chapter-3/04_Conclusion-Internal-Enemy.md'
    ]
  },
  {
    sectionIndex: 3,
    files: [
      'Chapter-4/01_The-Animal-Heritage.md',
      'Chapter-4/02_Sexuality-as-Primary-Distraction.md',
      'Chapter-4/03_Other-Impulses-and-Self-Transcendence.md'
    ]
  },
  {
    sectionIndex: 4,
    files: [
      'Chapter-5/01_The-Functional-Principle.md',
      'Chapter-5/02_The-Duty-of-the-Competent.md',
      'Chapter-5/03_The-Role-of-the-Rest.md'
    ]
  },
  {
    sectionIndex: 5,
    files: [
      'Chapter-6/01_The-Foundation-Reason-and-Science.md',
      'Chapter-6/02_The-Next-Frontier-The-Human-Itself.md',
      'Chapter-6/03_Vision-of-the-Future.md'
    ]
  },
  {
    sectionIndex: 6,
    files: ['Chapter-7/01_The-Masterplan.md']
  },
  {
    sectionIndex: 7,
    files: ['Afterword/Epilogue.md']
  }
];

function extractTitle(content, fileName) {
  let title = 'Untitled';
  const h1Match = content.match(/^# (.*)/m);
  if (h1Match) {
    title = h1Match[1];
  } else {
    const h2Match = content.match(/^## (.*)/m);
    if (h2Match) title = h2Match[1];
  }
  
  // Clean up: Remove "Chapter X: " or "Section X: " (case insensitive)
  title = title.replace(/^(Chapter|Section|Hfdst|Deel|Part)\s*\d+[:\s-]* /i, '');
  
  // Clean up: Remove leading numbers like "1. ", "2) ", "3: ", "4.1 " etc.
  title = title.replace(/^[\d\.]+[.:\)\s-]+/, '');

  // Clean up: Remove "The First/Second/Third/etc. Barrier: "
  title = title.replace(/^The (First|Second|Third|Fourth|Fifth|Sixth) Barrier:\s*/i, '');

  // Clean up: Remove "Conclusion: "
  title = title.replace(/^Conclusion:\s*/i, '');

  // Special case for "The world we live in..." -> "Our Reality"
  if (title.toLowerCase().startsWith("the world we live in is not perfect")) {
    title = "Our Reality";
  }

  // Fallback for Untitled or too generic
  if (title === 'Untitled' || title.toLowerCase() === 'introduction') {
    const base = path.basename(fileName, '.md').replace(/_/g, ' ').replace(/-/g, ' ');
    title = base.replace(/^\d+[\s_-]*/, '').split(' ').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
  }

  return title.trim();
}

function run() {
  const book = JSON.parse(fs.readFileSync(BOOK_PATH, 'utf8'));
  
  mapping.forEach(({ sectionIndex, files }) => {
    const section = book.en.sections[sectionIndex];
    section.chapters = files.map(file => {
      const filePath = path.join(MANUSCRIPT_ROOT, file);
      const content = fs.readFileSync(filePath, 'utf8');
      let title = extractTitle(content, file);
      
      // If title is redundant with section, try sub-header
      if (title.toLowerCase() === section.title.toLowerCase()) {
        const h2Match = content.match(/^## (.*)/m);
        if (h2Match) {
          title = extractTitle(h2Match[0], file);
        }
      }
      
      return {
        id: `EN/${file}`,
        title: title,
        content: content
      };
    });
  });

  fs.writeFileSync(BOOK_PATH, JSON.stringify(book, null, 2));
  console.log('Successfully updated book.json with cleaned English content');
}

run();
