const API_ENDPOINT = process.env.REACT_APP_API_ENDPOINT;

export async function queryDocumentation(question) {
  const response = await fetch(API_ENDPOINT, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question: question.trim() }),
  });

  if (!response.ok) {
    throw new Error('API error: ' + response.status);
  }

  return await response.json();
}
