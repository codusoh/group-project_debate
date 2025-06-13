import requests
import json
import os
import random
import datetime

class DebateSession:
    def __init__(self, topic, category="미지정", user_level="고등학생", difficulty="중"):
        self.topic = topic
        self.category = category
        self.user_level = user_level
        self.difficulty = difficulty
        self.user_stance = random.choice(["찬성", "반대"])
        self.bot_stance = "반대" if self.user_stance == "찬성" else "찬성"
        self.chat_log = []
        self.feedback = None
        self.improvements = []
        self.summary_notes = []
        self.time = datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")

    def add_entry(self, role, content):
        self.chat_log.append({"role": role, "content": content})

    def get_bot_response(self, api_key, system_prompt, model="deepseek/deepseek-r1:free"):
        messages = [{"role": "system", "content": system_prompt}] + self.chat_log
        headers = {
            "Authorization": f"Bearer {api_key}",
            "HTTP-Referer": "debate_program",
            "Content-Type": "application/json"
        }
        data = {
            "model": model,
            "messages": messages
        }
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        reply = response.json()["choices"][0]["message"]["content"]
        self.add_entry("assistant", reply)
        return reply

    def show_roles(self):
        print("\n[입장 안내]")
        print(f"사용자 입장: {self.user_stance}")
        print(f"상대 입장: {self.bot_stance}\n")

    def add_note_summary(self, note):
        self.summary_notes.append(note)

    def show_instructions(self):
        print("""
[토론 진행 순서 안내]
1. 사용자 입론
2. 상대 입론
3. 상대 반론
4. 사용자 반론
5. 상대 재반박
6. 사용자 정리
7. 상대 정리
8. 토론 피드백 저장
        """)
        

    def run_debate(self, api_key):
        print(f"\n 🗣️ 토론 주제: {self.topic}")
        self.show_roles()
        self.show_instructions()

        # 찬성측 / 반대측 판별
        if self.user_stance == "찬성":
            pro_side = "user"
            con_side = "bot"
        else:
            pro_side = "bot"
            con_side = "user"

        print("\n=== 입론 단계 ===")

        # 찬성측 입론
        if pro_side == "user":
            user_input = input(f"\n (찬성 측) 사용자의 입론: ")
            self.add_entry("user", user_input)
            self.add_note_summary("찬성 측(사용자) 입론 완료")
        else:
            print("\n (찬성 측) 상대의 입론 작성 중...")
            bot_argument = self.get_bot_response(api_key, f"""
        너는 '{self.topic}'에 대해 '찬성' 입장인 AI야.
        토론주제에 맞게 너의 입장에서 논리적으로 입론을 구성해서 짧고 간결하게 말해
        입론은 3~4문장으로만 구성하고, 한국어로만 대답해. 외국어를 사용하지마
        """)
            print(f"\n (찬성 측) 상대의 입론:\n{bot_argument}")
            self.add_entry("assistant", bot_argument)
            self.add_note_summary("찬성 측(상대) 입론 완료")

        # 반대측 입론
        if con_side == "user":
            user_input = input(f"\n (반대 측) 사용자의 입론: ")
            self.add_entry("user", user_input)
            self.add_note_summary("반대 측(사용자) 입론 완료")
        else:
            print("\n (반대 측) 상대의 입론 작성 중...")
            bot_argument = self.get_bot_response(api_key, f"""
        너는 '{self.topic}'에 대해 '반대' 입장인 AI야.
        토론주제에 맞게 너의 입장에서 논리적으로 입론을 구성해서 짧고 간결하게 말해
        입론은 3~4문장으로만 구성하고, 한국어로만 대답해. 외국어를 사용하지마
        """)
            print(f"\n (반대 측) 상대의 입론:\n{bot_argument}")
            self.add_entry("assistant", bot_argument)
            self.add_note_summary("반대 측(상대) 입론 완료")

        print("\n=== 반박 단계 ===")

        # 반대측 반박
        if con_side == "user":
            user_rebuttal = input(f"\n (반대 측) 반박을 입력하세요: ")
            self.add_entry("user", user_rebuttal)
            self.add_note_summary("반대 측(사용자) 반박 완료")
        else:
            print("\n (반대 측) 상대의 반박 작성 중...")
            bot_rebuttal = self.get_bot_response(api_key, f"""
        너는 '{self.topic}'에 대해 '반대' 입장인 AI야.
        찬성 측 입론을 논리적으로 짧게 반박해.
        반박은 3~4문장으로, 간결하고 논리적으로 해줘. 한국어로만 대답해. 외국어 사용하지 마.
        """)
            print(f"\n (반대 측) 상대의 반박:\n{bot_rebuttal}")
            self.add_entry("assistant", bot_rebuttal)
            self.add_note_summary("반대 측(상대) 반박 완료")

        # 찬성측 반박
        if pro_side == "user":
            user_rebuttal = input(f"\n (찬성 측) 반박을 입력하세요: ")
            self.add_entry("user", user_rebuttal)
            self.add_note_summary("찬성 측(사용자) 반박 완료")
        else:
            print("\n (찬성 측) 상대의 반박 작성 중...")
            bot_rebuttal = self.get_bot_response(api_key, f"""
        너는 '{self.topic}'에 대해 '찬성' 입장인 AI야.
        반대 측 입론에 대해 논리적으로 반박해.
        반박은 3~4문장으로, 간결하고 논리적으로 해줘. 한국어로만 대답해. 외국어 사용하지 마.
        """)
            print(f"\n (찬성 측) 상대의 반박:\n{bot_rebuttal}")
            self.add_entry("assistant", bot_rebuttal)
            self.add_note_summary("찬성 측(상대) 반박 완료")

        print("\n=== 재반박 단계 ===")