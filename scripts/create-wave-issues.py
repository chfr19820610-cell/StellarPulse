import json
import os
import sys
import urllib.request

REPO = os.environ.get('REPO') or os.environ.get('GITHUB_REPOSITORY')
TOKEN = os.environ.get('GITHUB_TOKEN')
DRY_RUN = os.environ.get('DRY_RUN', '0') == '1'

if not REPO:
    print('Missing REPO environment variable.', file=sys.stderr)
    sys.exit(1)
if not TOKEN:
    print('Missing GITHUB_TOKEN environment variable.', file=sys.stderr)
    sys.exit(1)

BASE_URL = f'https://api.github.com/repos/{REPO}/issues'
HEADERS = {
    'Authorization': f'Bearer {TOKEN}',
    'Accept': 'application/vnd.github+json',
    'Content-Type': 'application/json',
}

ISSUES = [
    {
        'title': '[wave] Fix mobile navbar focus trap on iOS',
        'body': """Overview: Mobile users on iOS cannot close the mobile menu using the back gesture; focus is trapped and scrolling is broken.

Type: Bug
Priority: P2
Difficulty: Small (≈2h)

Context: frontend/src/components/layout/MobileMenu.tsx

Acceptance criteria:
- Menu closes and restores page scroll on iOS Safari
- No JS errors in console
- Add a small E2E/manual test""",
        'labels': ['wave', 'bug', 'good-first-issue'],
    },
    {
        'title': '[wave] Add unit tests for useMarket hook',
        'body': """Overview: Add unit tests for useMarket hook to cover loading states and error handling.

Type: Test
Priority: P1
Difficulty: Small (≈3h)

Context: frontend/src/hooks/useMarket.ts

Acceptance criteria:
- Unit tests cover success, loading, and error states
- Tests run in CI""",
        'labels': ['wave', 'test'],
    },
    {
        'title': '[wave] Fix leaderboard sorting edge case',
        'body': """Overview: Leaderboard sorting currently mis-orders players with equal points; add tiebreakers and stable sort.

Acceptance criteria:
- Stable tiebreaker implemented (e.g., volume then win rate)
- Add unit test for tie case""",
        'labels': ['wave', 'bug'],
    },
    {
        'title': '[wave] Improve market card responsiveness on small screens',
        'body': """Overview: Tweak CSS to improve layout on <420px widths.

Acceptance criteria:
- Market cards readable on smallest devices
- No overflow or layout jumps""",
        'labels': ['wave', 'enhancement'],
    },
    {
        'title': '[wave] Update README with deployment quickstart',
        'body': """Overview: Add a concise 'Deploy to Testnet' quickstart with commands and environment variables.

Acceptance criteria:
- Quickstart section added to README
- Commands verified""",
        'labels': ['wave', 'docs'],
    },
    {
        'title': '[wave] Add E2E test for placing a bet flow',
        'body': """Overview: Implement Playwright/Vitest E2E test for the happy path of placing a bet and resolving.

Acceptance criteria:
- Test creates market, places bet, resolves outcome, and claims
- Runs reliably in CI""",
        'labels': ['wave', 'test', 'e2e'],
    },
    {
        'title': '[wave] Fix wallet connect error handling',
        'body': """Overview: Improve error messages and retry logic when wallet connection fails.

Acceptance criteria:
- Clear user-facing error shown
- Retry logic with exponential backoff""",
        'labels': ['wave', 'bug'],
    },
    {
        'title': '[wave] Remove unused imports across frontend',
        'body': """Overview: Run lint and remove unused imports/files to reduce bundle size.

Acceptance criteria:
- Lint passes
- No unused imports left""",
        'labels': ['wave', 'chore'],
    },
    {
        'title': '[wave] Add CONTRIBUTING.md with Wave workflow',
        'body': """Overview: Document how to pick Wave issues, branch naming, PR checklist, and etiquette.

Acceptance criteria:
- CONTRIBUTING.md added with clear steps""",
        'labels': ['wave', 'docs'],
    },
    {
        'title': '[wave] Add rate-limit to Soroban RPC calls in frontend',
        'body': """Overview: Implement simple rate limit/debounce for frequent RPC calls to avoid throttling.

Acceptance criteria:
- Rate limiter implemented and tested locally""",
        'labels': ['wave', 'enhancement', 'perf'],
    },
    {
        'title': '[wave] Fix rounding error in fee calculation',
        'body': """Overview: Address rounding causing small discrepancies in payouts.

Acceptance criteria:
- Accurate payouts in unit tests""",
        'labels': ['wave', 'bug'],
    },
    {
        'title': '[wave] Add admin-only UI for withdrawing fees',
        'body': """Overview: Add a small admin panel to view and withdraw accumulated fees.

Acceptance criteria:
- Withdraw UI only visible to admin wallets
- Calls contract withdraw function""",
        'labels': ['wave', 'feature'],
    },
    {
        'title': '[wave] Chore: add conventional commit linting to CI',
        'body': """Overview: Enforce commit message style with a GitHub Action.

Acceptance criteria:
- CI job fails on non-conventional messages""",
        'labels': ['wave', 'ci', 'chore'],
    },
    {
        'title': '[wave] Fix toast positioning on narrow viewports',
        'body': """Overview: Toast appears off-screen on small devices; adjust container and positioning.

Acceptance criteria:
- Toast visible and non-obstructive on small screens""",
        'labels': ['wave', 'bug', 'ui'],
    },
    {
        'title': '[wave] Improve error logging for contract calls',
        'body': """Overview: Add structured logging for failed contract calls to help debugging.

Acceptance criteria:
- Error logs include contract name, method, args, and error""",
        'labels': ['wave', 'chore'],
    },
    {
        'title': '[wave] Add market image fallback improvements',
        'body': """Overview: Improve SVG placeholder and ensure no console errors when image missing.

Acceptance criteria:
- Placeholder shows correctly
- No console errors""",
        'labels': ['wave', 'enhancement'],
    },
    {
        'title': '[wave] Test: update contract snapshot tests',
        'body': """Overview: Update failing snapshots after recent refactors.

Acceptance criteria:
- Snapshots updated and committed""",
        'labels': ['wave', 'test'],
    },
    {
        'title': '[wave] Accessibility audit: navbar and footer',
        'body': """Overview: Quick accessibility pass focusing on landmark roles, contrast, and keyboard navigation.

Acceptance criteria:
- List of recommended fixes in PR""",
        'labels': ['wave', 'accessibility'],
    },
    {
        'title': '[wave] Chore: update deps for frontend',
        'body': """Overview: Upgrade minor frontend dependencies and fix any breaking changes.

Acceptance criteria:
- Tests pass locally
- No major breaking changes""",
        'labels': ['wave', 'chore'],
    },
    {
        'title': '[wave] Feature: add share to Telegram button',
        'body': """Overview: Add Telegram share option alongside X and WhatsApp.

Acceptance criteria:
- Button opens Telegram share with prefilled text""",
        'labels': ['wave', 'feature'],
    },
    {
        'title': '[wave] Fix claim button state during pending transactions',
        'body': """Overview: Disable claim button while transaction pending to prevent double-claims.

Acceptance criteria:
- Button disabled during pending tx
- UI shows spinner""",
        'labels': ['wave', 'bug'],
    },
    {
        'title': '[wave] Improve README examples for RPC endpoints',
        'body': """Overview: Add example RPC endpoints and env var names for local dev.

Acceptance criteria:
- Examples added to README""",
        'labels': ['wave', 'docs'],
    },
    {
        'title': '[wave] Chore: remove deleted images from commit history (optional)',
        'body': """Overview: Research whether to fully expunge deleted image files from git history to shrink repo; propose plan.

Acceptance criteria:
- Documented plan or steps""",
        'labels': ['wave', 'spike'],
    },
    {
        'title': '[wave] Fix market resolve edge-case for simultaneous resolves',
        'body': """Overview: Prevent double-resolution when two actors trigger resolve near-simultaneously.

Acceptance criteria:
- Contract prevents duplicate resolves and tests cover race case""",
        'labels': ['wave', 'bug'],
    },
    {
        'title': '[wave] Add health-check endpoint for soroban RPC proxy',
        'body': """Overview: Add a lightweight health-check and fallback behavior if RPC is unreachable.

Acceptance criteria:
- Health-check endpoint implemented and used by UI""",
        'labels': ['wave', 'feature'],
    },
    {
        'title': '[wave] Docs: add contract ABI and example calls',
        'body': """Overview: Add short examples showing how to call key contract methods via RPC.

Acceptance criteria:
- Examples for place_bet, resolve_market, and claim""",
        'labels': ['wave', 'docs'],
    },
    {
        'title': '[wave] Fix inconsistent timezone display in leaderboard',
        'body': """Overview: Normalize timestamps to user locale and add consistent formatting.

Acceptance criteria:
- Timestamps show correctly across views""",
        'labels': ['wave', 'bug'],
    },
    {
        'title': '[wave] Add CONTRIBUTOR recognition in README',
        'body': """Overview: Add a short section recognizing contributors and how to get credit for Wave tasks.

Acceptance criteria:
- Section added and examples shown""",
        'labels': ['wave', 'docs'],
    },
    {
        'title': '[wave] Chore: add pre-commit hooks to run lint & tests',
        'body': """Overview: Add basic pre-commit checks to run ESLint and TypeScript typecheck.

Acceptance criteria:
- Hooks added and documented""",
        'labels': ['wave', 'chore'],
    },
]


def request(url, method='GET', data=None, headers=None):
    req = urllib.request.Request(url, data=data, headers=headers or {}, method=method)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.status, resp.read().decode('utf-8')

if DRY_RUN:
    print('DRY_RUN enabled; would create %d issues' % len(ISSUES))
    for issue in ISSUES:
        print('TITLE:', issue['title'])
    sys.exit(0)

existing = set()
page = 1
while True:
    params = f'?state=open&labels=wave&per_page=100&page={page}'
    url = BASE_URL + params
    status, body = request(url, headers=HEADERS)
    if status != 200:
        print('Failed to list existing issues:', status, body, file=sys.stderr)
        sys.exit(1)
    data = json.loads(body)
    if not data:
        break
    for item in data:
        if isinstance(item, dict) and item.get('title'):
            existing.add(item['title'].strip())
    page += 1

for issue in ISSUES:
    title = issue['title'].strip()
    if title in existing:
        print('Skipping existing issue:', title)
        continue
    payload = json.dumps(issue).encode('utf-8')
    status, body = request(BASE_URL, method='POST', data=payload, headers=HEADERS)
    print('Created issue:', title, 'status', status)
