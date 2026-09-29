## Hi there 👋 I'm Thun

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="dark_mode.svg" />
  <source media="(prefers-color-scheme: light)" srcset="light_mode.svg" />
  <img alt="DuchPanhathun's GitHub profile" src="dark_mode.svg" />
</picture>

**Full-stack engineer with AI/ML depth — Python + TypeScript — who has built fintech, media, and social-impact platforms for the Cambodian market.** 🇰🇭

Most of my work lives in private organization repositories, so this page is the map: what I've built, and what I owned in each.

### 🔭 Recent work

- 🏢 **Platform engineering at [Ailsa](https://github.com/Ailsa-io)** (late 2025 – 2026) — a grant-discovery and grant-application SaaS with deep AI integration. I worked across the customer app, admin dashboard, API gateway, shared library, and scraper services, usually shipping one feature end to end across all of them.
- 🎬 **Video streaming, 🧾 point-of-sale, and 🏦 co-op lending platforms** — project-based commercial builds in 2026, where I owned specific modules (details below).
- 🌱 **Social-impact work** — AI crop-disease advisory for Cambodian farmers, and NGO websites and management systems.

### ✨ Highlights

- 📄 **Published BSc thesis:** machine-learning fraud detection on **6.36M** online-payment transactions — domain-specific behavioural and temporal features, cost-sensitive learning, **99.96% ROC-AUC** with CatBoost. Solo work, Royal University of Phnom Penh, published on Zenodo with a DOI.
- 🌾 **Computer vision for farmers:** sole author of the crop-disease training pipelines (ConvNeXt-Large, EfficientNet-B5, Swin-B) across PyTorch and TensorFlow/Keras for **Carep / SaveCrop**, an AI agricultural advisory served through a Telegram bot.
- 🚀 **Bootstrapped a SaaS app from an empty repo:** Ailsa's Next.js 16 / React 19 customer application — Server Actions data layer, Auth0 authentication, AWS Amplify deployment — and was its most active contributor.
- 🔐 **Auth done properly:** database-backed JWT session revocation with concurrent-device limits, so logout takes effect immediately; section- and department-level access control derived from existing membership data, without a schema migration.
- 📺 **Live TV end to end:** entitlement-gated HLS playback authorized by short-lived tokens, built across a FastAPI backend and a Next.js client, with the API kept out of the video-segment traffic path.

### 🧠 What I'm good at

| Strength | What that looks like |
|---|---|
| 💳 **Cambodian payments** | KHQR / Bakong, ABA PayWay, and Baray across three platforms, plus Stripe. Includes the operational details: settlement without webhooks (polling plus a background sweeper), QR expiry rules, and dual-currency USD/KHR cash reconciliation. |
| 🤖 **Telegram as an app platform** | Full conversational clients, not just notifications: grammY bots with multi-step conversation flows, Telegram Mini Apps, OTP over chat, webhook and polling deployment, account linking. |
| 🧩 **AI with guardrails** | AI output is never silently committed: preview-then-insert editors, provenance so automated re-scoring never overwrites a human edit, and structured output validated against a closed catalogue with a deterministic fallback. |
| 🔐 **Authentication & authorization** | Role hierarchies plus document-level ACLs, session revocation, three-state Auth0 session handling, and machine-to-machine trust boundaries for AI agents. |
| 🇰🇭 **Bilingual Khmer/English products** | Six projects, from schema-level translation fields to type-enforced dictionaries where TypeScript guarantees every string is translated. Also Cambodia's province → district → commune → village hierarchy. |
| 🌱 **NGO & social-impact domains** | Child protection, grant funding, cooperative finance, and agricultural extension, including work for Save the Children Cambodia. |

### 🛠️ Selected work

| Project | What it is | Stack | What I did |
|---|---|---|---|
| **Ailsa** · 6 services | Grant-discovery & application SaaS | Next.js 16, React 19, Node/Express, FastAPI, MongoDB, Auth0, AWS (ECS, SQS, S3), Terraform, OpenAI + Anthropic | Founded the customer app; built the standard scraper tier (5 funder scrapers, normalizers, tests, SQS worker) and its LLM classification layer; owned features across gateway, admin, and shared library: RBAC, folder ACLs, grant-scraping retry pipeline, AI-agent auth, streaming AI editor UX |
| **Carep / SaveCrop** | AI crop-disease advisory for Cambodian farmers (Save the Children / STEER) | PyTorch, TensorFlow/Keras, Telegram bot, Next.js, Supabase | Sole author of both CV training repos; primary author of the weather scraper; founded the admin dashboard |
| **Reeltime Media** | Video streaming platform for Cambodia: VOD, live TV, KHQR payments | FastAPI, SQLAlchemy async, PostgreSQL, Next.js 16, hls.js, ffmpeg, Cloudflare R2 | Auth and session system; live TV across API and client |
| **Super-POS** | Coffee-shop POS and customer-loyalty platform | NestJS, Sequelize, Angular 18, Next.js 16, grammY, Socket.IO, OpenAI | Customer loyalty, wallet, and ERP backend modules; Telegram Mini App; AI badge assignment; idempotency keys for payment endpoints |
| **Loan Management System** | Savings-and-credit cooperative platform with a Telegram bot client | Next.js 16, Supabase (Postgres + RLS), Cloudflare R2, Telegram Bot API | Contributor to the app and its database migrations |
| **CCYMCR** | Bilingual NGO website with a hand-built CMS | Next.js 16, Supabase, Leaflet, Tailwind v4 | 100% solo: ~30 content types, each with its own table, API route, and live-editable component |
| **HR Platform** | NGO staffing tool (Save the Children Cambodia) | Django REST, MongoDB, PuLP, llama.cpp, FAISS, React | Near-sole author: linear-programming staff-to-task optimizer and a local-LLM RAG chatbot over uploaded HR documents |
| **Partnership MIS** | NGO partnership records system | Laravel 11, Next.js 14, PostgreSQL, Docker | Primary author of frontend and backend |
| **Positive Parenting** | Khmer-language parenting education site | React, Firebase | Built the admin CMS, media upload, tagging, and campaign/quiz scheduler |
| **Fraud Detection** (BSc thesis) | Online-payment fraud classification | Python, CatBoost, XGBoost, LightGBM, scikit-learn | Solo, published |

### 🧰 Tech stack

<p>
  <img src="https://skillicons.dev/icons?i=ts,js,py,php,nextjs,react,angular,tailwind,nodejs,nestjs,express,fastapi,django,laravel&perline=14" alt="Languages and frameworks" />
</p>
<p>
  <img src="https://skillicons.dev/icons?i=postgres,mongodb,mysql,redis,supabase,firebase,aws,gcp,cloudflare,vercel,docker,terraform,githubactions,pytorch,tensorflow,sklearn&perline=16" alt="Data, cloud and ML" />
</p>

- **Languages:** TypeScript, JavaScript, Python, PHP, SQL
- **Frontend:** Next.js (App Router), React 18/19, Angular 18, Tailwind, shadcn/Radix, Tiptap, hls.js
- **Backend:** FastAPI, NestJS, Express, Django REST, Laravel, Next.js Server Actions
- **Data:** PostgreSQL / Supabase, MongoDB, MySQL, Firestore, Redis · SQLAlchemy, Sequelize, Mongoose, Eloquent · Alembic
- **AI / ML:** PyTorch, TensorFlow/Keras, CatBoost/XGBoost/LightGBM, RAG (llama.cpp, sentence-transformers, FAISS), OpenAI & Anthropic APIs
- **Cloud / DevOps:** AWS (ECS/Fargate, S3, SQS, SES, CloudFront, Amplify), GCP, Cloudflare R2, Vercel, Docker, Terraform, GitHub Actions, ffmpeg
- **Payments & messaging:** KHQR/Bakong, ABA PayWay, Baray, Stripe · Telegram Bot API (grammY, Mini Apps), Slack, Twilio, Resend, SES

### 🗺️ Journey

- **2024** — Royal University of Phnom Penh team projects for NGOs: Positive Parenting, Partnership MIS
- **Early 2025** — HR Platform for Save the Children Cambodia: LP optimizer and local-LLM RAG
- **Mid 2025** — BSc thesis on fraud detection, published
- **Late 2025** — Carep / SaveCrop AI agri-advisory; joined **Ailsa**
- **2026** — Ailsa platform engineering alongside project-based streaming, POS, and co-op lending builds, and a solo NGO site (CCYMCR). All of these are now completed.
