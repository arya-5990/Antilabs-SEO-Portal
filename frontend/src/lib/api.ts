const API_BASE_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';

export async function analyzeCompetitors(ourUrl: string, competitorUrl: string) {
  const response = await fetch(`${API_BASE_URL}/api/analyze`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      our_url: ourUrl,
      competitor_url: competitorUrl,

    }),
  });

  if (!response.ok) {
    throw new Error('Failed to fetch analysis data');
  }

  return response.json();
}

export async function getHistory() {
  const response = await fetch(`${API_BASE_URL}/api/history`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    throw new Error('Failed to fetch history');
  }

  return response.json();
}

export async function getReportById(id: number) {
  const response = await fetch(`${API_BASE_URL}/api/history/${id}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    throw new Error('Failed to fetch report details');
  }

  return response.json();
}

export async function generateOptimizationCode(analysisData: unknown) {
  const response = await fetch(`${API_BASE_URL}/api/optimize`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      analysis_data: analysisData,
    }),
  });

  if (!response.ok) {
    throw new Error('Failed to generate optimization code');
  }

  return response.json();
}

export async function generateGBPReport(profileUrl: string) {
  const response = await fetch(`${API_BASE_URL}/api/gbp-report`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      profile_url: profileUrl,
    }),
  });

  if (!response.ok) {
    throw new Error('Failed to generate GBP report');
  }

  return response.json();
}

export async function getGBPHistory() {
  const response = await fetch(`${API_BASE_URL}/api/gbp-history`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    throw new Error('Failed to fetch GBP history');
  }

  return response.json();
}

export async function getGBPReportById(id: number) {
  const response = await fetch(`${API_BASE_URL}/api/gbp-history/${id}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    throw new Error('Failed to fetch GBP report details');
  }

  return response.json();
}
