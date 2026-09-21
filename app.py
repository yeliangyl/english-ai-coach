
import json
import os
import tempfile
import random
from pathlib import Path

import streamlit as st
from openai import OpenAI

APP_DIR = Path(__file__).parent
MEMORY_FILE = APP_DIR / "memory.json"

STARTING_QUESTIONS = [
    "What did you have for breakfast today?",
    "How has your day been so far?",
    "What are you planning to do this weekend?",
    "What is something interesting that happened recently?",
    "What do you usually do after dinner?",
    "Have you watched any good movies or shows recently?",
    "What kind of food do you usually cook at home?",
    "Did you go anywhere interesting last weekend?",
    "What is something you want to improve this year?",
    "What do you usually do when you have some free time?",

    "What is your favorite meal of the day?",
    "Do you prefer cooking at home or eating out?",
    "What is a restaurant you really like?",
    "What food do you miss from China?",
    "Is there any Canadian food you enjoy?",
    "What dish are you best at cooking?",
    "What do you usually drink in the morning?",
    "Do you like spicy food? Why or why not?",
    "What is one food you never get tired of?",
    "What is something you ate recently that was really good?",

    "What do you usually do on Saturday mornings?",
    "How do you normally spend Sunday?",
    "Do you prefer staying home or going out on weekends?",
    "What is your ideal weekend like?",
    "Where do you like to go for a short drive?",
    "What is a place near Vancouver that you enjoy visiting?",
    "Do you like going to the beach?",
    "What do you usually do when the weather is nice?",
    "What do you usually do on rainy days?",
    "What is one place you would like to visit again?",

    "What was your last trip like?",
    "Do you prefer road trips or flying?",
    "What is the most beautiful place you have visited?",
    "What kind of places do you like to visit when traveling?",
    "Do you like planning trips in advance?",
    "What is one city you would like to visit someday?",
    "Would you rather visit the mountains or the ocean?",
    "What do you usually pack for a short trip?",
    "What is the longest road trip you have ever taken?",
    "What is something that can make a trip stressful?",

    "What do you usually buy at the supermarket?",
    "Do you make a shopping list before going to the store?",
    "What is something that has become more expensive recently?",
    "Do you prefer shopping online or in stores?",
    "What was the last thing you bought online?",
    "What kind of products do you compare carefully before buying?",
    "Do you enjoy shopping for clothes?",
    "What is one thing you think is overpriced?",
    "What do you usually look for when buying a new product?",
    "Have you ever bought something and regretted it?",

    "What kind of car do you drive?",
    "What do you like most about your car?",
    "What is something you do not like about your car?",
    "Do you enjoy driving?",
    "What is traffic usually like where you live?",
    "Do you prefer SUVs or sedans?",
    "What feature is most important to you when buying a car?",
    "Have you ever taken a long road trip in Canada?",
    "What makes a car comfortable for you?",
    "Would you consider buying an electric car?",

    "What kind of work do you enjoy doing?",
    "What part of your job is the most challenging?",
    "What part of your job do you enjoy the most?",
    "How has technology changed the way you work?",
    "Do you think AI makes your work easier?",
    "What skill would you like to improve for your career?",
    "Do you prefer working alone or with a team?",
    "What makes a good coworker?",
    "What makes a good manager?",
    "What do you usually do when you have a difficult problem at work?",

    "How often do you use AI tools?",
    "What do you usually use ChatGPT for?",
    "Do you think AI will change many jobs?",
    "What technology do you use every day?",
    "What app do you use the most?",
    "Is there any technology you find frustrating?",
    "Would you like to build your own app someday?",
    "What kind of app would be useful in your daily life?",
    "Do you think people spend too much time on their phones?",
    "What is one piece of technology you could not live without?",

    "What do you usually do to relax?",
    "Do you have any hobbies?",
    "What kind of videos do you watch online?",
    "What kind of music do you listen to?",
    "Do you prefer movies or TV shows?",
    "What was the last movie you watched?",
    "Do you like reading books?",
    "What is something you would like to learn for fun?",
    "Do you enjoy taking photos?",
    "What is one hobby you would like to try?",

    "How often do you exercise?",
    "What kind of exercise do you enjoy?",
    "Do you prefer walking indoors or outdoors?",
    "What do you usually do to stay healthy?",
    "Do you pay attention to what you eat?",
    "What is one healthy habit you want to develop?",
    "How many hours do you usually sleep?",
    "Do you think you get enough sleep?",
    "What helps you feel less stressed?",
    "What is something you do to feel better after a tiring day?",

    "What do you like most about living in Canada?",
    "What do you miss most about living in China?",
    "What surprised you most after moving to Canada?",
    "What is one difference between life in Canada and China?",
    "Do you think Vancouver is a good place to live?",
    "What do you like most about the Vancouver area?",
    "What do you dislike about Vancouver?",
    "Do you prefer big cities or smaller cities?",
    "What makes a city a good place to live?",
    "If you could live anywhere for one year, where would you choose?"
]

