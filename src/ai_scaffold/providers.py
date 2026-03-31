"""Provider registry — supported AI, auth, database, and payment providers."""

from __future__ import annotations

AI_PROVIDERS: dict[str, dict] = {
    "openai": {
        "description": "OpenAI GPT-4o / o1 / o3",
        "env_vars": ["OPENAI_API_KEY"],
        "model_default": "gpt-4o",
        "sdk": "openai",
        "import": "from openai import OpenAI",
        "client_init": 'client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))',
        "chat_call": (
            'response = client.chat.completions.create(\n'
            '    model=settings.AI_MODEL,\n'
            '    messages=messages,\n'
            ')'
        ),
    },
    "anthropic": {
        "description": "Anthropic Claude 3.5 / 3.7",
        "env_vars": ["ANTHROPIC_API_KEY"],
        "model_default": "claude-3-5-sonnet-20241022",
        "sdk": "anthropic",
        "import": "import anthropic",
        "client_init": 'client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))',
        "chat_call": (
            'response = client.messages.create(\n'
            '    model=settings.AI_MODEL,\n'
            '    max_tokens=1024,\n'
            '    messages=messages,\n'
            ')'
        ),
    },
    "gemini": {
        "description": "Google Gemini 1.5 / 2.0",
        "env_vars": ["GOOGLE_API_KEY"],
        "model_default": "gemini-2.0-flash",
        "sdk": "google-generativeai",
        "import": "import google.generativeai as genai",
        "client_init": 'genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))',
        "chat_call": (
            'model = genai.GenerativeModel(settings.AI_MODEL)\n'
            'response = model.generate_content(prompt)'
        ),
    },
}

AUTH_PROVIDERS: dict[str, dict] = {
    "clerk": {
        "description": "Clerk — drop-in auth with pre-built UI",
        "env_vars": ["CLERK_SECRET_KEY", "NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY"],
        "docs": "https://clerk.com/docs",
    },
    "auth0": {
        "description": "Auth0 — enterprise SSO & social login",
        "env_vars": ["AUTH0_DOMAIN", "AUTH0_CLIENT_ID", "AUTH0_CLIENT_SECRET"],
        "docs": "https://auth0.com/docs",
    },
    "supabase-auth": {
        "description": "Supabase Auth — open-source, self-hostable",
        "env_vars": ["SUPABASE_URL", "SUPABASE_ANON_KEY"],
        "docs": "https://supabase.com/docs/guides/auth",
    },
    "nextauth": {
        "description": "NextAuth.js — flexible auth for Next.js",
        "env_vars": ["NEXTAUTH_SECRET", "NEXTAUTH_URL"],
        "docs": "https://next-auth.js.org",
    },
}

DB_PROVIDERS: dict[str, dict] = {
    "supabase": {
        "description": "Supabase — Postgres + realtime + storage",
        "env_vars": ["SUPABASE_URL", "SUPABASE_ANON_KEY", "SUPABASE_SERVICE_ROLE_KEY"],
        "docs": "https://supabase.com/docs",
        "orm": "sqlalchemy",
    },
    "planetscale": {
        "description": "PlanetScale — serverless MySQL (Vitess)",
        "env_vars": ["DATABASE_URL"],
        "docs": "https://planetscale.com/docs",
        "orm": "sqlalchemy",
    },
    "neon": {
        "description": "Neon — serverless Postgres",
        "env_vars": ["DATABASE_URL"],
        "docs": "https://neon.tech/docs",
        "orm": "sqlalchemy",
    },
    "sqlite": {
        "description": "SQLite — local dev / simple deployments",
        "env_vars": [],
        "docs": "https://docs.python.org/3/library/sqlite3.html",
        "orm": "sqlalchemy",
    },
}

PAYMENT_PROVIDERS: dict[str, dict] = {
    "stripe": {
        "description": "Stripe — full-featured payments & subscriptions",
        "env_vars": ["STRIPE_SECRET_KEY", "STRIPE_WEBHOOK_SECRET", "NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY"],
        "docs": "https://stripe.com/docs",
    },
    "lemon-squeezy": {
        "description": "Lemon Squeezy — Stripe alternative for indie devs",
        "env_vars": ["LEMONSQUEEZY_API_KEY", "LEMONSQUEEZY_WEBHOOK_SECRET"],
        "docs": "https://docs.lemonsqueezy.com",
    },
    "none": {
        "description": "No payments — skip payment integration",
        "env_vars": [],
        "docs": "",
    },
}
