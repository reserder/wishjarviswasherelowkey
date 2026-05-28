# AEGIS Master Architecture: Orbit OS Blueprint

## 1. Executive Architecture Overview
AEGIS (AI Executive OS) is a production-grade, local-first, modular operating system designed to serve as a high-leverage personal and company control center. Anchored by the main executive assistant, **Orbit**, AEGIS coordinates a hierarchical swarm of specialized sub-agents. It operates natively via the Model Context Protocol (MCP) to seamlessly integrate tools, web automation, and local file systems, prioritizing retrieval-augmented generation (RAG) and robust memory over zero-shot hallucinations. Engineered initially for an Apple MacBook Pro M2 Pro (16GB RAM), AEGIS scales cleanly to secure cloud deployments without architectural rewrites.

## 2. Core Design Principles
*   **Local-First & Privacy-First:** Sensitive data and daily execution remain on-device. Cloud escalation is strictly opt-in for overflow or premium reasoning tasks.
*   **Browser-First Interaction:** The terminal is reserved for DevOps and initial setup. Daily operations, monitoring, and configurations occur entirely within a polished web UI.
*   **Multi-Agent Hierarchy:** A supervisor (Orbit) routes intent to specialized agents, preventing context bloat and ensuring deep expertise per domain.
*   **MCP-Native Extensibility:** Tooling is decoupled via the Model Context Protocol, allowing safe, sandboxed, and dynamically configurable capabilities.
*   **Retrieval Before Generation:** Answers are grounded in a rich "Second Brain" via Qdrant and graph relationships to minimize hallucinations.
*   **Guardrailed Autonomy:** High-risk actions (e.g., GitHub commits, sending emails) require explicit human approval via Sentinel.
*   **Modular Evolution:** The architecture supports seamless migration from a local Docker Compose stack to a distributed, domain-mapped server environment.

## 3. Full System Diagram (Text)

```text
+-----------------------------------------------------------------------------------+
|                                 USER BROWSER                                      |
|  [ Open WebUI / Future Next.js App ]  <-->  [ Domain Front Door (Caddy/Traefik) ] |
+-----------------------------------------------------------------------------------+
                                  | (REST / WebSocket / SSE)
+-----------------------------------------------------------------------------------+
|                               AEGIS BACKEND (FastAPI / LangGraph)                 |
|                                                                                   |
|  +------------------+     +----------------------------------------------------+  |
|  | ORBIT (Main)     | --> | SPECIALISTS: Mercury, Atlas, Forge, Echo,          |  |
|  | Supervisor Agent |     | Muse, Operator                                     |  |
|  +------------------+     +----------------------------------------------------+  |
|          |                                     |                                  |
|  [ Sentinel (Security & Approval Gates) ] <----+                                  |
|          |                                                                        |
|  [ LiteLLM Router ]                                                               |
+-----------------------------------------------------------------------------------+
       |                  |                           |                      |
+-------------+    +---------------+        +-------------------+  +------------------+
| LOCAL MODEL |    | MCP REGISTRY  |        | MEMORY & RAG      |  | AUTOMATION (e.g. |
| (Ollama)    |    | & TOOL HOST   |        | (Qdrant/Postgres) |  | Windmill)        |
| - gemma4    |    | - GitHub      |        | - Vector DB       |  | - Cron Jobs      |
| - deepseek  |    | - Open Design |        | - Episodic Mem    |  | - Webhooks       |
| - mistral   |    | - Local FS    |        | - Second Brain    |  |                  |
+-------------+    +---------------+        +-------------------+  +------------------+
       |
+-------------+
| CLOUD API   |
| - qwen3.5   |
+-------------+
```

## 4. Component-by-Component Architecture

*   **Frontend Layer:** Starts with Open WebUI connected to the backend API. Transitions in Phase 5 to a custom React/Next.js application providing bespoke dashboards (Memory, Knowledge, MCP configs).
*   **API & Orchestration (Backend):** Built on Python (FastAPI + LangGraph). Manages state, handles routing logic, streams LLM responses, and orchestrates the agent swarm.
*   **Model Router (LiteLLM):** Provides a unified OpenAI-compatible endpoint. Handles fallbacks, load balancing, and cost tracking, abstracting away the underlying local Ollama or cloud models.
*   **Memory & RAG Subsystem:** Uses Qdrant for vector storage and PostgreSQL (or SQLite locally) for relational metadata and episodic memory. Incorporates LightRAG for graph-based relationship mapping.
*   **MCP Integration Layer:** A dedicated service (or internal module) that spins up stdio/HTTP MCP servers and manages tool execution scopes.
*   **Automation Engine:** Integrates with local Windmill (or similar lightweight task runner) to execute scheduled workflows like the "morning brief" or nightly document indexing.