st.set_page_config(page_title="English AI Coach", page_icon="🎤", layout="centered")

SYSTEM_PROMPT = """
You are a patient but demanding English speaking coach.

The student's goal is to improve spoken everyday English.
The student does NOT want to choose topics. You must drive the conversation.

For every student answer:
1. Understand what the student means before correcting.
2. Identify only the 1-3 most useful grammar mistakes. Do not nitpick every tiny issue.
3. Identify up to 2 unnatural expressions and suggest natural alternatives.
4. Give a concise explanation in Chinese.
5. Give a polished natural-English version of the student's answer.
6. Ask exactly ONE follow-up question based on the student's answer.
7. Keep the conversation alive. Never ask "What would you like to talk about?"
8. Gradually increase difficulty when the student is doing well.
9. Pay special attention to the student's recurring mistakes listed in memory.
10. If the student gives a very short answer, ask a concrete follow-up question.
11. If there are no important errors, say so briefly and focus on naturalness.
12. Avoid repeatedly asking about yesterday, work, school, or the same topic.
13. Vary topics naturally across daily life, family, food, shopping, travel,
    hobbies, news, plans, opinions, and experiences.
14. Follow the current topic for 2-4 questions when it is interesting, then
    naturally move to a new topic instead of staying on one subject too long.
15. Prefer questions that encourage the student to explain, describe, compare,
    give an opinion, or tell a short story instead of questions that can be
    answered with only yes or no.
16. Write spoken_feedback entirely in natural conversational English. Keep it concise
    and easy to understand when heard aloud. Explain the most useful corrections
    and natural alternatives.

Return valid JSON with exactly these keys:
{
  "feedback": {
    "summary": "...",
    "grammar": [
      {"original": "...", "correction": "...", "explanation": "..."}
    ],
    "natural": [
      {"original": "...", "better": "...", "explanation": "..."}
    ],
    "better_answer": "...",
    "spoken_feedback": "Short natural English feedback designed to be spoken aloud."
  },
  "next_question": "...",
  "new_memory": [
    {"category": "grammar|vocabulary|natural_expression", "mistake": "...", "better": "..."}
  ]
}
"""

def load_memory():
    if not MEMORY_FILE.exists():
        return []
    try:
        return json.loads(MEMORY_FILE.read_text(encoding="utf-8"))
    except Exception:
        return []

