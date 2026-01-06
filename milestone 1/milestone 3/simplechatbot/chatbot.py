import random
import datetime
import json
import os


class EnhancedChatbot:
    def __init__(self, name="ChatBot"):
        self.name = name
        self.user_name = None
        self.memory_file = "chatbot_memory.json"
        self.memory = self.load_memory()
        self.responses = self.initialize_responses()

    def load_memory(self):
        """Load conversation memory from file"""
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r') as f:
                    return json.load(f)
            except:
                return {"conversations": [], "user_info": {}}
        return {"conversations": [], "user_info": {}}

    def save_memory(self):
        """Save conversation memory to file"""
        with open(self.memory_file, 'w') as f:
            json.dump(self.memory, f, indent=2)

    def initialize_responses(self):
        """Initialize all response patterns"""
        responses = {
            "greetings": {
                "patterns": ["hello", "hi", "hey", "greetings", "good morning", "good afternoon"],
                "responses": [
                    "Hello! How can I help you today?",
                    "Hi there! What's on your mind?",
                    "Hey! Nice to see you!",
                    "Greetings! Ready to chat?"
                ]
            },
            "farewells": {
                "patterns": ["bye", "goodbye", "see you", "exit", "quit"],
                "responses": [
                    "Goodbye! Hope to chat again soon!",
                    "See you later!",
                    "Bye! Take care!",
                    "Farewell! Don't be a stranger!"
                ]
            },
            "name": {
                "patterns": ["your name", "who are you", "what are you"],
                "responses": [
                    f"I'm {self.name}, your friendly chatbot!",
                    f"They call me {self.name}!",
                    f"I go by {self.name}. Nice to meet you!"
                ]
            },
            "time": {
                "patterns": ["time", "what time", "current time"],
                "responses": [
                    f"The current time is {datetime.datetime.now().strftime('%I:%M %p')}",
                    f"It's {datetime.datetime.now().strftime('%H:%M')} right now"
                ]
            },
            "date": {
                "patterns": ["date", "today's date", "what date"],
                "responses": [
                    f"Today is {datetime.datetime.now().strftime('%A, %B %d, %Y')}",
                    f"The date is {datetime.datetime.now().strftime('%Y-%m-%d')}"
                ]
            },
            "joke": {
                "patterns": ["joke", "funny", "make me laugh"],
                "responses": [
                    "Why don't scientists trust atoms? Because they make up everything!",
                    "Why did the math book look so sad? Because it had too many problems!",
                    "What do you call a bear with no teeth? A gummy bear!"
                ]
            },
            "weather": {
                "patterns": ["weather", "rain", "sunny", "temperature"],
                "responses": [
                    "I wish I could check the weather for you, but I'm just a simple chatbot!",
                    "You might want to check a weather app for accurate forecasts!",
                    "I'm not connected to weather services, sorry!"
                ]
            },
            "help": {
                "patterns": ["help", "what can you do", "capabilities"],
                "responses": [
                    "I can chat with you, tell jokes, give the time and date, and remember our conversations!",
                    "Try asking me about time, date, or tell me a joke! You can also ask for help anytime.",
                    "I'm here to chat! You can ask me anything, and I'll do my best to respond."
                ]
            }
        }
        return responses

    def get_response(self, user_input):
        """Get appropriate response based on user input"""
        user_input_lower = user_input.lower()

        # Check for user name
        if "my name is" in user_input_lower:
            name = user_input.split("my name is")[-1].strip()
            if name:
                self.user_name = name
                self.memory["user_info"]["name"] = name
                return f"Nice to meet you, {name}! I'll remember that."

        # Check for greeting with name
        if self.user_name and any(greet in user_input_lower for greet in ["hello", "hi", "hey"]):
            return f"Hello {self.user_name}! How are you today?"

        # Check patterns
        for category, data in self.responses.items():
            for pattern in data["patterns"]:
                if pattern in user_input_lower:
                    return random.choice(data["responses"])

        # Default responses
        default_responses = [
            "That's interesting! Tell me more.",
            "I see. What else would you like to talk about?",
            "Could you elaborate on that?",
            "Hmm, I'm not sure I understand. Could you rephrase?",
            "Thanks for sharing!",
            f"Interesting point! What do you think about it, {self.user_name if self.user_name else ''}?"
        ]

        return random.choice(default_responses)

    def chat(self):
        """Main chat loop"""
        print("=" * 60)
        print(f"🤖 {self.name} v2.0 - Enhanced Chatbot")
        print("I can remember your name and our conversations!")
        print("Type 'quit', 'exit', or 'bye' to end the conversation")
        print("=" * 60)

        conversation_count = len(self.memory["conversations"]) + 1

        while True:
            # Get user input
            user_input = input("\nYou: ").strip()

            # Check for exit
            if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye']:
                response = random.choice(self.responses["farewells"]["responses"])
                print(f"🤖 {self.name}: {response}")

                # Save conversation
                self.memory["conversations"].append({
                    "id": conversation_count,
                    "date": datetime.datetime.now().isoformat(),
                    "user_input": user_input,
                    "bot_response": response
                })
                self.save_memory()
                break

            # Get and print response
            response = self.get_response(user_input)
            print(f"🤖 {self.name}: {response}")

            # Save to memory
            self.memory["conversations"].append({
                "id": conversation_count,
                "date": datetime.datetime.now().isoformat(),
                "user_input": user_input,
                "bot_response": response
            })
            conversation_count += 1

            # Auto-save every 5 messages
            if conversation_count % 5 == 0:
                self.save_memory()


def main():
    chatbot = EnhancedChatbot()
    chatbot.chat()


if __name__ == "__main__":
    main()

