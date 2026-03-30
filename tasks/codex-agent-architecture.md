# Codex Agent Architecture

This repository currently uses a simple role split for collaborative work.

- Planner Agent
  Clarifies scope, assumptions, and the smallest useful plan.
- Coder Agent
  Implements focused changes with minimal disruption.
- Reviewer Agent
  Looks for defects, regressions, and missing validation.
- Tester Agent
  Confirms what was verified and what remains unverified.

These roles are lightweight guides and can evolve with the project.
