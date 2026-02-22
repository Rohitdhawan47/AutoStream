### AutoStream Conversational AI Assistant

A stateful, production-style conversational AI system built using LangGraph, Retrieval-Augmented Generation (RAG), and local LLMs via Ollama to handle product questions, pricing queries, and lead qualification in a single continuous conversation.

This project focuses on conversation control, hallucination prevention, and business-driven dialogue, not just LLM responses.

## ✨ Key Highlights

* Built with LangGraph (graph-based conversation orchestration)

* Uses RAG for accurate pricing & plan answers

* Runs on local LLMs via Ollama (no OpenAI dependency)

* Hybrid rule-based + LLM design for reliability

* Explicit buy confirmation only (no premature lead capture)

* Persistent user memory across turns

* Designed like a real SaaS sales assistant, not a demo bot

## 🧠 Why This Architecture?
# Problems with naïve chatbots

* Hallucinate when user provides personal info

* Confuse user details with product questions

* Switch modes unpredictably

* Capture leads too early

* Repeat CTAs endlessly

# What this system fixes

* Separates user information vs product information

* Uses signals, not brittle intent modes

* Answers questions only when a question is asked

* Collects user data silently and progressively

* Submits leads only on explicit confirmation

## 🗂️ Project Structure
```
.
├── main.py                  # App entry point
├── graph.py                 # LangGraph definition
├── state.py                 # Graph state schema
├── session.py               # Persistent user memory
├── nodes/
│   ├── greeting.py          # Initial greeting
│   ├── rule_processor.py    # Slot extraction (rules + LLM fallback)
│   ├── intent_decision.py   # Intent signal detection
│   ├── llm_reply.py         # Core conversation logic
├── logic/
│   ├── extractors.py        # Regex-based field extraction
│   ├── llm_intent.py        # LLM-based intent signals
│   ├── rules.py             # Hard rules (buy phrases, question detection)
│   ├── llm_fallback.py      # LLM-based field extraction (guarded)
│   ├── lead_qualifier.py    # Lead submission logic
├── rag/
│   ├── vector_store.py      # Vector DB creation
│   ├── retriever.py         # Context retrieval
├── knowledge_base/
│   └── product.py           # Product seed (ground truth)
└── debug.py                 # Trace & debugging utilities
```
## 🔁 Conversation Flow (High Level)
```
User Input
   ↓
Rule Processor
   ↓
Intent Decision
   ↓
LLM Reply
   ↓
State Updated
```

Each user turn runs exactly once through this graph.

## 🧩 Core Components Explained
# 1️⃣ LangGraph (Conversation Orchestration)

LangGraph is used to:

1. Enforce deterministic execution order

2. Share state safely across nodes

3. Avoid recursive loops and intent chaos

Nodes are executed in this order:

1. rule_processor

2. intent_decision

3. llm_reply

This makes debugging and reasoning much easier than agent-style loops.

# 2️⃣ SessionUser (Persistent Memory)

SessionUser stores everything known about the user:
```
first_name
last_name
email
platform
plan

wants_info
wants_pricing
wants_to_buy

awaiting_slot
lead_submitted
```

This object persists across all turns and prevents the model from “forgetting”.

# 3️⃣ Rule Processor (Slot Filling Engine)

Runs before answering any question.

Responsibilities:

* Extract name, email, platform, plan using regex

* Set slot_filled_this_turn = True when data is captured

* Use LLM fallback only when rules fail

Why this matters:

“youtube, how much does it cost?”
→ platform is captured and question is answered correctly.

# 4️⃣ Intent Decision (Signals, Not Modes)

Instead of switching modes, the system detects signals:

* wants_info → product understanding

* wants_pricing → pricing & plans

* wants_to_buy → explicit confirmation only

This avoids failures like:

* “my name is Rahul” → product info ❌

* “youtube” → pricing answer ❌

# 5️⃣ LLM Reply (The Brain)

The LLM reply node controls all decisions:

