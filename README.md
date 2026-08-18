# AgentCore Chat (React + FastAPI)

React replacement for the Streamlit app, talking to your AWS Bedrock
AgentCore runtime.

## Why there's a backend at all

`boto3` and AWS credentials can't run in a browser. React can only ever
call an HTTP API, so there's a thin FastAPI service in `backend/` whose
only job is: receive `{ session_id, message }` from the browser, call
`client.invoke_agent_runtime(...)` exactly like your snippet, and return
the parsed JSON. Keep your AWS credentials on this server only — never in
the React app or its `.env` (anything prefixed `VITE_` is bundled into
the browser code and is public).

## Layout

```
backend/    FastAPI service wrapping invoke_agent_runtime
frontend/   Vite + React chat UI (sidebar of sessions + chat window)
```

## Backend setup

```bash
cd backend
python -m venv venv && source venv/bin/activate   # optional but recommended
pip install -e .          # uses pyproject.toml
# or: pip install -r requirements.txt
cp .env.example .env
```

Open `.env` and fill in:
- `AGENT_RUNTIME_ARN` — already pre-filled from your snippet, change if needed
- `ENDPOINT_QUALIFIER` — leave blank to use DEFAULT
- `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` — only needed if you're not
  already using `aws configure` or an IAM role

Run it:

```bash
uvicorn app:app --reload --port 8000
```

Check `http://localhost:8000/api/health` returns `{"status":"ok"}`.

## Frontend setup

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

Opens at `http://localhost:5173`. It calls the backend at the URL in
`VITE_API_BASE_URL`.

## What's different from the Streamlit version

- **No `chatbot.stream` / `chatbot.get_state`.** AgentCore's
  `invoke_agent_runtime` returns one response per call, not a token
  stream, and there's no equivalent of a LangGraph checkpointer to pull
  prior turns from. So the React app keeps each session's message
  history in the browser (`localStorage`) instead of re-loading it from
  the backend on click — same visual effect (sidebar of past chats,
  click to resume), different mechanism.
- **`session_id` = `thread_id`.** It's generated client-side (33+ chars,
  as AgentCore requires) and sent as `runtimeSessionId` on every call for
  that session, so the agent's own runtime state stays tied to it.
- **Response parsing.** `_extract_text` in `backend/app.py` guesses at
  common keys (`response`, `completion`, `output`, `result`, `text`,
  `message`) in the JSON your agent returns. Once you know the exact
  shape, trim that function down to just that key.

## Production notes

- Restrict `ALLOWED_ORIGINS` in the backend `.env` to your real frontend
  domain before deploying.
- Don't put AWS credentials in the frontend build. If you deploy the
  backend somewhere with an IAM role attached (ECS, Lambda, EC2), you can
  leave the AWS key/secret fields blank entirely.
