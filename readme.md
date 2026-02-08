# AutoStream Conversational Assistant

A stateful, sales-aware SaaS chatbot built with LangGraph, LLM grounding, and controlled lead capture.

This system is designed to:

answer product & pricing questions accurately (no hallucinations)

silently collect lead details over time

only capture a lead when the user explicitly commits

avoid intent loops, double replies, and false slot extraction

> 🧠 Core Design Philosophy

Do not over-classify intent.
Do not trust the LLM blindly.
Do not ask for user details unless there is buying intent.

Instead:

Rules decide hard business signals

LLM helps with language understanding

State controls what is allowed to happen next
```
🧱 High-Level Architecture
User Input
   ↓
rule_processor_node
   ↓
intent_node
   ↓
llm_reply_node
   ↓
END
```

There is no looping in the graph.
Each user message produces exactly one assistant reply.

## 🗂️ Key Components
# 1️⃣ SessionUser (Persistent User State)

Holds everything we know about the user across turns.
```
class SessionUser:
    first_name
    last_name
    email
    platform
    plan

    wants_to_buy       # explicit confirmation only
    lead_submitted     # prevents duplicate capture
```

Important rules:

wants_to_buy is false by default

It turns true only if user says something like:

“I want to buy the Pro plan”

# 2️⃣ AgentState (LangGraph State)
```
class AgentState(TypedDict):
    messages: List[BaseMessage]
    trace: List[str]
    session_user: SessionUser
    vector_store: FAISS
```

messages → conversation history

trace → debugging (node execution order)

session_user → long-term memory

vector_store → pricing knowledge base

# 🔍 Intent Handling (Minimal by Design)
```
detect_intent (rules first)

Rules exist only to detect strong signals:

Intent	Example
lead	“buy”, “go with pro”, “sign up”
pricing	“price”, “plans”, “cost”
info	“what is”, “tell me about”
chat	everything else```

Priority order (critical):

lead > pricing > info > chat


This avoids:

“pro plan” being misread as pricing

buying intent being downgraded

intent_node

Calls decide_intent

Sets:

state["route"]

session_user.mode

Lead mode persists unless explicitly overridden.

# 🧠 llm_reply_node (The Brain)

This node does everything related to replying.

Execution Order
- 1️⃣ Detect intent signals

pricing?

info?

chat?

- 2️⃣ Detect hard buy confirmation
`
if wants_to_buy(text):
    session_user.wants_to_buy = True`


This is the only place buying intent is allowed.

- 3️⃣ Close the deal (only if allowed)
if session_user.wants_to_buy and session_user.is_complete():
    mock_lead_capture(...)


No email? No platform? No plan?
👉 No lead capture. Period.

- 4️⃣ Answer the user
Signal	Source
pricing	RAG (autostream_docs.txt)
info	PRODUCT_SEED
chat	free LLM

All answers are:

short

grounded

non-invented

# 📦 RAG (Pricing Only)

Vector store: FAISS

Source: autostream_docs.txt

Used only for pricing

retrieve_context(vector_store, query)


If similarity is weak → fallback response.

No hallucinated pricing. Ever.

# 🧾 Rule Processor (Slot Filling)
rule_processor_node

Runs before intent and reply.

Extracts only when appropriate:

name → only after we ask for name

email → regex

platform → keyword match

plan → controlled vocabulary

LLM fallback is:

guarded

optional

never first choice

🚫 What This System Intentionally Avoids

❌ Intent routers everywhere

❌ Multiple reply nodes

❌ Graph loops

❌ Over-reliance on LLM classification

❌ Capturing leads without consent

🧪 Example Flow
User: tell me about autostream
→ info → PRODUCT_SEED reply + CTA

User: what are the plans
→ pricing → RAG reply + CTA

User: I’ll go with Pro plan
→ wants_to_buy = True

User: my email is x@y.com
→ slot filled

User: I create for YouTube
→ slot filled

→ lead captured

🧠 Why This Architecture Works

Deterministic where it matters

Flexible where language is messy

Sales-aligned, not chatbot-academic

Easy to debug (traceable, linear)