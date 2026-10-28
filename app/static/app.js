/**
 * app.js — LegalBot frontend client logic
 *
 * Handles:
 *  - Health check badge on load
 *  - Character counter for the textarea
 *  - Example question chips
 *  - POST /ask request with animated progress steps
 *  - Rendering the markdown-like answer (lightweight parser)
 *  - Copy-to-clipboard
 *  - Error display and retry
 */

// ── DOM references ────────────────────────────────────────────
const questionInput   = document.getElementById('question-input');
const charCount       = document.getElementById('char-count');
const askBtn          = document.getElementById('ask-btn');
const askBtnText      = document.getElementById('ask-btn-text');
const askBtnSpinner   = document.getElementById('ask-btn-spinner');

const progressSection = document.getElementById('progress-section');
const step1           = document.getElementById('step-1');
const step2           = document.getElementById('step-2');
const step3           = document.getElementById('step-3');

const answerSection   = document.getElementById('answer-section');
const questionDisplay = document.getElementById('question-display');
const answerContent   = document.getElementById('answer-content');
const sourcesSection  = document.getElementById('sources-section');
const sourcesList     = document.getElementById('sources-list');
const disclaimerText  = document.getElementById('disclaimer-text');
const copyBtn         = document.getElementById('copy-btn');
const newQuestionBtn  = document.getElementById('new-question-btn');

const errorSection    = document.getElementById('error-section');
const errorTitle      = document.getElementById('error-title');
const errorMessage    = document.getElementById('error-message');
const retryBtn        = document.getElementById('retry-btn');

const healthBadge     = document.getElementById('health-badge');

// ── Health check ──────────────────────────────────────────────
async function checkHealth() {
  try {
    const res  = await fetch('/health');
    const data = await res.json();
    if (data.status === 'healthy' && data.groq_configured) {
      healthBadge.textContent = '✅ System Ready';
      healthBadge.className   = 'badge badge--healthy';
    } else {
      healthBadge.textContent = '⚠️ API Key Missing';
      healthBadge.className   = 'badge badge--unhealthy';
    }
  } catch {
    healthBadge.textContent = '❌ Offline';
    healthBadge.className   = 'badge badge--unhealthy';
  }
}

// ── Character counter & button enable/disable ─────────────────
questionInput.addEventListener('input', () => {
  const len = questionInput.value.length;
  charCount.textContent = `${len} / 2000`;
  askBtn.disabled = questionInput.value.trim().length < 10;
});

// ── Example chips ─────────────────────────────────────────────
document.querySelectorAll('.example-chip').forEach(chip => {
  chip.addEventListener('click', () => {
    questionInput.value = chip.dataset.q;
    questionInput.dispatchEvent(new Event('input'));
    questionInput.focus();
  });
});

// ── Progress animation helpers ────────────────────────────────
let progressInterval = null;
let currentStep      = 0;

const steps = [step1, step2, step3];
const stepDelays = [0, 4000, 10000]; // stagger timing in ms

function startProgress() {
  currentStep = 0;
  steps.forEach(s => {
    s.classList.remove('active', 'done');
    const dot = s.querySelector('.step-dot');
    dot.className = 'step-dot';
  });

  progressSection.classList.remove('hidden');

  // Activate step 1 immediately
  activateStep(0);

  // Schedule steps 2 and 3
  stepDelays.slice(1).forEach((delay, i) => {
    setTimeout(() => activateStep(i + 1), delay);
  });
}

function activateStep(index) {
  // Mark previous step done
  if (index > 0) {
    const prev    = steps[index - 1];
    const prevDot = prev.querySelector('.step-dot');
    prev.classList.remove('active');
    prev.classList.add('done');
    prevDot.className = 'step-dot step-dot--done';
  }

  if (index >= steps.length) return;

  const step = steps[index];
  const dot  = step.querySelector('.step-dot');
  step.classList.add('active');
  dot.className = 'step-dot step-dot--active';
}

function finishProgress() {
  steps.forEach(s => {
    s.classList.remove('active');
    s.classList.add('done');
    const dot = s.querySelector('.step-dot');
    dot.className = 'step-dot step-dot--done';
  });
}

function stopProgress() {
  clearInterval(progressInterval);
}

