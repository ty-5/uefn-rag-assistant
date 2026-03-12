import React from 'react';

export default function LoadingSpinner() {
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: '12px', padding: '24px 0' }}>
      <div style={{
        width: '20px',
        height: '20px',
        border: '2px solid rgba(0,212,255,0.2)',
        borderTop: '2px solid #00d4ff',
        borderRadius: '50%',
        animation: 'spin 0.8s linear infinite',
      }} />
      <span style={{
        fontFamily: "'JetBrains Mono', monospace",
        fontSize: '12px',
        color: 'rgba(0,212,255,0.7)',
        letterSpacing: '0.1em',
      }}>
        QUERYING DOCUMENTATION...
      </span>
    </div>
  );
}