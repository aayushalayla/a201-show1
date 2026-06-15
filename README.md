# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

My domain is an unofficial guide to CS side projects for college students building portfolios for internships and entry-level software roles. Official career resources often give broad advice like “build projects” or “make a GitHub,” but they rarely explain what actually makes a project seem impressive, generic, over-AI-generated, or useful in hiring.

This knowledge is valuable because the practical advice is scattered across Reddit threads, GitHub discussions, career guides, recruiter-facing articles, and personal blogs. My system brings those sources together so students can ask specific questions about project quality, GitHub presentation, class projects, AI-assisted work, and recruiter behavior.

---

## Document Sources

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | Building a Portfolio That Shows Your Skills, Not Just AI | Blog / AI-era portfolio advice | https://blog.vibecoder.me/building-a-portfolio-that-shows-your-skills-not-just-ai |
| 2 | Using GitHub for Portfolios | GitHub Community discussion | https://github.com/orgs/community/discussions/169760 |
| 3 | Fine-Tuning GitHub for Portfolios | Career-guide article | https://flatironschool.com/blog/github-profile-and-git-practices-for-job-seekers/ |
| 4 | Range of Projects a Portfolio Can Include | Software engineer portfolio guide | https://arc.dev/talent-blog/software-engineer-portfolio/ |
| 5 | Junior Developer Portfolio Best Practices | Developer advice article | https://dev.to/jtrevdev/junior-developer-portfolio-best-practices-4bj2 |
| 6 | What Projects Got You Hired? | Reddit thread / student and developer discussion | https://www.reddit.com/r/learnprogramming/comments/skov60/what_are_the_projects_that_got_you_hired/ |
| 7 | How and When to Include Projects on Your Resume | Career-center article | https://career.pennwest.edu/blog/2022/08/10/how-and-when-to-include-projects-on-your-resume-plus-examples/ |
| 8 | Do Recruiters Look Through GitHub Projects? | Reddit thread / student and hiring discussion | https://www.reddit.com/r/csMajors/comments/ol42hl/do_recruiters_actually_go_through_your_github/ |
| 9 | Building a Coding Portfolio | Coding portfolio guide | https://www.educative.io/blog/building-a-coding-portfolio |
| 10 | How Hiring Evaluates Developer Portfolios | Hiring-side article | https://medium.com/predict/how-to-evaluate-developer-portfolios-before-hiring-af2908025a09 |
---
## Chunking Strategy

Initial chunk inspection showed that the chunks were mostly readable and contained relevant portfolio advice, but some chunks began mid-word because the overlap was character-based. I fixed this by adjusting the overlap to start at word boundaries and by adding title/URL metadata to each source file. I also adjusted Reddit/forum chunking so separate comments were less likely to be merged into one chunk.

**Chunk size:**  
700–900 characters.

**Overlap:**  
100 characters.

**Why these choices fit your documents:**  
My documents mix short Reddit/forum comments, bullet-point advice, and longer explanatory paragraphs from career guides. A 700–900 character chunk is large enough to preserve a complete piece of advice, such as why tutorial projects can look generic or how to make a GitHub repository more reviewable, but small enough to keep unrelated topics separate. The 100-character overlap helps preserve context when advice spans two adjacent paragraphs.

Before chunking, I manually copied each source into a `.txt` file, removed obvious navigation text and unrelated page clutter, and included source metadata at the top of each file. The ingestion script cleaned remaining HTML artifacts, normalized whitespace, loaded title/URL metadata, and saved the final chunks to `chunks.json`.

**Final chunk count:**  
169 chunks across 10 documents.

---

## Embedding Model

**Model used:**  
I used `all-MiniLM-L6-v2` through the `sentence-transformers` library.

I chose this model because it runs locally and works well for semantic search over short-to-medium text chunks. My corpus includes Reddit comments, GitHub discussions, career advice articles, and hiring-side portfolio advice, so I needed an embedding model that could retrieve conceptually similar chunks even when the wording differed across sources.

**Production tradeoff reflection:**  
If I were deploying this system for real users and cost was not a constraint, I would compare `all-MiniLM-L6-v2` against stronger embedding models with better performance on informal language, technical hiring language, and longer context. I would also consider latency, cost, multilingual support, local vs. API-hosted deployment, and whether the model handles mixed-source corpora well. A stronger model might improve retrieval for nuanced questions like “what makes a project generic,” where the answer may be phrased indirectly across multiple sources.
---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**

**How source attribution is surfaced in the response:**

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**

**What the system returned:**

**Root cause (tied to a specific pipeline stage):**

**What you would change to fix it:**

---

## Spec Reflection

**One way the spec helped you during implementation:**  
The spec helped me avoid building the generation layer before checking retrieval. Because planning.md forced me to define the domain, source list, chunk size, overlap, embedding model, and evaluation questions first, I had a concrete target for the ingestion and retrieval code instead of writing a generic RAG pipeline. It also made chunk inspection easier because I knew what kinds of questions each chunk should be able to answer.

**One way your implementation diverged from the spec, and why:**  
The main implementation change was in the chunking stage. My original plan used paragraph-aware chunking with character overlap, but early inspection showed that some chunks began mid-word or merged separate Reddit comments. I adjusted the code so overlap starts closer to word boundaries and Reddit-style comment separators act as hard boundaries. This made the chunks more readable and better suited for retrieval.
---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

## AI Usage

**Instance 1**

- *What I gave the AI:*  
  I gave the AI my Documents section, Chunking Strategy section, and Architecture diagram from planning.md. I also described that my documents were local `.txt` files copied from articles, Reddit threads, GitHub discussions, and career guides.

- *What it produced:*  
  It produced a Python ingestion script with functions for loading documents, cleaning text, parsing title/URL metadata, splitting documents into chunks, and saving the results to `chunks.json`.

- *What I changed or overrode:*  
  I adjusted the chunking logic after inspecting sample chunks. Some chunks started mid-word or merged unrelated Reddit comments, so I added word-boundary overlap handling and treated Reddit/forum comment separators as hard chunk boundaries.

**Instance 2**

- *What I gave the AI:*  
  I gave the AI my Retrieval Approach section, including the embedding model `all-MiniLM-L6-v2`, the vector store ChromaDB, and the top-k value of 5.

- *What it produced:*  
  It produced a retrieval script that loads `chunks.json`, embeds the chunk text with `sentence-transformers`, stores embeddings and metadata in ChromaDB, and retrieves the top 5 chunks for a query with distance scores.

- *What I changed or overrode:*  
  I debugged the local Python environment before retrieval worked. The first virtual environment used Python 3.14, which caused dependency issues with ChromaDB and `onnxruntime`, so I recreated the environment with Python 3.11. I also pinned ChromaDB more strictly to reduce pip dependency backtracking.