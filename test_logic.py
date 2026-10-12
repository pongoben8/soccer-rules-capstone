import unittest
from logic import classify_intent, extract_entities, retrieve, out_of_scope, answer_without_model

class LogicTests(unittest.TestCase):
    def test_four_intents(self):
        self.assertEqual(classify_intent('explain offside'), 'explain_rule')
        self.assertEqual(classify_intent('is that a foul tackle'), 'check_foul')
        self.assertEqual(classify_intent('who gets the corner restart'), 'restart')
        self.assertEqual(classify_intent('what if the player is offside'), 'scenario')

    def test_two_entities(self):
        slots = extract_entities('defender commits a foul inside the box')
        self.assertEqual(slots['topic'], 'foul')
        self.assertEqual(slots['location'], 'inside penalty area')
        self.assertEqual(slots['team'], 'defending')

    def test_empty_retrieval(self):
        self.assertIsNone(retrieve('unknown'))
        self.assertIn('need the rule topic', answer_without_model(None, {}))

    def test_refusal(self):
        self.assertTrue(out_of_scope('give me medical advice'))

if __name__ == '__main__':
    unittest.main()
