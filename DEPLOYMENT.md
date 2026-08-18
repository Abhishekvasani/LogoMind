# Deploying LogoMind — free tier (Vercel + Neon)

No sign-up/sign-in by design (founder decision): the deployed app is a single shared workspace. Everything below fits the **free** tiers.

**Shape (as deployed):** ONE multi-service Vercel project — `logo-mind` — imported from the GitHub repo:
- **frontend** ← `frontend/` (Next.js) — serves the UI at the project domain
- **backend** ← `backend/` (FastAPI service, entrypoint `app/main.py`) — answers at `/api/*` (and `/api/backend/*`); the router is dual-mounted so both prefixes work

**Database:** Neon free Postgres, created and connected through Vercel Storage (marketplace) — `DATABASE_URL` (pooled) is injected into the project. Sketch images are stored **in the database**; the LIC knowledge volumes are vendored at `backend/05_RS_LICs` (sync with `python scripts/sync_backend_lics.py` after editing LICs).

**Long AI calls:** `maxDuration` defaults under Fluid Compute are sufficient; `/health` self-diagnoses (`db.scheme/ok`, `knowledge.available`).

**Deploy hook:** pushes occasionally miss the Git webhook; the `zap-deploy` hook (project Settings → Git) triggers a production deploy of `main` on demand.

**Live:** https://logo-mind-two.vercel.app — `/api/health` returns healthy + 24/24 knowledge extracts.

---

## 1. Create the database (Neon, ~2 minutes)

1. Sign up at [neon.tech](https://neon.tech) → **Create project** (any name, e.g. `logomind`).
2. Copy the **pooled** connection string — it looks like:
   `postgresql://user:pass@ep-xxx-pooler.region.aws.neon.tech/neondb?sslmode=require`

## 2. Deploy the API project

```bash
npm i -g vercel          # once
cd backend
vercel link              # create NEW project, name it e.g. logomind-api
```

Set environment variables (Vercel dashboard → project → Settings → Environment Variables, or `vercel env add`):

| Variable | Value |
|---|---|
| `DATABASE_URL` | the Neon pooled connection string |
| `LOGOMIND_AI_PROVIDER` | `nim` |
| `NVIDIA_API_KEY` | your NVIDIA key (same as `backend/.env`) |
| `LOGOMIND_MODEL` | e.g. `nvidia/nemotron-3-ultra-550b-a55b` (or a faster/smaller model) |
| `CORS_ORIGINS` | leave unset until the web URL exists; then set it (step 4) |

```bash
vercel --prod
```

Note the URL, e.g. `https://logomind-api.vercel.app`. Check: `curl https://logomind-api.vercel.app/health` → `{"status": "healthy", "knowledge": ...}` with 24 extracts.

## 3. Create the schema (once, from your machine)

```bash
cd backend
DATABASE_URL="<neon pooled url>" alembic upgrade head
```

(Or run `vercel env pull .env.production` first and use that `DATABASE_URL`.)

## 4. Deploy the Web project

```bash
cd ../frontend
vercel link              # create NEW project, e.g. logomind-web
vercel env add NEXT_PUBLIC_API_BASE production   # value: https://logomind-api.vercel.app
vercel --prod
```

Note the web URL (e.g. `https://logomind-web.vercel.app`), then finish CORS on the API:

```bash
cd ../backend
vercel env add CORS_ORIGINS production   # value: https://logomind-web.vercel.app
vercel --prod                             # redeploy to pick it up
```

## 5. Sanity walk

Open the web URL → create a project → run the pipeline. If a slow stage times out, the UI shows progress + Retry — retrying continues fine.

---

## Notes & limits (free tier reality)

- **Request body ≤ 4 MB** (Vercel): sketch uploads are capped at 3.5 MB server-side (`LOGOMIND_MAX_IMAGE_BYTES` to change).
- **No auth (by decision):** anyone with the URL can use the workspace — share deliberately.
- **Cold starts:** the first request after idle loads the app + 24 knowledge volumes (~1–2 s).
- **Model speed:** the big nemotron model is slow; a smaller model (`LOGOMIND_MODEL`) makes serverless life easier.
- **`alembic stamp head`** on the Neon DB if `init_db`'s auto-create ran before migrations did — harmless either way.
- Local dev is unchanged (SQLite + `.env`).

## Updating

```bash
cd backend  && vercel --prod   # after API changes
cd frontend && vercel --prod   # after UI changes
```
