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
    
         # 찬성측 재반박
        if pro_side == "user":
            user_re_rebuttal = input(f"\n (찬성 측) 재반박을 입력하세요: ")
            self.add_entry("user", user_re_rebuttal)
            self.add_note_summary("찬성 측(사용자) 재반박 완료")
        else:
            print("\n (찬성 측) 상대의 재반박 작성 중...")
            bot_re_rebuttal = self.get_bot_response(api_key, f"""
        너는 '{self.topic}'에 대해 '찬성' 입장인 AI야.
        반대 측 반박에 대해 논리적으로 재반박해.
        논리적이고 간결하게 2~3문장으로만 반박하며, 명확하게 작성해줘. 한국어로만 대답해. 외국어를 사용하지마.
        """)
            print(f"\n (찬성 측) 상대의 재반박:\n{bot_re_rebuttal}")
            self.add_entry("assistant", bot_re_rebuttal)
            self.add_note_summary("찬성 측(상대) 재반박 완료")

        # 반대측 재반박
        if con_side == "user":
            user_re_rebuttal = input(f"\n (반대 측) 재반박을 입력하세요: ")
            self.add_entry("user", user_re_rebuttal)
            self.add_note_summary("반대 측(사용자) 재반박 완료")
        else:
            print("\n (반대 측) 상대의 재반박 작성 중...")
            bot_re_rebuttal = self.get_bot_response(api_key, f"""
        너는 '{self.topic}'에 대해 '반대' 입장인 AI야.
        찬성 측 재반박에 대해 논리적으로 재반박해.
        논리적이고 간결하게 2~3문장으로만 반박하며, 명확하게 작성해줘. 한국어로만 대답해. 외국어 사용하지마. 
        """)
            print(f"\n (반대 측) 상대의 재반박:\n{bot_re_rebuttal}")
            self.add_entry("assistant", bot_re_rebuttal)
            self.add_note_summary("반대 측(상대) 재반박 완료")

        print("\n=== 최종 정리 단계 ===")

        # 찬성측 최종 정리
        if pro_side == "user":
            user_summary = input(f"\n (찬성 측) 최종 정리 발언을 입력하세요: ")
            self.add_entry("user", user_summary)
            self.add_note_summary("찬성 측(사용자) 최종 정리 발언 완료")
        else:
            print("\n (찬성 측) 상대의 최종 정리 작성 중...")
            bot_summary = self.get_bot_response(api_key, f"""
        너는 '{self.topic}'에 대해 '찬성' 입장인 AI야.
        최종 정리 발언으로 자신의 입장을 다시 강조하고 마무리 멘트를 작성해.
        3~4문장으로 핵심만 강조해. 한국어로만 대답해. 외국어 절대 사용하지마.
        """)
            print(f"\n (찬성 측) 상대의 최종 정리:\n{bot_summary}")
            self.add_entry("assistant", bot_summary)
            self.add_note_summary("찬성 측(상대) 최종 정리 발언 완료")

        # 반대측 최종 정리
        if con_side == "user":
            user_summary = input(f"\n (반대 측) 최종 정리 발언을 입력하세요: ")
            self.add_entry("user", user_summary)
            self.add_note_summary("반대 측(사용자) 최종 정리 발언 완료")
        else:
            print("\n (반대 측) 상대의 최종 정리 작성 중...")
            bot_summary = self.get_bot_response(api_key, f"""
        너는 '{self.topic}'에 대해 '반대' 입장인 AI야.
        최종 정리 발언으로 자신의 입장을 다시 강조하고 마무리 멘트를 작성해.
        3~4문장으로 핵심만 강조해. 한국어로만 대답해. 외국어 절대 사용하지마.
        """)
            print(f"\n (반대 측) 상대의 최종 정리:\n{bot_summary}")
            self.add_entry("assistant", bot_summary)
            self.add_note_summary("반대 측(상대) 최종 정리 발언 완료")

    def request_feedback(self, api_key, model="deepseek/deepseek-r1:free"):
        messages = [
            {"role": "system", "content": f"""
        너는 토론 평가를 해주는 AI 코치야.
        아래는 '{self.topic}' 주제로 진행된 토론 기록이야. 사용자의 입장은 '{self.user_stance}'이고, 너는 '{self.bot_stance}' 입장이었어.
        {self.user_stance}에 대한 전체 피드백을 줘. 논리성, 표현, 개선점 등을 언급해줘. 고쳤으면 하는 부분은 잘 지적해주고, {self.bot_stance}에서 잘한 점은 장점으로 언급하며 이것처럼 해도 좋다는 피드백도 줘. 
        마지막에 '이번 토론에서 나아진 점:'이라는 항목으로 간단히 정리해줘. 한국어로만 대답해. 짧고 간결하게 말해.
        """}
        ] + self.chat_log

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
        self.feedback = reply

        if "이번 토론에서 나아진 점:" in reply:
            self.improvements.append(reply.split("이번 토론에서 나아진 점:")[-1].strip())

        return reply

    def save_to_json(self, base_directory="debate_logs"):
        category_dir = os.path.join(base_directory, self.category)
        os.makedirs(category_dir, exist_ok=True)

        data = {
            "timestamp": self.time,
            "topic": self.topic,
            "category": self.category,
            "user_level": self.user_level,
            "difficulty": self.difficulty,
            "user_stance": self.user_stance,
            "bot_stance": self.bot_stance,
            "chat_log": self.chat_log,
            "feedback": self.feedback,
            "improvements": self.improvements,
            "notes": self.summary_notes
        }

        safe_topic = self.topic.replace(" ", "_").replace("/", "_")
        filename = os.path.join(category_dir, f"{safe_topic}_{self.time.replace(':', '-').replace(' ', '_')}.json")
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        return filename


