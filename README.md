# Soccer Rules Assistant — CSC-128 Capstone

An educational Streamlit chatbot with four intents (rule explanation, foul assessment, restart explanation, scenario questions), three remembered entities (rule topic, field location, team role), curated reference snippets, Groq language-model responses, and offline fallback.

## Run locally

1. Create a Python virtual environment and activate it.
2. `pip install -r requirements.txt`
3. Copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml`, then put **your own current Groq key** in the copy. Never commit it.
4. Check `git check-ignore -v .streamlit/secrets.toml` and `git status` before any commit.
5. `streamlit run app.py`
6. `python -m unittest discover -s tests -v`

## Deploy

Create a public GitHub repo, push these files **without secrets.toml**, and deploy `app.py` at https://share.streamlit.io. Add `GROQ_API_KEY = "..."` in the deployed app's Secrets settings separately. Test the public URL in a private browser window and wake it before the demonstration.

## Demo script (under five minutes)

1. Show the disclosure and ask: `Explain offside.`
2. Ask: `A defender commits a foul inside the box.` Then ask: `What happens in that situation?` Show remembered slots.
3. Ask: `Who gets a corner kick?` and `What if a player is offside?` to show four intents.
4. Ask about an unsupported topic and show grounded refusal.
5. Temporarily remove the key locally (never show it on camera) and show the offline fallback; then restore it.
6. Explain one improvement: more complete and versioned official IFAB rules.

## Scope and limitations

The reference snippets are simplified teaching notes, **not** a complete or officially licensed copy of IFAB's current Laws. Do not rely on this app for real officiating decisions. It does not store conversations outside the Streamlit session; text may be sent to Groq when the API key is configured. The model is instructed to stay within the supplied excerpt, but this is not a guarantee.
