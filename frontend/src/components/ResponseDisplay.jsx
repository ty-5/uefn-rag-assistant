import React from 'react';

const CATEGORY_COLORS = {
  'verse-language': '#00d4ff',
  'api-reference': '#a78bfa',
  'tutorial': '#34d399',
  'patch-notes': '#fbbf24',
  'troubleshooting': '#f87171',
};

const CATEGORY_LABELS = {
  'verse-language': 'VERSE',
  'api-reference': 'API REF',
  'tutorial': 'TUTORIAL',
  'patch-notes': 'PATCH',
  'troubleshooting': 'TROUBLESHOOT',
};

function renderInline(text) {
  const parts = text.split(/(`[^`]+`|\*\*[^*]+\*\*)/g);
  return parts.map((part, i) => {
    if (part.startsWith('`') && part.endsWith('`')) {
      return (
        <code key={i} style={{
          fontFamily: "'JetBrains Mono', monospace",
          fontSize: '12px',
          background: 'rgba(0,212,255,0.1)',
          color: '#00d4ff',
          padding: '1px 5px',
          borderRadius: '3px',
        }}>
          {part.slice(1, -1)}
        </code>
      );
    }
    if (part.startsWith('**') && part.endsWith('**')) {
      return (
        <strong key={i} style={{ color: 'rgba(255,255,255,0.95)', fontWeight: '600' }}>
          {part.slice(2, -2)}
        </strong>
      );
    }
    return part;
  });
}

function MarkdownAnswer({ text }) {
  const lines = text.split('\n');
  const elements = [];
  let i = 0;
  let keyCounter = 0;

  while (i < lines.length) {
    const line = lines[i];

    if (line.startsWith('```')) {
      const lang = line.slice(3).trim() || 'verse';
      const codeLines = [];
      i++;
      while (i < lines.length && !lines[i].startsWith('```')) {
        codeLines.push(lines[i]);
        i++;
      }
      elements.push(
        <div key={keyCounter++} style={{
          background: 'rgba(0,0,0,0.4)',
          border: '1px solid rgba(255,255,255,0.1)',
          borderRadius: '4px',
          padding: '14px 16px',
          margin: '12px 0',
          overflowX: 'auto',
        }}>
          <div style={{
            fontSize: '9px',
            fontFamily: "'JetBrains Mono', monospace",
            color: '#00d4ff',
            marginBottom: '8px',
            letterSpacing: '0.1em',
            textTransform: 'uppercase',
          }}>{lang}</div>
          <pre style={{
            margin: 0,
            fontFamily: "'JetBrains Mono', monospace",
            fontSize: '13px',
            lineHeight: '1.6',
            color: '#e2e8f0',
          }}>{codeLines.join('\n')}</pre>
        </div>
      );
    } else if (line.startsWith('### ')) {
      elements.push(
        <h3 key={keyCounter++} style={{
          fontSize: '14px', fontWeight: '700', color: '#00d4ff',
          margin: '16px 0 6px', fontFamily: "'JetBrains Mono', monospace",
          letterSpacing: '0.05em',
        }}>{line.slice(4)}</h3>
      );
    } else if (line.startsWith('## ')) {
      elements.push(
        <h2 key={keyCounter++} style={{
          fontSize: '15px', fontWeight: '700', color: '#00d4ff',
          margin: '18px 0 8px', fontFamily: "'JetBrains Mono', monospace",
          letterSpacing: '0.05em',
        }}>{line.slice(3)}</h2>
      );
    } else if (line.startsWith('- ') || line.startsWith('* ')) {
      elements.push(
        <div key={keyCounter++} style={{ display: 'flex', gap: '8px', margin: '3px 0', paddingLeft: '4px' }}>
          <span style={{ color: '#00d4ff', flexShrink: 0, marginTop: '1px' }}>▸</span>
          <span style={{ fontSize: '14px', lineHeight: '1.6', color: 'rgba(255,255,255,0.8)' }}>
            {renderInline(line.slice(2))}
          </span>
        </div>
      );
    } else if (line.match(/^\d+\. /)) {
      const num = line.match(/^(\d+)\. /)[1];
      elements.push(
        <div key={keyCounter++} style={{ display: 'flex', gap: '10px', margin: '3px 0', paddingLeft: '4px' }}>
          <span style={{
            color: '#00d4ff', flexShrink: 0,
            fontFamily: "'JetBrains Mono', monospace",
            fontSize: '12px', minWidth: '16px',
          }}>{num}.</span>
          <span style={{ fontSize: '14px', lineHeight: '1.6', color: 'rgba(255,255,255,0.8)' }}>
            {renderInline(line.replace(/^\d+\. /, ''))}
          </span>
        </div>
      );
    } else if (line.trim() === '') {
      elements.push(<div key={keyCounter++} style={{ height: '6px' }} />);
    } else {
      elements.push(
        <p key={keyCounter++} style={{
          fontSize: '14px', lineHeight: '1.75',
          color: 'rgba(255,255,255,0.82)', margin: '4px 0',
        }}>
          {renderInline(line)}
        </p>
      );
    }
    i++;
  }

  return <div>{elements}</div>;
}