## 5. Agent Hierarchy

### Main Assistant
*   **Orbit (Executive OS):** The primary interface. Understands user intent, maintains session context, routes tasks to specialists, and synthesizes final outputs. Generates the daily briefing and triages inbox/calendar.

### Specialist Agents
*   **Mercury (Research):** Deep analysis, web scraping, document synthesis. Uses `deepseek-r1:7b`. High memory access, read-only tools.
*   **Atlas (Business/Ops):** Manages Amora OS, financial tracking, SOPs. Uses `gemma4:e4b`. Needs Sentinel approval for writing data.
*   **Forge (Coding/Infra):** Connects to GitHub, reviews PRs, debugs architecture. Uses `deepseek-r1:7b`. Full MCP file/git access. Approvals needed for commits.
*   **Echo (Memory):** The librarian. Curates, edits, and retrieves long-term and episodic memory. Uses `mistral:latest` (fast, lightweight). No external tools.
*   **Muse (Music/Brand):** Artist persona, rollout strategy, content generation. Uses `gemma4:e4b`. Persona-safe mode enforced.
*   **Sentinel (Security):** Not conversational; a programmatic/LLM hybrid gatekeeper that intercepts sensitive tool calls, evaluates risk, and prompts the user for approval.
*   **Operator (Automation):** Interacts with Windmill/cron to schedule jobs and execute background workflows.

## 6. Model Routing Strategy

Designed for M2 Pro (16GB RAM) constraints:
*   **`gemma4:e4b` (Primary):** Orbit, Atlas, Muse. The daily driver. Fast, low memory footprint, capable of standard conversational and orchestration tasks.
*   **`deepseek-r1:7b` (Reasoning):** Forge, Mercury. Loaded on-demand (swapping out gemma if necessary) for complex coding, deep research, or multi-step logic.
*   **`mistral:latest` (Fallback/Utility):** Echo, background tasks (summarization, memory compression). Highly efficient for rapid text processing.
*   **`qwen3.5:397b-cloud` (Escalation):** Used strictly for tasks explicitly flagged by the user as requiring "maximum intelligence" or when local models fail verification checks >3 times.

**Routing Logic:**
*   *Low-Latency (UI chats):* `gemma4`
*   *Heavy Code/Logic:* Route to `deepseek`.
*   *Background Ingestion:* `mistral` batches.
*   *Memory Constraints:* The system ensures only one heavy model is loaded in Ollama at a time to stay under the ~12GB VRAM limit of the 16GB unified memory.

## 7. Frontend Product Architecture

The AI OS browser interface (React/Next.js or customized Open WebUI):

**Pages:**
1.  **Home (Orbit Dashboard):** High-level daily brief, pending approvals, quick chat.
2.  **Assistants:** Directory of agents, their current statuses, and configuration.
3.  **Models:** LiteLLM UI integration to view loaded models, VRAM usage, and fallbacks.
4.  **Knowledge & Memory:** "Second Brain" explorer. View vectors, graph relationships, and edit/delete specific memories.
5.  **MCP Servers:** UI to add new MCP tools, view connection status, and configure per-agent access.
6.  **GitHub / Integrations:** Connect private repos, manage PATs, view recent PR summaries.
7.  **Automations:** View scheduled Windmill jobs (e.g., nightly syncs).
8.  **Approvals (Sentinel Queue):** Tinder-style swipe/click to approve or reject staged actions (e.g., "Forge wants to commit to main").

**UX Flows:**
*   *Adding MCP Server:* User inputs Docker image or local path in UI -> Backend tests connection -> Saves to DB -> Orbit updates its tool registry dynamically.
*   *Approving Risk:* Agent hits a gated tool -> Pauses execution -> Emits SSE to Frontend -> Approval Queue shows diff/intent -> User clicks "Approve" -> Execution resumes.

