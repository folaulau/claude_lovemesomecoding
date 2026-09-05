# Customer Data Unification Platform

## About
Design a simplified customer data unification platform.

Multiple source systems (CRM, Billing, Support) continuously emit customer record updates.
Records may conflict, arrive out of order, or be incomplete. Design a system that produces a
single trustworthy customer record and can explain why it chose each value.

## Requirements
The system should:
- Ingest customer records from multiple sources (CRM, Billing, Support)
- Handle duplicates, out-of-order events, and conflicting data
- Normalize records into a canonical schema
- Perform identity resolution (match records belonging to the same customer)
- Merge records into a unified customer profile
- Maintain an audit trail and lineage of every decision
- Emit downstream updates to consumers

Constraints given:
- Spring Boot is the backend API.
- Include a flow chart.
- Do **not** borrow from `lovemesomecoding_demo_project` — none of those apps fit this shape.
  This is a greenfield design.

## Deliverable
- `design.html` — the design document, published as an Artifact.
- `progress_report.md` — status and the decisions behind the design.