function SourceCard({ source, index }) {
  const category = source.source_type || source.metadata?.source_type || 'api-reference';
  const color = CATEGORY_COLORS[category] || '#00d4ff';
  const label = CATEGORY_LABELS[category] || category.toUpperCase();
  const url = source.source_url || source.metadata?.url || source.url || '#';
  const title = source.title || source.metadata?.title || `Source ${index + 1}`;
  const similarity = source.similarity_score ? Math.round(source.similarity_score * 100) : null;

  return ( <a
    
      href={url}
      target="_blank"
      rel="noopener noreferrer"
      style={{
        display: 'block',
        textDecoration: 'none',
        background: 'rgba(255,255,255,0.03)',
        border: '1px solid rgba(255,255,255,0.08)',
        borderLeft: `3px solid ${color}`,
        borderRadius: '4px',
        padding: '10px 14px',
        marginBottom: '8px',
        transition: 'all 0.2s ease',
        cursor: url === '#' ? 'default' : 'pointer',
      }}
      onMouseEnter={e => {
        e.currentTarget.style.background = 'rgba(255,255,255,0.06)';
        e.currentTarget.style.borderColor = 'rgba(255,255,255,0.15)';
        e.currentTarget.style.borderLeftColor = color;
      }}
      onMouseLeave={e => {
        e.currentTarget.style.background = 'rgba(255,255,255,0.03)';
        e.currentTarget.style.borderColor = 'rgba(255,255,255,0.08)';
        e.currentTarget.style.borderLeftColor = color;
      }}
    >
      <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '2px' }}>
        <span style={{
          fontSize: '9px',
          fontFamily: "'JetBrains Mono', monospace",
          fontWeight: '700',
          color,
          background: `${color}18`,
          border: `1px solid ${color}40`,
          borderRadius: '2px',
          padding: '1px 5px',
          letterSpacing: '0.08em',
        }}>{label}</span>
        {similarity && (
          <span style={{
            fontSize: '9px',
            fontFamily: "'JetBrains Mono', monospace",
            color: 'rgba(255,255,255,0.3)',
            marginLeft: 'auto',
          }}>{similarity}% match</span>
        )}
      </div>
      <div style={{
        fontSize: '12px',
        color: 'rgba(255,255,255,0.6)',
        fontFamily: "'JetBrains Mono', monospace",
        overflow: 'hidden',
        textOverflow: 'ellipsis',
        whiteSpace: 'nowrap',
      }}>{title}</div>
    </a>
    );
}

export default function ResponseDisplay({ response, onNewQuery }) {
  return (
    <div style={{ marginTop: '36px' }}>
      <div style={{
        background: 'rgba(255,255,255,0.02)',
        border: '1px solid rgba(255,255,255,0.08)',
        borderRadius: '8px',
        padding: '24px',
        marginBottom: '16px',
      }}>
        <div style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          marginBottom: '16px',
          paddingBottom: '12px',
          borderBottom: '1px solid rgba(255,255,255,0.06)',
        }}>
          <span style={{
            fontFamily: "'JetBrains Mono', monospace",
            fontSize: '10px',
            color: '#00d4ff',
            letterSpacing: '0.15em',
          }}>ANSWER</span>
          {response.query_time_ms && (
            <span style={{
              fontFamily: "'JetBrains Mono', monospace",
              fontSize: '10px',
              color: 'rgba(255,255,255,0.2)',
            }}>{response.query_time_ms}ms</span>
          )}
        </div>
        <MarkdownAnswer text={response.answer || ''} />
      </div>

      {response.sources && response.sources.length > 0 && (
        <div>
          <div style={{
            fontFamily: "'JetBrains Mono', monospace",
            fontSize: '10px',
            color: 'rgba(255,255,255,0.25)',
            letterSpacing: '0.15em',
            marginBottom: '10px',
          }}>SOURCES ({response.sources.length})</div>
          {response.sources.map((source, i) => (
            <SourceCard key={i} source={source} index={i} />
          ))}
        </div>
      )}

      <button
        onClick={onNewQuery}
        style={{
          marginTop: '20px',
          background: 'transparent',
          border: 'none',
          color: 'rgba(255,255,255,0.3)',
          fontFamily: "'JetBrains Mono', monospace",
          fontSize: '11px',
          cursor: 'pointer',
          letterSpacing: '0.1em',
          padding: '4px 0',
          transition: 'color 0.15s',
        }}
        onMouseEnter={e => e.currentTarget.style.color = 'rgba(0,212,255,0.7)'}
        onMouseLeave={e => e.currentTarget.style.color = 'rgba(255,255,255,0.3)'}
      >
        ← NEW QUERY
      </button>
    </div>
  );
}