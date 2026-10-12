"""Deterministic intent, entity and retrieval logic for a small soccer assistant."""
import re

RULES = {
    'offside': ('Offside', 'Being in an offside position is not itself an offence. An offence requires involvement in active play when a teammate plays or touches the ball. A player cannot be offside directly from a throw-in, goal kick or corner kick.'),
    'handball': ('Handball', 'Not every touch of the ball by a hand or arm is an offence. Deliberate contact and certain situations where the arm makes the body unnaturally bigger can be offences. The precise context matters.'),
    'foul': ('Fouls', 'Careless direct-free-kick offences normally result in a direct free kick; reckless offences also require a caution; excessive force requires a sending-off. A direct-free-kick offence by a defender inside their own penalty area normally results in a penalty kick.'),
    'throw-in': ('Throw-in', 'A throw-in is awarded when the whole ball crosses the touchline, on the ground or in the air. The opponents of the player who last touched it take the throw-in.'),
    'goal kick': ('Goal kick', 'A goal kick is awarded when the whole ball crosses the goal line without a goal being scored, last touched by an attacking player, and no other restart applies.'),
    'corner': ('Corner kick', 'A corner kick is awarded when the whole ball crosses the goal line without a goal being scored, last touched by a defending player, and no other restart applies.'),
    'free kick': ('Free kicks', 'A direct free kick may score directly against opponents. An indirect free kick must touch another player before a goal can be scored. The referee signals an indirect free kick with a raised arm.'),
    'penalty': ('Penalty kick', 'A penalty kick is awarded for a direct-free-kick offence by a defender inside their own penalty area, subject to the Laws of the Game.'),
}

INTENT_WORDS = {
    'explain_rule': ('rule', 'explain', 'what is', 'meaning', 'offside', 'handball'),
    'check_foul': ('foul', 'tackle', 'push', 'trip', 'yellow', 'red card', 'handball'),
    'restart': ('restart', 'throw-in', 'corner', 'goal kick', 'free kick', 'penalty'),
    'scenario': ('what if', 'scenario', 'suppose', 'imagine', 'inside', 'outside', 'happened'),
}

SENSITIVE = ('medical advice', 'legal advice', 'investment advice', 'diagnose', 'suicide', 'self harm')

def classify_intent(message):
    text = message.lower()
    if any(word in text for word in ('what if', 'scenario', 'suppose', 'imagine')):
        return 'scenario'
    if any(word in text for word in ('restart', 'throw-in', 'corner', 'goal kick', 'free kick', 'penalty')):
        return 'restart'
    if any(word in text for word in ('foul', 'tackle', 'push', 'trip', 'yellow', 'red card')):
        return 'check_foul'
    return 'explain_rule'

def extract_entities(message):
    text = message.lower()
    topic = next((key for key in sorted(RULES, key=len, reverse=True) if key in text), None)
    location = next((value for phrase, value in [('inside the penalty area', 'inside penalty area'), ('inside the box', 'inside penalty area'), ('outside the penalty area', 'outside penalty area'), ('outside the box', 'outside penalty area'), ('touchline', 'touchline'), ('goal line', 'goal line')] if phrase in text), None)
    team = next((value for phrase, value in [('defending team', 'defending'), ('defender', 'defending'), ('attacking team', 'attacking'), ('attacker', 'attacking')] if phrase in text), None)
    return {'topic': topic, 'location': location, 'team': team}

def retrieve(topic):
    return RULES.get(topic)

def out_of_scope(message):
    return any(term in message.lower() for term in SENSITIVE)

def answer_without_model(topic, entities):
    rule = retrieve(topic)
    if not rule:
        return 'I need the rule topic to answer. Try offside, handball, foul, corner, goal kick, throw-in, free kick, or penalty.'
    label, fact = rule
    details = ', '.join(f'{k}: {v}' for k, v in entities.items() if v and k != 'topic')
    return f'{label}: {fact}' + (f'\n\nScenario details remembered: {details}. A referee must decide based on all the facts.' if details else '')