Decision logic (simplified):
```
IF wants_to_buy AND all slots complete:
    submit lead

ELSE IF slot just filled AND no question:
    ask next slot

ELSE IF question exists:
    answer it (info / pricing / chat)

ELSE:
    continue slot filling
```

This guarantees:

* No hallucinations

* No premature selling

* No repeated CTAs

* No ignored questions

## 📚 Retrieval-Augmented Generation (RAG)

Used only for pricing-related questions.

Flow:

1. Retrieve relevant chunks from vector DB

2. Inject context into system prompt

3. Force LLM to answer only from retrieved data

If nothing is retrieved → graceful fallback.

This ensures:

* No made-up prices

* No plan hallucination

* Answers remain grounded

## 🦙 Ollama (Local LLMs)

This project runs on local models via Ollama, for example:

- Mistral

- LLaMA

- Gemma

# Why Ollama?

* No API cost

* Full control over data

* Resume-friendly (infra + AI)

* Easy model swapping

## ▶️ How to Run the Project
# 1️⃣ Install Requirements
```pip install langchain langgraph ollama faiss-cpu```


(Exact dependencies may vary based on your setup.)

# 2️⃣ Install & Start Ollama

```ollama run mistral```

or any supported model you prefer.

Make sure Ollama is running in the background.

# 3️⃣ Build the Vector Store

The vector store is built automatically when the app starts using content from:

```knowledge_base/product.py```

# 4️⃣ Run the Application
```python main.py```

# 5️⃣ Example Interaction
```
User: hi tell me about autostream
Bot: AutoStream helps creators edit and optimize videos automatically.
     Which platform do you mainly create for?

User: youtube
Bot: Which plan are you considering? (Basic, Pro, Enterprise)

User: pro plan
Bot: What's the best email to send your plan details to?

User: my name is Rohit Dhawan
Bot: If you'd like to move forward, just say:
     "I'll go with the Pro plan"

User: I'll go with the Pro plan
Bot: You're all set! Our team will reach out shortly.
```
## 🛑 Hallucination Prevention Techniques

* contains_question() gate

* slot_filled_this_turn flag

* Explicit buy phrases only

* No implicit intent escalation

* Slot filling runs silently


This project demonstrates:

* Stateful LLM orchestration with LangGraph

* Real-world chatbot failure mitigation

* Clear separation of concerns

* Defensive LLM design

* Business-aware conversational logic

* Hybrid rule + LLM architecture

* This is not a demo chatbot — it is a system.

### 📲 WhatsApp Deployment (Webhook Integration)

This assistant can be integrated with WhatsApp using a webhook-based architecture (e.g., Meta WhatsApp Cloud API or Twilio WhatsApp API).

## 🔁 Deployment Flow
```
User (WhatsApp)
      ↓
WhatsApp Cloud API
      ↓
Webhook (FastAPI backend)
      ↓
LangGraph Agent (rule_processor → intent → llm_reply)
      ↓
Response returned to WhatsApp API
      ↓
Message delivered to user
```

## ⚙️ Implementation Approach

# 1. Expose a Webhook Endpoint

  * Build a FastAPI server:
```
    @app.post("/webhook")
    async def receive_message(request: Request):
        data = await request.json()
        user_text = extract_whatsapp_message(data)

        state["messages"].append(HumanMessage(content=user_text))
        state = graph.invoke(state)

        reply = state["messages"][-1].content
        send_whatsapp_reply(reply)
```

# 2. Session Mapping

  * Use the WhatsApp phone number as the session key.

  * Store SessionUser objects in a dictionary or database:

```sessions[phone_number] = SessionUser()```


# 3. Preserve State

  * Each WhatsApp user maintains their own SessionUser.

  * This keeps slot filling and lead tracking persistent.

# 4. Production Considerations

  * Store session data in Redis or a database (not memory)

  * Add request verification (Meta webhook signature validation)

  * Deploy using Docker + cloud VM or container service

## 🏁 Final Note

LLMs are powerful, but unreliable without structure.
This architecture treats the LLM as a component, not the controller.

That’s the difference between a prototype and production.