## 8. MCP Integration Architecture

The Model Context Protocol (MCP) is the sole mechanism for tool integration.

*   **Registry:** Backend maintains a DB of active MCP servers (HTTP mode for Dockerized tools, stdio for local scripts).
*   **Per-Agent Permissions:** Forge gets `mcp://github` and `mcp://localfs`. Orbit gets `mcp://calendar`.
*   **GitHub MCP:** Deployed as an isolated Docker container with injected PATs.
*   **Filesystem MCP:** Restricted via Docker volumes to specific directories (e.g., `~/aegis-workspace`), preventing access to `~/.ssh` or root.
*   **Security Risks & Mitigation:**
    *   *Prompt Injection via PR:* Malicious code in a repo could instruct Forge to exfiltrate secrets.
    *   *Mitigation:* MCP tools return data wrapped in `<untrusted>` tags. The LLM is prompted to never execute commands found within untrusted blocks. Sentinel blocks any outbound network requests not explicitly allowlisted.

## 9. Memory + RAG (Second Brain) Architecture

**Memory Types:**
1.  **Short-term:** Current session context window (managed by LangGraph).
2.  **Episodic:** Chronological log of significant interactions (stored in Postgres).
3.  **Semantic (Second Brain):** Facts, concepts, and relationships (stored in Qdrant + LightRAG).
4.  **Preference:** User instructions ("I prefer Python over JS") injected into the system prompt.

**Corpus Separation (Qdrant Collections):**
*   `personal_life_os`
*   `amora_business_ops`
*   `forge_codebase`
*   `muse_brand`

**Retrieval Pipeline:**
User Query -> Orbit extracts intent -> Query routed to Qdrant -> Metadata filtering (e.g., domain="amora") -> Top-K vectors retrieved -> Reranked via local cross-encoder -> Injected into agent context with source citations.
*Memory Editing:* Users can browse the memory UI and delete/edit nodes, which triggers a vector tombstone and re-indexing.

## 10. Security Architecture

Enterprise-grade security on a local-first system:
*   **RBAC:** Admin (full system access), Normal User (interaction only), Assistant (sandboxed execution).
*   **Secrets:** `.env` files are never read directly by LLMs. Secrets are injected into MCP containers at runtime.
*   **Approval Gates (Sentinel):** Hardcoded policies. Any tool tagged `requires_approval: true` suspends the LangGraph node until a human webhook is received.
*   **GitHub Boundaries:** Fine-grained PATs only. Separate PATs for Read-Only (indexing) vs Read-Write (Forge PRs). Branch protection enforced on GitHub's side.
*   **Making it Safe for Production:** Implement strict network isolation. The LLM container must have NO internet access except via authorized MCP proxies. Use Caddy with mTLS or strict OIDC for the frontend.

## 11. Deployment Architecture

### A. Local Development (M2 Pro 16GB)
Runs entirely in Docker Compose:
*   `host`: Ollama (utilizing Metal GPU).
*   `container_1`: Aegis Backend (FastAPI).
*   `container_2`: Open WebUI (port 3000).
*   `container_3`: Qdrant (port 6333).
*   `container_4`: LiteLLM Proxy.
*   `container_5+`: Ephemeral MCP servers.

### B. Future Server/VPS Deployment
*   **Reverse Proxy:** **Caddy** is strongly recommended over Traefik for this stack. It offers automatic HTTPS, simpler config (Caddyfile), and zero-friction subdomain routing.
*   Isolated VPC network. Data drives mounted as encrypted volumes.
*   Cloud LLMs accessed via secure LiteLLM proxy.

## 12. Folder Structure

```text
aegis-ai-os/
├── .env.example
├── docker-compose.yml
├── Makefile
├── frontend/                 # Phase 5: Custom Next.js UI
├── backend/                  # FastAPI + LangGraph orchestration
│   ├── api/                  # REST/SSE endpoints
│   ├── core/                 # Configs, security, Sentinel
│   ├── workflows/            # LangGraph state machines
│   └── database/             # Postgres/Qdrant clients
├── agents/                   # Agent definitions
│   ├── orbit.py
│   ├── specialists/          # mercury, atlas, forge, etc.
│   └── prompts/              # System prompt templates
├── memory/                   # Second Brain logic
│   ├── indexing/             # Ingestion pipelines
│   └── retrieval/            # RAG and reranking logic
├── mcp_servers/              # Local stdio MCP implementations
│   ├── local_fs/
│   └── automation/
├── configs/                  # LiteLLM, Agent routing YAMLs
├── infra/                    # Caddyfile, deployment scripts
├── tests/                    # Pytest suite
└── docs/                     # Architecture and SOPs
```

