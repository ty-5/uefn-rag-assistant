import React from 'react';

const EXAMPLE_QUESTIONS = [
  "What is the syntax for a timer in Verse?",
  "How do I use creative_prop_asset?",
  "What changed in the latest UEFN patch notes?",
  "How do I handle player elimination events?",
  "What are the available movement functions in Verse?",
  "How do I create a custom device in UEFN?",
  "What is the difference between weak_map and map in Verse?",
  "How do I reference a spawner device in Verse code?",
];

export default function ExampleQuestions({ onQuestionClick }) {
  return (
    <div style={{ marginTop: '32px' }}>
      <div style={{
        fontFamily: "'JetBrains Mono', monospace",
        fontSize: '10px',
        color: 'rgba(255,255,255,0.25)',
        letterSpacing: '0.15em',
        marginBottom: '12px',
      }}>
        EXAMPLE QUERIES
      </div>
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))',
        gap: '8px',
      }}>
        {EXAMPLE_QUESTIONS.map((q, i) => (
          <button
            key={i}
            onClick={() => onQuestionClick(q)}
            style={{
              background: 'rgba(255,255,255,0.02)',
              border: '1px solid rgba(255,255,255,0.07)',
              borderRadius: '4px',
              padding: '10px 14px',
              textAlign: 'left',
              color: 'rgba(255,255,255,0.5)',
              fontFamily: "'JetBrains Mono', monospace",
              fontSize: '12px',
              lineHeight: '1.5',
              cursor: 'pointer',
              transition: 'all 0.15s ease',
            }}
            onMouseEnter={e => {
              e.currentTarget.style.background = 'rgba(0,212,255,0.08)';
              e.currentTarget.style.borderColor = 'rgba(0,212,255,0.3)';
              e.currentTarget.style.color = 'rgba(255,255,255,0.9)';
            }}
            onMouseLeave={e => {
              e.currentTarget.style.background = 'rgba(255,255,255,0.02)';
              e.currentTarget.style.borderColor = 'rgba(255,255,255,0.07)';
              e.currentTarget.style.color = 'rgba(255,255,255,0.5)';
            }}
          >
            <span style={{ color: 'rgba(0,212,255,0.5)', marginRight: '6px' }}>▸</span>
            {q}
          </button>
        ))}
      </div>
    </div>
  );
}