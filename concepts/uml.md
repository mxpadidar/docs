# UML Cheat Sheet for Modeling Auth Domain Class Diagrams


1 — Purpose and scope
- UML (Unified Modeling Language) is a visual language to describe software structure and behavior.
- This doc focuses on class diagrams and relationships (association, multiplicity, aggregation, composition) and how to model auth entities (User, Session, RefreshToken, AuthTicket). It intentionally omits behavioral diagrams (sequence, activity, state) except where briefly noted.

2 — Class diagram basics
- Class box: three compartments
  1. Name (top) — class name or stereotype (e.g., <<enumeration>>).
  2. Attributes (middle) — name: type, optional visibility (+ public, - private).
  3. Operations (bottom) — methods (not required for data model diagrams).
- Stereotypes: annotate special classes (<<enumeration>>, <<value object>>, <<entity>>).
- Notes: attach textual constraints or invariants using a note element.

3 — Associations (general)
- Definition: a structural relationship showing that instances of one class are connected to instances of another.
- Notation: plain solid line between classes. Optionally label the role names near each end.
- Semantics: associations do not imply ownership or lifecycle constraints by themselves — they express references/links.

4 — Multiplicity
- Multiplicities are properties on each end of an association; they indicate how many instances of the target can be associated with a single instance of the source.
- Common notations:
  - 1 = exactly one
  - 0..1 = zero or one (optional)
  - * or 0..* = zero or many
  - 1..* = one or many
  - n..m = specific range
- Best practice: show multiplicities on both ends for precision (e.g., 1 — *). It's acceptable to show only the side that needs clarification, but showing both is clearer.
- Example reading: [1] user.id ---- session.user_id [0..*] means: each User (1) may be referenced by 0..* Sessions; each Session references exactly 1 User.

5 — Role names and navigation
- Role names: optional labels at each end that describe the role (e.g., user.sessions). Useful when classes appear multiple times or relationships are ambiguous.
- Navigation: associations are navigable by default both ways, but you can indicate unidirectional navigation with an open arrowhead. Most data models treat FKs as navigable in both directions (but implementations may restrict).

6 — Aggregation vs Composition
- Both are special kinds of association used to document whole–part relationships; they are semantic hints, not enforcement.
- Aggregation (hollow diamond on the “whole” end)
  - Meaning: whole–part with weak ownership. Parts can exist independently and may be shared by multiple wholes.
  - Use-case: "Session aggregates RefreshTokens" — tokens conceptually belong to a session but have independent identity/history.
- Composition (filled diamond on the “whole” end)
  - Meaning: strong ownership, part's lifecycle is bound to the whole. When whole is destroyed, parts should be destroyed; parts typically have no meaning outside the whole.
  - Use-case: rare in auth systems. Only use if you guarantee strict cascading delete and parts have no independent identity.
- Practical note: many practitioners avoid UML composition unless lifecycle semantics are strict. Implement lifecycle rules in code/DB, and use aggregation/composition primarily for documentation.

7 — When to model which relation type in auth domain
- Plain association: default for references and FKs.
  - session.user_id -> user.id   (session references user; user is not a part of a session)
  - auth_ticket.user_id -> user.id (optional association)
- Aggregation (optional, for documentation): indicates grouping/ownership but not tight lifecycle coupling.
  - session (whole) —◊— refresh_token (part)  (Session aggregates RefreshTokens)
  - user (whole) —◊— session (part)  (optional: User aggregates Sessions)
- Composition (rare): only if you guarantee deletion-of-parent => deletion-of-children and children have no identity outside parent.

8 — Constraints, invariants, and nullability
- Express domain rules with OCL-like notes or plain text notes attached to the class or association.
- Examples for your domain:
  - AuthTicket conditional nullability: "if intent == REGISTER then user_id MUST be NULL; if intent ∈ {RESET_PWD, CHANGE_PWD} then user_id MUST be NOT NULL".
  - RefreshToken reuse rule: "if refresh token reused (revoked token re-presented) -> immediately set Session.status = REVOKED".
- Mark fields optional explicitly (0..1) and required (1). Also note which fields are hashed or sensitive (e.g., token_hash stored hashed).

9 — Full relation list for your model (with types and multiplicities)
- [1] user.id ---- auth_ticket.user_id [0..1]
  Type: association (optional on ticket side). A User may have many tickets; a ticket may reference zero or one User.

- [1] user.id ---- session.user_id [0..*]
  Type: association (many-to-one). A User may have many Sessions; each Session references exactly one User.

- [0..1] auth_ticket.id ---- session.ticket_id [0..1]
  Type: association (optional). A Session may be linked to one AuthTicket and a ticket may be consumed to create at most one Session.