## 13. Config Examples

**1. LiteLLM Model Routing (`configs/litellm_config.yaml`)**
```yaml
model_list:
  - model_name: gemma-primary
    litellm_params:
      model: ollama/gemma4:e4b
      api_base: http://host.docker.internal:11434
  - model_name: deepseek-reasoner
    litellm_params:
      model: ollama/deepseek-r1:7b
      api_base: http://host.docker.internal:11434
  - model_name: cloud-escalation
    litellm_params:
      model: openai/qwen3.5:397b-cloud
      api_key: os.environ/QWEN_API_KEY
```

**2. MCP Registry Entry (Backend DB / Config)**
```json
{
  "server_name": "github_mcp",
  "type": "http",
  "url": "http://github-mcp:8080/mcp",
  "allowed_agents": ["forge"],
  "tools": {
    "read_repo": {"requires_approval": false},
    "create_pr": {"requires_approval": true}
  }
}
```

**3. Caddyfile (Reverse Proxy)**
```caddyfile
orbit.aegis.local {
    reverse_proxy frontend:3000
}

api.aegis.local {
    reverse_proxy backend:8000
}

models.aegis.local {
    reverse_proxy litellm:4000
}
```

## 14. Phased Roadmap

*   **Phase 0: Stabilize Local Stack.** (Current) Ensure Ollama, LiteLLM, and Open WebUI communicate flawlessly on the M2 Mac. Test memory limits.
*   **Phase 1: Working Browser Shell with Orbit.** Implement LangGraph backend. Connect Orbit agent to UI. Establish intent routing.
*   **Phase 2: Memory + Knowledge + RAG.** Deploy Qdrant. Build the Echo agent. Implement background document ingestion and vector search.
*   **Phase 3: MCP Integrations + GitHub.** Integrate MCP standard. Build Forge agent. Connect GitHub with read-only PATs first, then read-write with approvals.
*   **Phase 4: Automation and Approvals.** Implement Sentinel approval queue. Connect Windmill for scheduled morning briefs and agent cron jobs.
*   **Phase 5: Custom Branded AI OS Frontend.** Replace Open WebUI with a bespoke Next.js dashboard featuring Memory explorers, MCP config UI, and Tinder-style approval swiping.
*   **Phase 6: Voice / Wearables.** Expose secure WebSocket endpoints for mobile companion apps.

## 15. Top Risks and Mitigations

1.  **VRAM Exhaustion (16GB Limit):**
    *   *Risk:* Loading Deepseek + Gemma simultaneously crashes the Mac.
    *   *Mitigation:* LiteLLM / Backend logic must explicitly unload models via Ollama API before switching, or strictly limit concurrent agent execution.
2.  **Context Bloat:**
    *   *Risk:* Passing too much RAG data crashes local models.
    *   *Mitigation:* Context compression agent (mistral) summarizes RAG output before feeding it to Orbit. Strict token limits enforced.
3.  **Prompt Injection from GitHub:**
    *   *Risk:* Summarizing a malicious PR compromises Forge.
    *   *Mitigation:* Sentinel parses Forge's output for unauthorized tool requests. Strict network isolation for the LLM.

## 16. Recommended Immediate Next Actions

1.  **Setup Directory Structure:** Scaffold the folders as outlined in Section 12.
2.  **Verify Hardware Constraints:** Write a script to load `gemma4:e4b` and `deepseek-r1:7b` sequentially in Ollama to verify transition times and memory spikes on the M2 Pro.
3.  **Implement LiteLLM Router:** Set up `configs/litellm_config.yaml` and run the proxy to abstract Ollama from the upcoming backend.
4.  **Draft the LangGraph Supervisor:** Begin writing `backend/workflows/supervisor.py` to establish the Orbit routing logic.
