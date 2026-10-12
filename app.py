"""Streamlit interface for the Soccer Rules Assistant capstone."""
import streamlit as st
from logic import classify_intent, extract_entities, out_of_scope, retrieve, answer_without_model
from safe_call import ask_model

st.set_page_config(page_title='Soccer Rules Assistant', page_icon='⚽')
st.title('⚽ Soccer Rules Assistant')
st.info('I am an AI-powered software chatbot, not a human referee. Answers are educational and may be incomplete. Do not enter personal or sensitive information; questions are sent to a third-party language model when enabled.')
st.caption('Ask about offside, fouls, handball, or restarts. For a disputed match decision, consult a qualified referee and the current official IFAB Laws of the Game.')

if 'history' not in st.session_state:
    st.session_state.history = []
if 'slots' not in st.session_state:
    st.session_state.slots = {'topic': None, 'location': None, 'team': None}

with st.sidebar:
    st.subheader('Current scenario')
    for key, value in st.session_state.slots.items():
        st.write(f'**{key.title()}:** {value or "not provided"}')
    if st.button('Clear conversation'):
        st.session_state.history = []
        st.session_state.slots = {'topic': None, 'location': None, 'team': None}
        st.rerun()

for item in st.session_state.history:
    with st.chat_message(item['role']):
        st.write(item['content'])

if prompt := st.chat_input('Example: A defender trips an attacker inside the box. What happens?'):
    st.session_state.history.append({'role': 'user', 'content': prompt})
    with st.chat_message('user'):
        st.write(prompt)

    if out_of_scope(prompt):
        answer = 'I only explain soccer rules. For medical, legal, financial, or mental health concerns, please contact a qualified professional.'
    else:
        intent = classify_intent(prompt)
        new_slots = extract_entities(prompt)
        for key, value in new_slots.items():
            if value is not None:
                st.session_state.slots[key] = value
        slots = st.session_state.slots
        topic = slots['topic']
        rule = retrieve(topic)
        if rule is None:
            answer = 'I cannot find a matching rule in my small reference set. Please name a rule such as offside, handball, foul, throw-in, goal kick, corner, free kick, or penalty. I will not guess.'
        else:
            fallback = answer_without_model(topic, slots)
            try:
                key = st.secrets.get('GROQ_API_KEY', '')
            except Exception:
                key = ''
            if key:
                system = ('You are an educational soccer rules assistant. Disclose no private data. '
                          'Answer ONLY from the supplied rule excerpt. Never invent rules or numbers. '
                          'If the excerpt cannot settle a scenario, say a qualified referee should decide. '
                          'Be concise and accessible. Do not provide medical, legal, financial or mental health advice.')
                context = f'Intent: {intent}\nKnown scenario entities: {slots}\nReference: {rule[0]} — {rule[1]}\nQuestion: {prompt}'
                model_answer, error = ask_model(key, [{'role': 'system', 'content': system}, {'role': 'user', 'content': context}])
                answer = model_answer if model_answer else f'{error}\n\nReference answer (offline): {fallback}'
            else:
                answer = ('The AI service is not configured. Here is the reference answer instead:\n\n' + fallback)
    with st.chat_message('assistant'):
        st.write(answer)
    st.session_state.history.append({'role': 'assistant', 'content': answer})