- [1] session.uuid ---- refresh_token.session_uuid [0..*]
  Type: association (many-to-one). A Session may have many RefreshTokens; each RefreshToken belongs to exactly one Session. Consider documenting as aggregation (Session aggregates RefreshTokens).

- [1] user.id ---- refresh_token.user_id [0..*]
  Type: association (many-to-one). A User may have many RefreshTokens; each RefreshToken belongs to exactly one User.

10 — Example attribute annotations (how to display in class box)
- Use +/- for visibility and annotate optional fields with "?: type" or with multiplicity. Example:
  - + id: int
  - + user_id: int  // FK to User.id (1..1)
  - + ticket_id: int?  // nullable FK (0..1)
  - + token_hash: str  // stored hashed
  - + revoked_at: datetime?  // optional timestamp

11 — Cardinality placement conventions
- Multiplicity appears at each association end; it's a property of that end.
- It's common to only write the multiplicity on the "many" side to save space, but this loses clarity. Prefer both ends in precise technical diagrams.

12 — Visual conventions and glyphs
- Association: solid line.
- Directed association / navigation: open arrow at navigable end.
- Aggregation: hollow diamond at whole end.
- Composition: filled diamond at whole end.
- Multiplicity: numbers or ranges near ends (e.g., 1, 0..1, *, 1..*).
- Notes: use a note box connected with a dashed line for constraints or explanation.

13 — Practical modeling advice (applied)
- Prefer plain associations for FKs. Add multiplicities at both ends.
- Use aggregation to convey grouping (Session aggregates RefreshTokens) — helpful for reviewers, optional for implementers.
- Avoid composition unless you truly enforce child deletion and children have no independent identity.
- Model nullable FKs explicitly (0..1) and express domain invariants as notes.
- Keep enums (AuthMethod, SessionStatus, UserSex) as <<enumeration>> elements and reference them by type in attributes.
- Index and uniqueness: add small notes for important DB constraints (e.g., unique(session.uuid), index(refresh_token.token_hash)).

14 — Security & lifecycle notes (domain-specific)
- session.uuid is your jti (JWT ID). Mark it unique and indexed. Document that session.uuid is stable for the session lifetime.
- RefreshToken records store token_hash only (never store raw token). Add an attribute note: token_hash: str (hashed).
- Rotation model:
  - RefreshToken has revoked_at, replaced_by (optional) to track rotations and reuse detection. Add revoked_at: datetime? and replaced_by: int? attributes to the RefreshToken class if desired.
  - On reuse detection, revoke the parent Session — document as a note on RefreshToken.

15 — Examples of short invariants/notes to attach to diagram
- AuthTicket: "if intent == REGISTER => user_id == NULL; else user_id != NULL".
- Session: "session.uuid is JTI; unique index; revocation checks use session.status".
- RefreshToken: "store token_hash only; revoked tokens must set revoked_at; replaced_by points to next token record".

16 — Common mistakes to avoid
- Mistaking aggregation/composition for enforcement: these are diagram semantics only; actual DB constraints and application logic must implement lifecycle rules.
- Omitting multiplicities or showing them only on one end — leads to ambiguity.
- Using composition when parts have meaningful independent lifecycle or need audit/history.

17 — Quick checklist for reviewing your auth class diagram
- Are multiplicities shown on both ends for every relation? (Yes → clearer)
- Are optional/nullable relationships clearly annotated? (Yes → good)
- Are domain invariants written as notes? (Yes → reduces ambiguity)
- Are lifecycle expectations (cascade deletes, orphan handling) documented? (Yes → implementers know requirements)
- Are enums and sensitive fields (hashed tokens) clearly labeled? (Yes → security-aware design)
- Are aggregation/composition glyphs used intentionally and sparingly? (Use only if you mean it)

18 — Short examples (ready-to-copy)
- Association with multiplicities:
  - [1] user.id ---- session.user_id [0..*]
- Aggregation example (visual hint): Session ⟶◊ RefreshToken
  - Annotate in text: "Session aggregates RefreshTokens (weak ownership)."

19 — Next steps and usage
- Add multiplicity labels to your draw.io diagram at both ends of each association. Use notes for invariants and security constraints. Use aggregation hollow diamond for Session→RefreshToken if you want to communicate grouping.
- Enforce rules in code and DB: nullability, FK constraints, unique indices (session.uuid), cascades (if any), hashed storage for tokens.

If you want, I can:
- Generate a short corrected draw.io XML snippet to add multiplicity labels and note boxes for your diagram, or
- Produce a one-page printable cheat sheet (PNG or SVG) with the symbols and their meanings tailored to your auth model.

Which of those would you prefer next?