#주제 추천 받기
def get_topic_suggestion(api_key, system_prompt, model="deepseek/deepseek-r1:free"):
    messages = [{"role": "system", "content": system_prompt}]
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
    reply = response.json()["choices"][0]["message"]["content"].strip()
    return reply

#실행파트
if __name__ == "__main__":
    api_key = input("OpenRouter API 키를 입력하세요: ")
    user_level = input("원하는 수준을 선택하세요 (중학생 / 고등학생 / 대학생): ")
    difficulty = input("난이도를 선택하세요 (상 / 중 / 하): ")
    category = input("카테고리를 선택하세요 (윤리 / 사회 / 법 / 기술 / 환경): ")

    system_prompt = f"""
    너는 AI 토론 주제 제안자야.
    카테고리는 '{category}'이고, 사용자의 수준은 '{user_level}', 난이도는 '{difficulty}'야.
    카테고리, 사용자 수준, 난이도를 모두 고려해서 적절한 한국어 토론 주제를 1개 추천해줘. 
    토론 주제는 명확한 찬반 논쟁이 가능한 형태로 제시해. 
    주제에 대해서 찬성과 반대입장이 나오도록 vs같은 표현은 쓰지마.
    한 문장으로 주제만 이야기 해. 

"""

   #주제 반복해서 받기
    while True:
        suggested_topic = get_topic_suggestion(api_key, system_prompt)
        print(f"\n 추천 주제:\n {suggested_topic}")

        user_choice = input("\n이 주제를 사용할까요? (Enter = 예, 아니오면 '다른 주제' 입력): ").strip()
        if user_choice == "":
            topic = suggested_topic
            break
        else:
            print("\n 새로운 주제를 생성 중입니다...\n")
           

    debate = DebateSession(topic, category, user_level, difficulty)
    debate.run_debate(api_key)

    print("\n 피드백 요청 중...")
    feedback = debate.request_feedback(api_key)
    print(f"\n 피드백:\n{feedback}")

    saved_path = debate.save_to_json()
    print(f"\n 토론 결과가 저장되었습니다: {saved_path}")
