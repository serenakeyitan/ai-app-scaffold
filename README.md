# ai-app-scaffold

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![CI](https://github.com/serenakeyitan/ai-app-scaffold/actions/workflows/ci.yml/badge.svg)](https://github.com/serenakeyitan/ai-app-scaffold/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/ai-app-scaffold)](https://pypi.org/project/ai-app-scaffold/)

> **Zero-to-prod AI app in one command.** Stop assembling IKEA furniture. Start shipping.

Inspired by [Karpathy's observation](https://twitter.com/karpathy) that the hardest part of shipping an AI app isn't the AI code — it's wiring up all the services: auth, payments, database, domain, secrets, monitoring. `ai-scaffold` pre-wires all of it.

```bash
pip install ai-app-scaffold
ai-scaffold new my-app --ai openai --auth clerk --db supabase --payments stripe
```

That's it. You get a production-ready FastAPI monorepo with everything connected.

---

## The Problem

When you build an AI-powered app, the AI code is maybe 5% of the work. The rest is:

- **Auth** — Clerk, Auth0, or Supabase Auth, with JWTs, sessions, social login
- **Payments** — Stripe subscriptions, webhooks, billing portal
- **Database** — Supabase, PlanetScale, Neon, with migrations and connection pooling
- **Secrets** — `.env` management, rotation, production vs. dev separation
- **Monitoring** — Sentry error tracking, metrics endpoint
- **Docker** — Dockerfile, docker-compose, health checks
- **CI/CD** — GitHub Actions for lint, test, and deploy

`ai-scaffold` generates a project with all of this pre-wired and ready to deploy.

---

## Quick Start

```bash
# Install
pip install ai-app-scaffold

# Interactive mode — guided prompts
ai-scaffold new my-ai-app

# One-liner — fully specified
ai-scaffold new my-ai-app \
  --ai anthropic \
  --auth clerk \
  --db supabase \
  --payments stripe

# Check your environment
ai-scaffold doctor

# See all supported providers
ai-scaffold list-providers
```

---

## Supported Providers

### AI Providers

| Provider | Models | Env Var |
|----------|--------|---------|
| `openai` | GPT-4o, o1, o3 | `OPENAI_API_KEY` |
| `anthropic` | Claude 3.5, 3.7 | `ANTHROPIC_API_KEY` |
| `gemini` | Gemini 1.5, 2.0 | `GOOGLE_API_KEY` |

### Auth Providers

| Provider | Description |
|----------|-------------|
| `clerk` | Drop-in auth with pre-built UI |
| `auth0` | Enterprise SSO & social login |
| `supabase-auth` | Open-source, self-hostable |
| `nextauth` | Flexible auth for Next.js |

### Database Providers

| Provider | Description |
|----------|-------------|
| `supabase` | Postgres + realtime + storage |
| `planetscale` | Serverless MySQL (Vitess) |
| `neon` | Serverless Postgres |
| `sqlite` | Local dev / simple deployments |

### Payment Providers

| Provider | Description |
|----------|-------------|
| `stripe` | Full-featured payments & subscriptions |
| `lemon-squeezy` | Stripe alternative for indie devs |
| `none` | Skip payment integration |

---

## Generated Project Structure

```
my-ai-app/
├── app/
│   ├── main.py           # FastAPI application factory
│   ├── settings.py       # Pydantic settings (typed env vars)
│   ├── monitoring.py     # Sentry + /metrics endpoint
│   ├── routes/
│   │   ├── chat.py       # AI chat endpoint (provider pre-wired)
│   │   ├── auth.py       # Auth middleware
│   │   └── webhooks.py   # Payment webhook handler
│   ├── db/
│   │   └── models.py     # SQLAlchemy models (User, Conversation, Message)
│   └── services/
│       ├── ai.py         # AI provider client
│       └── payments.py   # Payment provider client
├── .env.example          # All env vars listed, ready to fill
├── .gitignore
├── Dockerfile
├── docker-compose.yml    # App + Postgres
├── pyproject.toml
└── .github/
    └── workflows/
        └── ci.yml        # Lint + test on push
```

---

## CLI Reference

```
Commands:
  new              Scaffold a new production-ready AI application
  list-providers   List all supported providers by category
  add              Add a feature to an existing scaffolded project
  doctor           Check your environment for required dependencies
```

### `ai-scaffold new`

```
Arguments:
  PROJECT_NAME  Name of the project (used as directory name)

Options:
  --ai          [openai|anthropic|gemini]
  --auth        [clerk|auth0|supabase-auth|nextauth]
  --db          [supabase|planetscale|neon|sqlite]
  --payments    [stripe|lemon-squeezy|none]
  --monitoring / --no-monitoring   (default: on)
  --docker / --no-docker           (default: on)
  --ci / --no-ci                   (default: on)
  -o, --output-dir PATH
  -y, --yes     Skip interactive prompts
```

### `ai-scaffold add`

```bash
ai-scaffold add monitoring     # Add Sentry + metrics
ai-scaffold add docker         # Add Dockerfile + compose
ai-scaffold add ci             # Add GitHub Actions
ai-scaffold add rate-limiting  # Add Redis-backed rate limiting
ai-scaffold add analytics      # Add PostHog analytics
```

---

## Running Tests

```bash
pip install -e ".[dev]"
pytest tests/ -v
```

---

## Contributing

Contributions welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) first.

Ideas for contributions:
- New AI providers (Mistral, Cohere, Together AI)
- New auth providers (Lucia, Better Auth)
- New database providers (Turso, CockroachDB)
- Frontend scaffold (Next.js, SvelteKit)
- Deployment configs (Fly.io, Railway, Render)

---

## License

MIT — see [LICENSE](LICENSE).

---

*Built because Karpathy was right: the DevOps assembly is the hard part.*
