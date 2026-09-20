# Victor Bello

### AI Automation Specialist · n8n Workflow Developer · API & Business Process Automation

I build practical automation systems that help businesses **respond faster, reduce repetitive work, and move important data reliably between tools**.

My focus is production-minded workflow automation: secure webhook intake, API integrations, data normalization, routing logic, duplicate-safe processing, persistent state, notifications, retries, and clear failure handling.

---

## Featured Project — RapidHome Lead Automation

**Secure n8n lead intake, qualification, storage, and response workflow for home-service businesses.**

[View the project →](https://github.com/azvicbello-cmd/rapidhhome-n8n-lead-automation)

### What it demonstrates

- Authenticated inbound webhook intake
- **HMAC-SHA256** request-signature verification
- Raw-body validation before processing
- JavaScript lead normalization and deterministic scoring
- Stable idempotency keys
- Persistent lead storage with n8n Data Tables
- Duplicate detection to prevent repeat processing
- **HOT / WARM / COLD** lead routing
- Immediate Telegram escalation for urgent leads
- Retry and failure-handling paths
- Structured API responses for success, duplicates, authorization failures, and downstream errors

### Architecture

```text
Authenticated Webhook
        |
        v
HMAC-SHA256 Verification
     /         \
 valid       invalid
   |            |
   v            v
Normalize     HTTP 401
& Score
   |
   v
Duplicate Protection
   |
   v
Persistent Storage
   |
   v
HOT / WARM / COLD Routing
   |       |        |
   v       v        v
Urgent   Follow-   Nurture
Alert      up
```

> The current qualification logic is deterministic and rule-based. I do not present it as LLM-powered when it is not. AI enrichment can be added as a separate layer when the business case actually benefits from it.

---

## What I Build

- Lead capture and response automation
- CRM and webhook workflows
- API-to-API integrations
- Business process automation
- Data validation and transformation pipelines
- Notification and escalation systems
- Duplicate-safe / idempotent workflows
- Retry logic and explicit failure handling
- AI-assisted workflow layers where they add measurable value

---

## Business Problems I Like Solving

**Slow lead response** → automatically classify and escalate urgent enquiries.

**Repeated webhook deliveries** → prevent duplicate records and duplicate actions.

**Manual handoffs** → route information automatically to the right path or person.

**Silent integration failures** → build retries, error branches, and structured responses.

**Messy inbound data** → normalize and validate before downstream processing.

**Weak webhook security** → add authentication and request-integrity verification.

---

## Technical Toolkit

**Automation:** n8n · Webhooks · Conditional Routing · Data Tables  
**Integration:** REST APIs · JSON · HMAC-SHA256 · Authentication  
**Logic:** JavaScript · Data Normalization · Validation · Idempotency  
**Reliability:** Retry Logic · Failure Handling · Structured API Responses  
**Notifications:** Telegram integrations and escalation workflows

---

## How I Approach Automation

I prefer systems that are:

- **Secure** — authentication and request validation are designed in
- **Reliable** — retries and failure paths are intentional
- **Idempotent** — repeated events do not create uncontrolled duplicate actions
- **Observable** — workflows return clear, structured outcomes
- **Honest** — deterministic automation and actual AI/LLM functionality are clearly distinguished
- **Adaptable** — client-specific rules and integrations can change without rebuilding the entire core workflow

---

## Current Focus

I am building automation solutions for service businesses and operational teams where faster response, cleaner data flow, and fewer manual handoffs can improve day-to-day operations.

I am open to **AI automation, n8n workflow development, API integration, and business process automation** opportunities.

---

## Connect

**LinkedIn:** [Victor Bello](https://www.linkedin.com/in/victor-bello-az)  
**Featured project:** [RapidHome n8n Lead Automation](https://github.com/azvicbello-cmd/rapidhhome-n8n-lead-automation)