// ── Simple markdown renderer ──────────────────────────────────
// Converts headings, bold, bullet lists, and line breaks to HTML.
function renderMarkdown(text) {
  if (!text) return '';

  const lines   = text.split('\n');
  const html    = [];
  let inList    = false;

  for (let i = 0; i < lines.length; i++) {
    let line = lines[i];

    // Headings
    if (line.startsWith('### ')) {
      if (inList) { html.push('</ul>'); inList = false; }
      html.push(`<h3>${escapeHtml(line.slice(4))}</h3>`);
      continue;
    }
    if (line.startsWith('## ')) {
      if (inList) { html.push('</ul>'); inList = false; }
      html.push(`<h2>${escapeHtml(line.slice(3))}</h2>`);
      continue;
    }
    if (line.startsWith('# ')) {
      if (inList) { html.push('</ul>'); inList = false; }
      html.push(`<h1>${escapeHtml(line.slice(2))}</h1>`);
      continue;
    }

    // Bullet list items
    if (/^[-*•]\s/.test(line)) {
      if (!inList) { html.push('<ul>'); inList = true; }
      html.push(`<li>${inlineFormat(line.replace(/^[-*•]\s/, ''))}</li>`);
      continue;
    }

    // Numbered list
    if (/^\d+\.\s/.test(line)) {
      if (!inList) { html.push('<ul>'); inList = true; }
      html.push(`<li>${inlineFormat(line.replace(/^\d+\.\s/, ''))}</li>`);
      continue;
    }

    // End of a list block
    if (inList && line.trim() === '') {
      html.push('</ul>');
      inList = false;
    }

    // Blank line → paragraph break
    if (line.trim() === '') {
      html.push('<br>');
      continue;
    }

    // Normal paragraph line
    html.push(`<p>${inlineFormat(line)}</p>`);
  }

  if (inList) html.push('</ul>');
  return html.join('\n');
}

// Inline: **bold** and `code`
function inlineFormat(text) {
  return escapeHtml(text)
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/`([^`]+)`/g, '<code>$1</code>');
}

function escapeHtml(str) {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

// ── Ask button click handler ───────────────────────────────────
askBtn.addEventListener('click', submitQuestion);
questionInput.addEventListener('keydown', e => {
  if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) submitQuestion();
});

async function submitQuestion() {
  const question = questionInput.value.trim();
  if (!question || question.length < 10) return;

  // Reset UI
  hideAll();
  setLoading(true);
  startProgress();

  try {
    const response = await fetch('/ask', {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify({ question }),
    });

    const data = await response.json();

    finishProgress();

    if (!response.ok) {
      // HTTP error (422, 503, 500)
      showError(
        response.status === 503 ? 'API Key Not Configured' : 'Request Failed',
        data.detail || 'An unexpected error occurred. Please try again.'
      );
      return;
    }

    // Success — render the answer
    showAnswer(data);

  } catch (err) {
    finishProgress();
    showError('Connection Error', 'Could not reach the LegalBot server. Is it running?');
  } finally {
    setLoading(false);
    // Hide progress after a short delay so the user sees all steps completed
    setTimeout(() => progressSection.classList.add('hidden'), 1200);
  }
}

// ── Render answer ─────────────────────────────────────────────
function showAnswer(data) {
  questionDisplay.textContent = `"${data.question}"`;
  answerContent.innerHTML     = renderMarkdown(data.answer || '');

  // Sources
  if (data.sources && data.sources.length > 0) {
    sourcesList.innerHTML = data.sources
      .map(src => `<li>${escapeHtml(src)}</li>`)
      .join('');
    sourcesSection.classList.remove('hidden');
  } else {
    sourcesSection.classList.add('hidden');
  }

  // Disclaimer
  disclaimerText.textContent = data.disclaimer || '';

  answerSection.classList.remove('hidden');
  answerSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// ── Show error ────────────────────────────────────────────────
function showError(title, message) {
  errorTitle.textContent   = title;
  errorMessage.textContent = message;
  errorSection.classList.remove('hidden');
}

// ── Copy answer ───────────────────────────────────────────────
copyBtn.addEventListener('click', () => {
  const text = answerContent.innerText || '';
  navigator.clipboard.writeText(text).then(() => {
    copyBtn.textContent = '✅ Copied!';
    setTimeout(() => { copyBtn.textContent = '📋 Copy'; }, 2000);
  });
});

// ── New question / retry ──────────────────────────────────────
newQuestionBtn.addEventListener('click', resetUI);
retryBtn.addEventListener('click', () => {
  hideAll();
  // Re-enable input so user can adjust and resubmit
});

function resetUI() {
  hideAll();
  questionInput.value   = '';
  charCount.textContent = '0 / 2000';
  askBtn.disabled       = true;
  questionInput.focus();
}

function hideAll() {
  progressSection.classList.add('hidden');
  answerSection.classList.add('hidden');
  errorSection.classList.add('hidden');
}

function setLoading(loading) {
  askBtn.disabled = loading;
  if (loading) {
    askBtnText.textContent = 'Analyzing…';
    askBtnSpinner.classList.remove('hidden');
  } else {
    askBtnText.textContent = 'Ask LegalBot';
    askBtnSpinner.classList.add('hidden');
    // Re-enable only if enough text
    askBtn.disabled = questionInput.value.trim().length < 10;
  }
}

// ── Init ──────────────────────────────────────────────────────
checkHealth();
