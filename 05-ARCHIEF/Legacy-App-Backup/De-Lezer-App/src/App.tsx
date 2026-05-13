import { useState, useEffect, useRef } from 'react'
import ReactMarkdown from 'react-markdown'
import bookData from './data/book.json'
import { BookOpen, MessageSquare, ChevronLeft, ChevronRight, Send, Loader2 } from 'lucide-react'
import { askArchitect } from './lib/architect'

interface Message {
  role: 'user' | 'architect';
  text: string;
}

function App() {
  const [version, setVersion] = useState('nl-original')
  const [currentChapterIndex, setCurrentChapterIndex] = useState(0)
  const [showChat, setShowChat] = useState(true)
  const [messages, setMessages] = useState<Message[]>([])
  const [inputValue, setInputValue] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [systemPrompt, setSystemPrompt] = useState('')
  const [systemPromptEn, setSystemPromptEn] = useState('')
  
  const chatEndRef = useRef<HTMLDivElement>(null)
  const currentBook = (bookData as any)[version]
  const currentChapter = currentBook.chapters[currentChapterIndex] || { title: 'Geen inhoud', content: 'Deze versie heeft nog geen inhoud.' }

  useEffect(() => {
    fetch('/system_prompt.md')
      .then(res => res.text())
      .then(setSystemPrompt)
    fetch('/system_prompt_en.md')
      .then(res => res.text())
      .then(setSystemPromptEn)
  }, [])

  useEffect(() => {
    const greeting = version.startsWith('en') 
      ? 'Hello. I am the Architect. I have read the manuscript. If you have any questions about this text, or how you can apply it, feel free to ask.'
      : 'Hallo. Ik ben de Architect. Ik heb het manuscript gelezen. Als je vragen hebt over deze tekst, of hoe je dit kunt toepassen, stel ze gerust.';
    
    setMessages([{ role: 'architect', text: greeting }]);
  }, [version])

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const handleSend = async () => {
    if (!inputValue.trim() || isLoading) return

    const userMessage = inputValue.trim()
    setMessages(prev => [...prev, { role: 'user', text: userMessage }])
    setInputValue('')
    setIsLoading(true)

    const currentSystemPrompt = version.startsWith('en') ? systemPromptEn : systemPrompt
    const response = await askArchitect(userMessage, currentChapter.content, currentSystemPrompt)
    
    setMessages(prev => [...prev, { role: 'architect', text: response }])
    setIsLoading(false)
  }

  return (
    <div className="flex h-screen w-screen bg-slate-950 text-slate-200 overflow-hidden font-sans">
      {/* Sidebar - Navigation */}
      <div className="w-64 bg-slate-900 border-r border-slate-800 flex flex-col shrink-0">
        <div className="p-6 border-b border-slate-800 flex items-center gap-3">
          <div className="bg-blue-600 p-1.5 rounded-lg">
            <BookOpen size={20} className="text-white" />
          </div>
          <h1 className="font-bold text-lg tracking-tight">De Architect</h1>
        </div>
        
        {/* Version Selector */}
        <div className="p-4 border-b border-slate-800 bg-slate-900/50">
          <div className="text-[10px] uppercase tracking-widest text-slate-500 mb-2 font-bold px-1">Versie / Taal</div>
          <select 
            value={version} 
            onChange={(e) => {
              setVersion(e.target.value);
              setCurrentChapterIndex(0);
            }}
            className="w-full bg-slate-800 text-sm border border-slate-700 rounded-xl p-2.5 focus:outline-none focus:ring-2 focus:ring-blue-600/50 transition-all appearance-none cursor-pointer"
          >
            <option value="nl-original">Nederlands (Origineel)</option>
            <option value="nl-simple">Nederlands (Eenvoudig)</option>
            <option value="nl-ai">Nederlands (AI)</option>
            <option value="en-original">English (Original)</option>
          </select>
        </div>

        <div className="flex-1 overflow-y-auto p-3 space-y-1">
          {currentBook.chapters.map((chap: any, idx: number) => (
            <button
              key={chap.id}
              onClick={() => setCurrentChapterIndex(idx)}
              className={`w-full text-left p-3 rounded-xl transition-all duration-200 ${
                idx === currentChapterIndex 
                  ? 'bg-blue-600/10 text-blue-400 border border-blue-600/20 shadow-[0_0_15px_rgba(37,99,235,0.1)]' 
                  : 'hover:bg-slate-800/50 text-slate-400 border border-transparent'
              }`}
            >
              <div className="text-[10px] uppercase tracking-widest opacity-50 mb-1 font-bold">
                {version.startsWith('en') ? 'Chapter' : 'Hoofdstuk'} {idx + 1}
              </div>
              <div className="text-sm font-semibold truncate">{chap.title}</div>
            </button>
          ))}
          {currentBook.chapters.length === 0 && (
            <div className="p-4 text-sm text-slate-500 italic text-center">
              {version.startsWith('en') ? 'No chapters found for this version.' : 'Geen hoofdstukken gevonden voor deze versie.'}
            </div>
          )}
        </div>
      </div>

      {/* Main Content - Reader */}
      <div className="flex-1 flex flex-col bg-[#020617] relative">
        <header className="h-16 border-b border-slate-800/50 flex items-center justify-between px-8 bg-slate-950/20 backdrop-blur-xl z-10">
          <div className="flex items-center gap-6">
            <div className="flex items-center gap-2">
              <button 
                disabled={currentChapterIndex === 0}
                onClick={() => setCurrentChapterIndex(prev => prev - 1)}
                className="p-2 hover:bg-slate-800 rounded-lg disabled:opacity-20 transition-colors"
              >
                <ChevronLeft size={20} />
              </button>
              <button 
                disabled={currentChapterIndex === currentBook.chapters.length - 1 || currentBook.chapters.length === 0}
                onClick={() => setCurrentChapterIndex(prev => prev + 1)}
                className="p-2 hover:bg-slate-800 rounded-lg disabled:opacity-20 transition-colors"
              >
                <ChevronRight size={20} />
              </button>
            </div>
            <span className="text-xs font-bold tracking-widest text-slate-500 uppercase">
              {currentChapter.title}
            </span>
          </div>
          <button 
            onClick={() => setShowChat(!showChat)}
            className={`flex items-center gap-2 px-4 py-2 rounded-full text-xs font-bold uppercase tracking-wider transition-all ${
              showChat ? 'bg-blue-600 text-white shadow-lg shadow-blue-600/20' : 'bg-slate-800 text-slate-400 hover:bg-slate-700'
            }`}
          >
            <MessageSquare size={14} />
            <span>{showChat ? (version.startsWith('en') ? 'Close Architect' : 'Sluit Architect') : (version.startsWith('en') ? 'Open Architect' : 'Open Architect')}</span>
          </button>
        </header>

        <main className="flex-1 overflow-y-auto p-12 lg:p-20 scroll-smooth">
          <div className="max-w-2xl mx-auto">
            <article className="prose prose-invert prose-slate prose-headings:text-white prose-headings:font-bold prose-p:text-slate-300 prose-p:leading-relaxed prose-p:text-lg prose-strong:text-blue-400 prose-blockquote:border-blue-600 prose-blockquote:bg-blue-600/5 prose-blockquote:py-1 prose-blockquote:px-6 prose-blockquote:rounded-r-lg">
              <ReactMarkdown>{currentChapter.content}</ReactMarkdown>
            </article>
            <div className="h-24" /> {/* Spacer */}
          </div>
        </main>
      </div>

      {/* Chat Sidebar - The Architect */}
      {showChat && (
        <div className="w-[450px] bg-slate-900 border-l border-slate-800 flex flex-col shadow-2xl z-20">
          <div className="p-5 border-b border-slate-800/50 flex items-center justify-between bg-slate-900/50 backdrop-blur">
            <div className="flex items-center gap-3">
              <div className="relative">
                <div className="w-10 h-10 rounded-full bg-gradient-to-tr from-blue-600 to-indigo-500 flex items-center justify-center text-white font-black shadow-lg">A</div>
                <div className="absolute bottom-0 right-0 w-3 h-3 bg-green-500 border-2 border-slate-900 rounded-full"></div>
              </div>
              <div>
                <div className="font-bold text-sm tracking-tight">{version.startsWith('en') ? 'The Architect' : 'De Architect'}</div>
                <div className="text-[10px] text-slate-500 uppercase tracking-widest font-black">Expert Systeem v3.0</div>
              </div>
            </div>
          </div>
          
          <div className="flex-1 overflow-y-auto p-6 space-y-6 bg-slate-900/30">
            {messages.map((msg, i) => (
              <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                <div className={`max-w-[85%] p-4 rounded-2xl text-sm leading-relaxed shadow-sm ${
                  msg.role === 'user' 
                    ? 'bg-blue-600 text-white rounded-tr-none' 
                    : 'bg-slate-800 text-slate-200 rounded-tl-none border border-slate-700/50'
                }`}>
                  {msg.text}
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="flex justify-start">
                <div className="bg-slate-800 p-4 rounded-2xl rounded-tl-none border border-slate-700/50">
                  <Loader2 className="animate-spin text-blue-500" size={18} />
                </div>
              </div>
            )}
            <div ref={chatEndRef} />
          </div>

          <div className="p-6 border-t border-slate-800/50 bg-slate-900">
            <form 
              onSubmit={(e) => { e.preventDefault(); handleSend(); }}
              className="relative group"
            >
              <input 
                type="text" 
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                placeholder={version.startsWith('en') ? "Ask a question about this chapter..." : "Stel een vraag over dit hoofdstuk..."}
                className="w-full bg-slate-850 border border-slate-700/50 rounded-2xl py-4 pl-5 pr-14 text-sm focus:outline-none focus:ring-2 focus:ring-blue-600/50 focus:border-blue-600/50 transition-all bg-slate-800/50 group-hover:bg-slate-800"
              />
              <button 
                type="submit"
                disabled={!inputValue.trim() || isLoading}
                className="absolute right-2 top-2 p-2.5 bg-blue-600 text-white rounded-xl hover:bg-blue-500 transition-all disabled:opacity-20 disabled:grayscale shadow-lg shadow-blue-600/20"
              >
                <Send size={18} />
              </button>
            </form>
            <div className="mt-4 text-[9px] text-center text-slate-600 uppercase tracking-[0.2em] font-bold">
              {version.startsWith('en') ? 'Cognitive Interface • The Competent Future' : 'Cognitieve Interface • De Competente Toekomst'}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default App
