import { useState, useEffect, useRef } from 'react';
import { queryDocumentation } from './services/api';
import LoadingSpinner from './components/LoadingSpinner.jsx';
import ExampleQuestions from './components/ExampleQuestions.jsx';
import ResponseDisplay from './components/ResponseDisplay.jsx';
import './App.css';

export default function App() {
  const [question, setQuestion] = useState('');
  const [response, setResponse] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [mounted, setMounted] = useState(false);
  const inputRef = useRef(null);
  const resultsRef = useRef(null);

  useEffect(() => {
    setMounted(true);
  }, []);

  const handleQuery = async (q) => {
    const queryText = q || question;
    if (!queryText.trim() || isLoading) return;

    setIsLoading(true);
    setError(null);
    setResponse(null);

    try {
      const data = await queryDocumentation(queryText);
      setResponse(data);
      setTimeout(() => resultsRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' }), 100);
    } catch (err) {
      setError(err.message || 'Failed to reach the API. Check your connection.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleExampleClick = (q) => {
    setQuestion(q);
    handleQuery(q);
  };

  const handleNewQuery = () => {
    setResponse(null);
    setQuestion('');
    inputRef.current?.focus();
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleQuery();
    }
  };

  return (
    <div className="app-container">
      <div className="grid-lines">
        {[...Array(8)].map((_, i) => (
          <div key={i} className="grid-line-v" style={{ left: `${(i + 1) * 12.5}%` }} />
        ))}
        {[...Array(6)].map((_, i) => (
          <div key={i} className="grid-line-h" style={{ top: `${(i + 1) * 16.66}%` }} />
        ))}
      </div>

      <div className="glow-orb" />

      <div className="content">

        {/* Header */}
        <header className={`header ${mounted ? 'visible' : ''}`}>
          <div className="header-badge">
            <div className="pulse-dot" />
            <span>UEFN Documentation Assistant</span>
          </div>
          <h1 className="header-title">
            Ask anything about{' '}
            <span className="header-gradient">Verse & UEFN</span>
          </h1>
          <p className="header-subtitle">
            Semantic search across 82 documentation pages — Verse language, API reference, tutorials, and patch notes.
          </p>
        </header>

        {/* Search Box */}
        <div className={`search-box ${mounted ? 'visible' : ''}`}>
          <div className="search-inner">
            <textarea
              ref={inputRef}
              value={question}
              onChange={e => setQuestion(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask about Verse syntax, UEFN devices, patch notes, API references..."
              rows={3}
              className="search-textarea"
            />
            <div className="search-footer">
              <span className="search-hint">ENTER to submit</span>
              <button
                onClick={() => handleQuery()}
                disabled={isLoading || !question.trim()}
                className="submit-btn"
              >
                QUERY →
              </button>
            </div>
          </div>
        </div>

        {/* Example Questions */}
        {!response && !isLoading && (
          <ExampleQuestions onQuestionClick={handleExampleClick} />
        )}

        {/* Loading */}
        {isLoading && <LoadingSpinner />}

        {/* Error */}
        {error && (
          <div className="error-box">
            <span className="error-label">ERROR</span>
            <span className="error-dash">—</span>
            {error}
          </div>
        )}

        {/* Response */}
        {response && (
          <div ref={resultsRef}>
            <ResponseDisplay response={response} onNewQuery={handleNewQuery} />
          </div>
        )}

        {/* Footer */}
        <footer className="footer">
          <span>UEFN RAG ASSISTANT</span>
          <span>82 DOCS · 159 CHUNKS · BEDROCK + PGVECTOR</span>
        </footer>

      </div>
    </div>
  );
}