def save_memory(memory):
    MEMORY_FILE.write_text(
        json.dumps(memory[-30:], ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

def get_client():
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        st.error("没有找到 OPENAI_API_KEY。请先设置环境变量。")
        st.stop()
    return OpenAI(api_key=key)

def transcribe(client, audio_file):
    suffix = Path(audio_file.name).suffix or ".wav"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as f:
        f.write(audio_file.getvalue())
        path = f.name
    try:
        with open(path, "rb") as audio:
            result = client.audio.transcriptions.create(
                model="gpt-4o-mini-transcribe",
                file=audio
            )
        return result.text
    finally:
        try:
            os.remove(path)
        except OSError:
            pass

def coach_turn(client, history, answer, memory):
    memory_text = json.dumps(memory[-12:], ensure_ascii=False)

    input_text = [
        {
            "role": "developer",
            "content": SYSTEM_PROMPT + "\n\nStudent memory:\n" + memory_text
        }
    ]

    input_text.extend(history[-8:])
    input_text.append({
        "role": "user",
        "content": answer
    })

    response = client.responses.create(
        model="gpt-5.6-luna",
        input=input_text,
        text={
            "format": {
                "type": "json_schema",
                "name": "english_coach_response",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "feedback": {
                            "type": "object",
                            "properties": {
                                "summary": {
                                    "type": "string"
                                },
                                "grammar": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "original": {
                                                "type": "string"
                                            },
                                            "correction": {
                                                "type": "string"
                                            },
                                            "explanation": {
                                                "type": "string"
                                            }
                                        },
                                        "required": [
                                            "original",
                                            "correction",
                                            "explanation"
                                        ],
                                        "additionalProperties": False
                                    }
                                },
                                "natural": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "original": {
                                                "type": "string"
                                            },
                                            "better": {
                                                "type": "string"
                                            },
                                            "explanation": {
                                                "type": "string"
                                            }
                                        },
                                        "required": [
                                            "original",
                                            "better",
                                            "explanation"
                                        ],
                                        "additionalProperties": False
                                    }
                                },
                                "better_answer": {
                                    "type": "string"
                                },
                                "spoken_feedback": {
                                    "type": "string"
                                }
                            },
                            "required": [
                                "summary",
                                "grammar",
                                "natural",
                                "better_answer",
                                "spoken_feedback"
                            ],
                            "additionalProperties": False
                        },
                        "next_question": {
                            "type": "string"
                        },
                        "new_memory": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "category": {
                                        "type": "string",
                                        "enum": [
                                            "grammar",
                                            "vocabulary",
                                            "natural_expression"
                                        ]
                                    },
                                    "mistake": {
                                        "type": "string"
                                    },
                                    "better": {
                                        "type": "string"
                                    }
                                },
                                "required": [
                                    "category",
                                    "mistake",
                                    "better"
                                ],
                                "additionalProperties": False
                            }
                        }
                    },
                    "required": [
                        "feedback",
                        "next_question",
                        "new_memory"
                    ],
                    "additionalProperties": False
                }
            }
        }
    )

    return json.loads(response.output_text)

def speak(client, text):
    response = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="marin",
        input=text,
        speed=1.0,
        instructions=(
            "Speak in a natural North American English accent. "
            "Use a relaxed, conversational tone like an adult speaking "
            "in everyday life in the United States or Canada. "
            "Use natural rhythm, sentence stress, linking, and intonation. "
            "Do not speak like a language teacher or a news announcer. "
            "Do not exaggerate pronunciation. "
            "Speak at a normal native conversational speed."
        )
    )
    
    return response.read()

def get_new_starting_question():
    # Avoid repeating any of the 10 most recently used starting questions.
    recent_questions = st.session_state.get("recent_starting_questions", [])

    choices = [
        q for q in STARTING_QUESTIONS
        if q not in recent_questions
    ]

    if not choices:
        recent_questions = []
        choices = STARTING_QUESTIONS.copy()

    question = random.choice(choices)
    recent_questions.append(question)
    st.session_state.recent_starting_questions = recent_questions[-10:]

    return question

if "history" not in st.session_state:
    st.session_state.history = []
if "question" not in st.session_state:
    st.session_state.question = get_new_starting_question()
if "last_feedback" not in st.session_state:
    st.session_state.last_feedback = None
if "turn" not in st.session_state:
    st.session_state.turn = 0

memory = load_memory()

st.title("🎤 English AI Coach")
st.caption("AI 主动提问 → 你回答 → 纠错 → 根据你的回答继续追问")

with st.sidebar:
    st.subheader("今日练习")
    st.write(f"第 {st.session_state.turn} 轮")
    st.write(f"已记录错误：{len(memory)} 条")
    if st.button("清空学习记录"):
        save_memory([])
        st.session_state.history = []
        st.session_state.turn = 0
        st.session_state.question = get_new_starting_question()
        st.session_state.last_feedback = None
        st.rerun()

