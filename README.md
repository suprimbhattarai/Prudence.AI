# Prudence AI

Prudence AI is an AI-native customer-support and field-service operations platform focused first on Internet Service Providers (ISPs).

It is designed to handle the full support lifecycle:

complaint → issue understanding → troubleshooting → knowledge retrieval → allowed actions → human escalation → technician scheduling → geographically valid assignment → field visit → resolution → service report → feedback

Prudence is not intended to be only a chatbot. The long-term goal is to build a complete AI-assisted support and operations system.

---

## Current Focus

The current development focus is the ISP vertical.

The project is being built as a clean modular monolith first, with architecture that can grow without turning into large tightly-coupled files.

Current backend work includes:

- User account models
- Customer profiles
- Technician profiles
- Admin profiles
- Technician skills
- Technician teams
- Service zones
- Team-to-service-zone relationships
- PostgreSQL integration
- SQLAlchemy ORM models

Authentication, authorization, ticketing, appointments, technician scheduling, AI workflows, and the frontend will be added gradually.

---

## Core Product Flow

```text
Customer issue
    ↓
Prudence understands the complaint
    ↓
Troubleshooting
    ↓
Retrieve organization knowledge
    ↓
Take allowed actions
    ↓
Escalate to human when required
    ↓
Create ticket / appointment
    ↓
Find geographically valid technicians
    ↓
Filter by availability and required skills
    ↓
Assign technician
    ↓
Track field visit
    ↓
Resolve issue
    ↓
Generate service report
    ↓
Customer feedback
