---
name: prd
description: Generate a Product Requirements Document (PRD) from a product idea. Use when asked to create a PRD, document product requirements, or start a new product. Invoked as "/prd <product description>".
metadata:
  author: custom
  version: "1.0.0"
  argument-hint: <product-description>
---

# Product Requirements Document Generator

Generate comprehensive Product Requirements Documents following industry best practices. This skill gathers information about a product idea through structured questions and produces a well-organized PRD.

## Overview

When invoked with `/prd <product description>`, this skill:
1. Analyzes the initial product description
2. Identifies gaps in the information needed for a complete PRD
3. Asks up to 10 targeted follow-up questions to fill those gaps
4. Generates a comprehensive PRD document at `dev-docs/prd.md`

## Input Format

```
/prd <product description>
```

The product description can be a brief idea, a detailed concept, or anything in between. The skill will adapt its questions based on what information is provided.

## The Process

### Step 1: Analyze Initial Input

Parse the product description to identify:
- **Provided information**: What details are already clear
- **Missing information**: What gaps need to be filled
- **Ambiguities**: What needs clarification

Map the input against the PRD framework sections to determine what questions to ask.

### Step 2: Ask Follow-up Questions

Use the AskUserQuestion tool to gather missing information. Ask **up to 10 questions** to complete the picture. Questions should be:

- **Targeted**: Address specific gaps in the PRD
- **Prioritized**: Most critical information first
- **Clear**: Easy to understand and answer
- **Actionable**: Answers directly inform the PRD

**Question Categories (prioritized):**

| Priority | Category | Purpose |
|----------|----------|---------|
| 1 | Problem & Users | Who has this problem? How painful is it? |
| 2 | Goals & Success | What does success look like? How to measure? |
| 3 | Core Features | What are the must-have capabilities? |
| 4 | User Experience | How will users interact with the product? |
| 5 | Scope & Constraints | What's in/out? What limitations exist? |
| 6 | Technical Context | Platform, integrations, technical requirements? |
| 7 | Business Context | Monetization, competition, go-to-market? |
| 8 | Risks & Dependencies | What could go wrong? What do we depend on? |

**Question Selection Logic:**

```
1. Review initial input for each PRD section
2. Identify sections with insufficient information
3. Prioritize questions by impact on PRD quality
4. Group related questions when possible (max 4 options per question)
5. Skip questions where reasonable defaults exist
6. Stop when you have enough for a solid PRD (don't force 10 questions)
```

**Example Question Patterns:**

```
Problem & Users:
- "Who is the primary target user for this product?"
- "What problem does this solve and how do users currently handle it?"

Goals & Success:
- "What would make this product successful? Any specific metrics?"
- "What is the primary goal users should accomplish?"

Core Features:
- "What are the 3-5 must-have features for the initial version?"
- "Are there features explicitly NOT needed for v1?"

User Experience:
- "What platforms should this support (web, mobile, desktop)?"
- "Should this integrate with any existing tools or services?"

Scope & Constraints:
- "What's the expected scale (users, data volume)?"
- "Are there any regulatory or compliance requirements?"

Technical Context:
- "Are there preferred technologies or existing systems to integrate with?"
- "Any performance requirements (load times, response times)?"

Business Context:
- "Is this B2B, B2C, or internal tooling?"
- "How will this be monetized (if applicable)?"
```

### Step 3: Generate the PRD

After gathering information, create a comprehensive PRD at `dev-docs/prd.md` with the following structure:

```markdown
# Product Requirements Document: [Product Name]

> Generated: [Date]
> Status: Draft
> Version: 1.0

## Executive Summary

[2-3 sentence overview of the product, its purpose, and primary value proposition]

---

## 1. Problem Statement

### 1.1 Background
[Context and background of the problem space]

### 1.2 Problem Definition
[Clear articulation of the problem being solved]

### 1.3 Current Solutions
[How users currently solve this problem, pain points with existing solutions]

---

## 2. Target Users

### 2.1 Primary Users
[Description of the main user persona(s)]

### 2.2 Secondary Users
[Other stakeholders or user types, if applicable]

### 2.3 User Personas

#### Persona 1: [Name]
- **Role**: [Job title or role]
- **Goals**: [What they want to achieve]
- **Pain Points**: [Current frustrations]
- **Tech Savviness**: [Low/Medium/High]

[Additional personas as needed]

---

## 3. Goals & Objectives

### 3.1 Product Vision
[Long-term vision for the product]

### 3.2 Product Goals
[Specific, measurable goals for this version]

### 3.3 Success Metrics (KPIs)

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| [Metric 1] | [Target value] | [How to measure] |
| [Metric 2] | [Target value] | [How to measure] |

### 3.4 Non-Goals
[What this product explicitly will NOT do]

---

## 4. User Stories & Use Cases

### 4.1 User Stories

| ID | As a... | I want to... | So that... | Priority |
|----|---------|--------------|------------|----------|
| US-001 | [user type] | [action] | [benefit] | [P0/P1/P2] |

### 4.2 Key Use Cases

#### UC-001: [Use Case Name]
- **Actor**: [User type]
- **Precondition**: [What must be true before]
- **Main Flow**:
  1. [Step 1]
  2. [Step 2]
  3. [Step 3]
- **Postcondition**: [What is true after]
- **Exceptions**: [What could go wrong]

---

## 5. Features & Requirements

### 5.1 Feature Overview

| Feature | Description | Priority | Status |
|---------|-------------|----------|--------|
| [Feature 1] | [Brief description] | P0 | Planned |

### 5.2 Functional Requirements

#### FR-001: [Requirement Name]
- **Description**: [Detailed description]
- **Acceptance Criteria**:
  - [ ] [Criterion 1]
  - [ ] [Criterion 2]
- **Dependencies**: [Any dependencies]

[Additional requirements...]

### 5.3 Non-Functional Requirements

#### Performance
- [Performance requirement 1]
- [Performance requirement 2]

#### Security
- [Security requirement 1]
- [Security requirement 2]

#### Accessibility
- [Accessibility requirement 1]

#### Scalability
- [Scalability requirement 1]

---

## 6. User Experience

### 6.1 User Flows

#### Flow 1: [Flow Name]
[Start] -> [Step 1] -> [Step 2] -> [End State]

### 6.2 Key Screens/Views
[Description of main UI components or screens]

### 6.3 Design Principles
[Guiding principles for the UX/UI design]

---

## 7. Technical Considerations

### 7.1 Platform & Technology
- **Platform**: [Web/Mobile/Desktop/etc.]
- **Technology Stack**: [If predetermined]

### 7.2 Integrations
[External systems or APIs to integrate with]

### 7.3 Data Requirements
[Data storage, processing, privacy considerations]

### 7.4 Technical Constraints
[Technical limitations or requirements]

---

## 8. Scope & Boundaries

### 8.1 In Scope (v1)
- [Feature/capability 1]
- [Feature/capability 2]

### 8.2 Out of Scope (v1)
- [Feature/capability to defer]
- [Feature/capability to defer]

### 8.3 Future Considerations (v2+)
- [Potential future enhancement 1]
- [Potential future enhancement 2]

---

## 9. Dependencies & Risks

### 9.1 Dependencies

| Dependency | Type | Owner | Status |
|------------|------|-------|--------|
| [Dependency 1] | [Internal/External] | [Team/Person] | [Status] |

### 9.2 Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk 1] | [H/M/L] | [H/M/L] | [Mitigation strategy] |

### 9.3 Assumptions
- [Assumption 1]
- [Assumption 2]

---

## 10. Open Questions

[Any remaining questions or decisions to be made]

- [ ] [Question 1]
- [ ] [Question 2]

---

## Appendix

### A. Glossary
[Define any domain-specific terms]

### B. References
[Links to research, competitive analysis, etc.]

### C. Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | [Date] | [Author] | Initial draft |
```

### Step 4: Review and Refine

After generating the initial PRD:

1. **Completeness Check**: Ensure all sections have meaningful content
2. **Consistency Check**: Verify terminology and priorities are consistent
3. **Clarity Check**: Ensure requirements are specific and testable
4. **Gap Identification**: Note any remaining open questions

## Question Strategy

### Adaptive Questioning

The number and type of questions should adapt to the initial input:

**Minimal Input** (just an idea):
- Ask 8-10 questions covering all major areas
- Start with problem/users, end with technical details

**Moderate Input** (idea + some context):
- Ask 5-7 questions focusing on gaps
- Skip areas that are well-defined

**Detailed Input** (comprehensive description):
- Ask 2-4 clarifying questions
- Focus on ambiguities and edge cases

### Question Batching

Use the AskUserQuestion tool efficiently:
- Group related questions when possible
- Provide multiple-choice options when appropriate
- Use "Other" option for open-ended responses
- Batch up to 4 questions per tool call

### Skip Conditions

Don't ask about:
- Information clearly stated in the input
- Details that can use reasonable defaults
- Implementation specifics (save for TRD)
- Exact timelines or deadlines

## PRD Best Practices Applied

This skill follows industry-standard PRD best practices:

1. **User-Centric**: Focus on user problems and outcomes, not solutions
2. **Measurable**: Include specific, measurable success criteria
3. **Prioritized**: Use P0/P1/P2 priority levels consistently
4. **Testable**: Write requirements with clear acceptance criteria
5. **Scoped**: Clearly define what's in and out of scope
6. **Risk-Aware**: Identify dependencies and risks early
7. **Iterative**: Design for versioned development (v1, v2+)
8. **Accessible**: Write for all stakeholders, not just engineers

## Output

- **File**: `dev-docs/prd.md`
- **Format**: Markdown with clear section hierarchy
- **Length**: Comprehensive but not excessive (aim for clarity)

## Example Session

```
User: /prd A mobile app that helps people track their daily water intake

Assistant: I will help you create a PRD for a water intake tracking app. Let me ask a few questions to understand your vision better.

[Uses AskUserQuestion tool with questions about:]
- Target users (health-conscious adults, athletes, people with medical conditions)
- Platform preference (iOS, Android, both)
- Key features (reminders, goal setting, history tracking)
- Integration needs (Apple Health, Google Fit, wearables)

User: [Answers questions...]

Assistant: Based on your answers, I will now generate a comprehensive PRD.

[Writes dev-docs/prd.md with all sections filled in based on the gathered information]

Assistant: I have created the PRD at dev-docs/prd.md. The document includes:
- Executive summary of the water tracking app
- Problem statement about dehydration
- Target user personas
- 12 user stories prioritized P0-P2
- Feature requirements with acceptance criteria
- Technical considerations for mobile development
- Success metrics including DAU and retention targets
```

## Success Criteria

A successful PRD generation:
- Asks relevant follow-up questions (up to 10)
- Creates a complete PRD at `dev-docs/prd.md`
- Covers all 10 main sections
- Uses consistent priority levels (P0/P1/P2)
- Includes measurable success metrics
- Clearly defines scope boundaries
- Documents assumptions and risks

## Notes

- The skill adapts question depth based on initial input detail
- Questions are batched efficiently (up to 4 per tool call)
- The PRD template can be customized for specific domains
- Open questions section captures items needing future decisions
- Revision history enables PRD evolution tracking