st.subheader("AI Question")

client = get_client()

question_audio_key = f"question_audio_{st.session_state.turn}"

# 每一道新问题只调用一次 OpenAI TTS
if question_audio_key not in st.session_state:
    with st.spinner("AI is asking the question..."):
        st.session_state[question_audio_key] = speak(
            client,
            st.session_state.question
        )

# 只创建一个 audio 元素
st.audio(
    st.session_state[question_audio_key],
    format="audio/mp3",
    autoplay=True
)

# Show / Hide question text
show_text_key = f"show_question_text_{st.session_state.turn}"

if show_text_key not in st.session_state:
    st.session_state[show_text_key] = False

if st.button(
    "👀 Show / Hide question text",
    key=f"show_button_{st.session_state.turn}"
):
    st.session_state[show_text_key] = (
        not st.session_state[show_text_key]
    )

if st.session_state[show_text_key]:
    st.info(st.session_state.question)

st.divider()
st.subheader("Your Answer")

audio = st.audio_input(
    "🎤 直接说英语",
    key=f"audio_answer_{st.session_state.turn}"
)

typed = st.text_area(
    "或者先用文字测试",
    placeholder="Type your English answer here...",
    height=100,
    key=f"text_answer_{st.session_state.turn}"
)

answer = None
if audio is not None:
    answer = "__AUDIO__"
elif typed.strip():
    answer = typed.strip()

if st.button("Submit Answer", type="primary"):
    if not answer:
        st.warning("请录音或输入一句英语。")
        st.stop()

    client = get_client()

    with st.spinner("AI 正在分析你的英语..."):
        if answer == "__AUDIO__":
            answer_text = transcribe(client, audio)
        else:
            answer_text = answer

        try:
            result = coach_turn(
                client,
                st.session_state.history,
                answer_text,
                memory
            )
        except Exception as exc:
            st.error("这次 AI 处理失败，请稍后重试。")
            st.code(str(exc))
            st.stop()

    st.session_state.history.append(
        {"role": "user", "content": answer_text}
    )
    st.session_state.history.append(
        {"role": "assistant", "content": result["next_question"]}
    )
    st.session_state.turn += 1
    st.session_state.question = result["next_question"]
    st.session_state.last_feedback = result

    new_items = result.get("new_memory", [])
    if new_items:
        memory.extend(new_items)
        save_memory(memory)

    st.rerun()

if st.session_state.last_feedback:
    result = st.session_state.last_feedback

    st.divider()
    st.subheader("📝 Feedback")

    st.success(result["feedback"]["summary"])

    spoken_feedback = result["feedback"].get("spoken_feedback", "")
    if spoken_feedback:
        st.markdown("### 🎧 English Feedback")
        st.write(spoken_feedback)

        if st.button(
            "🔊 Listen to English Feedback",
            key=f"spoken_feedback_audio_{st.session_state.turn}"
        ):
            client = get_client()
            feedback_audio = speak(client, spoken_feedback)
            st.audio(
                feedback_audio,
                format="audio/mp3",
                autoplay=True
            )

    grammar = result["feedback"].get("grammar", [])
    if grammar:
        st.markdown("### Grammar")
        for item in grammar:
            st.markdown(
                f"**❌ {item['original']}**  \n"
                f"**✅ {item['correction']}**  \n"
                f"{item['explanation']}"
            )

    natural = result["feedback"].get("natural", [])
    if natural:
        st.markdown("### More Natural English")
        for item in natural:
            st.markdown(
                f"**{item['original']} → {item['better']}**  \n"
                f"{item['explanation']}"
            )

    st.markdown("### ⭐ Better Version")

    better_answer = result["feedback"]["better_answer"]

    st.write(better_answer)

    if st.button(
        "🔊 Listen to Better Version",
        key=f"better_answer_audio_{st.session_state.turn}"
    ):
        client = get_client()
        better_audio = speak(client, better_answer)
        st.audio(
            better_audio,
            format="audio/mp3",
            autoplay=True
        )
