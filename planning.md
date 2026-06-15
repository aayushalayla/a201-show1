# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->
My domain is an unofficial guide to CS side projects for college students building portfolios for internships and entry-level software roles. This knowledge is valuable because official career resources often give generic advice like “build projects” or “make a GitHub,” while the more practical advice about what seems impressive, generic, over-AI-generated, or actually useful to recruiters is scattered across Reddit threads, GitHub discussions, personal blogs, and career guides.
---

## Documents
| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | Building a Portfolio That Shows Your Skills, Not Just AI | AI-era advice on why simple polished apps are less convincing now, and why students need to show decisions, tradeoffs, debugging, and process. | https://blog.vibecoder.me/building-a-portfolio-that-shows-your-skills-not-just-ai |
| 2 | Using GitHub for Portfolios | GitHub Community discussion about whether employers inspect GitHub, what public projects to show, and why strong READMEs matter. | https://github.com/orgs/community/discussions/169760 |
| 3 | Fine-Tuning GitHub for Portfolios | Career-guide advice on cleaning up a GitHub profile, making repositories presentable, and using GitHub as job-search evidence. | https://flatironschool.com/blog/github-profile-and-git-practices-for-job-seekers/ |
| 4 | Range of Projects a Portfolio Can Include | Broad software engineering portfolio guide showing common portfolio sections, project categories, and mainstream expectations. | https://arc.dev/talent-blog/software-engineer-portfolio/ |
| 5 | Junior Developer Portfolio Best Practices | Advice on portfolio structure, quality over quantity, GitHub Pages, READMEs, project descriptions, and mistakes junior developers should avoid. | https://dev.to/jtrevdev/junior-developer-portfolio-best-practices-4bj2 |
| 6 | What Projects Got You Hired? | Reddit discussion where programmers describe which projects helped them get hired, including concerns about boring beginner projects like calculators or BMI apps. | https://www.reddit.com/r/learnprogramming/comments/skov60/what_are_the_projects_that_got_you_hired/ |
| 7 | How and When to Include Projects on Your Resume | Career-center advice on when to include class projects, side projects, and academic projects on a resume, plus how to describe them. | https://career.pennwest.edu/blog/2022/08/10/how-and-when-to-include-projects-on-your-resume-plus-examples/ |
| 8 | Do Recruiters Look Through GitHub Projects? | Student/recruiter reality-check thread about whether recruiters actually inspect GitHub projects or mostly rely on resumes. | https://www.reddit.com/r/csMajors/comments/ol42hl/do_recruiters_actually_go_through_your_github/ |
| 9 | Building a Coding Portfolio | Interviewer-facing guide on project types, documentation, source-code access, live demos, and presenting a coding portfolio. | https://www.educative.io/blog/building-a-coding-portfolio |
| 10 | How Hiring Evaluates Developer Portfolios | Hiring-side perspective on what reviewers look for when judging developer portfolios before interviews. | https://medium.com/predict/how-to-evaluate-developer-portfolios-before-hiring-af2908025a09 |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->
**Chunk size:** 700–900 characters

**Overlap:** 100 characters

**Reasoning:** My documents mix short forum-style comments, bullet-point advice, and longer explanatory paragraphs from career guides. I will preserve paragraph or comment boundaries when possible, then combine nearby text until each chunk is around 700–900 characters. This size is large enough to keep a complete piece of advice together, such as why a project looks generic or how to present it on GitHub, but small enough that retrieval can still distinguish between subtopics like README quality, class projects, AI-generated projects, recruiter behavior, and resume presentation.

The 100-character overlap helps prevent meaning loss when a point spans two adjacent chunks, such as a warning about generic AI-assisted projects followed by advice on how to make the project more original.

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

## Retrieval Approach

**Embedding model:**  
I will use `all-MiniLM-L6-v2` through the `sentence-transformers` library. 
This model runs locally, does not require an API key, and is a good default for semantic search over short-to-medium text chunks like Reddit comments, GitHub discussions, and portfolio advice articles.

**Top-k:**  
I will retrieve the top 5 most relevant chunks for each user query.

**Production tradeoff reflection:**  
For this project, `all-MiniLM-L6-v2` is a practical choice because it is easy to run locally. If I were deploying this for real users and cost was not a constraint, I would compare it with stronger embedding models that perform better on informal career advice, technical language, and longer documents. I would also weigh context length, retrieval accuracy, latency, cost, and whether the model handles mixed writing styles well, since my corpus includes polished articles, Reddit-style comments, GitHub discussions, and hiring advice.

Retrieving 5 chunks gives the generation model enough context to answer nuanced questions without flooding it with loosely related material. If retrieval results are too narrow or miss important context, I may increase top-k to 6 or 7. If answers become vague or pulled in too many directions, I will lower top-k to 3 or 4.

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

## Evaluation Plan

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | What makes a CS portfolio project look generic or unimpressive? | Generic projects are usually tutorial-style apps, common clones, or simple projects with no original problem, user, technical decision-making, documentation, or evidence that the student understood what they built. |
| 2 | How can a student make an AI-assisted project show real skill instead of looking AI-generated? | The project should show process. Including problem choice, design decisions, debugging, tradeoffs, iteration, documentation, and what they personally understood or changed beyond the AI-generated baseline. |
| 3 | Do recruiters or hiring teams actually look through GitHub projects? | The expected answer should be nuanced based on the given articles: recruiters may not deeply inspect every GitHub link, but a clean GitHub can still matter for technical reviewers, hiring managers, interviews, or companies that value open-source/project evidence. (8,6)|
| 4 | Should college students include class projects on a CS resume or portfolio? | Yes, if the class project is relevant, polished, clearly explained, and shows the student’s own contribution. It is weaker if it looks like an unchanged assignment, has no documentation, or is less relevant than stronger side/work projects. |
| 5 | What should a strong project entry include on a resume, GitHub, or portfolio site? | It should include the problem the project solves, the technologies used, what the student personally built, the impact or result, a clean README, and ideally links to source code, screenshots, or a live demo.|

---

## Anticipated Challenges

1. Some advice may depend on context across multiple paragraphs, such as a warning about generic AI-assisted projects followed by advice on how to make them more original. If chunking splits the warning from the solution, the retrieved chunk may only show half the point and not provide a satisfying answer.

2. Portfolio advice often repeats similar words like “project,” “GitHub,” “resume,” and “skills." This may mean semantic search retrieves chunks that mention the same keywords but answer a different question. 
---

## Architecture

Document Ingestion
(local .txt files from articles, Reddit threads, GitHub discussions, and career guides)
        ↓
Chunking
(custom Python chunk_text function; 700–900 characters, 100–150 character overlap)
        ↓
Embedding + Vector Store
(sentence-transformers all-MiniLM-L6-v2 → ChromaDB)
        ↓
Retrieval
(semantic similarity search; retrieve top 5 chunks with source title + URL metadata)
        ↓
Generation
(Groq llama-3.3-70b-versatile; answer only from retrieved chunks and cite sources)
---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

## AI Tool Plan

**Milestone 3 — Ingestion and chunking:**  
I plan to use Claude or ChatGPT to help implement the document ingestion and chunking script. I will give the AI my Documents section, Chunking Strategy section, and Architecture diagram. I will ask it to write Python code that loads `.txt` files from the `documents/` folder, cleans obvious formatting noise, preserves source metadata, and splits the text into 700–900 character chunks with 100-character overlap.

I expect the AI to produce functions such as `load_documents()`, `clean_text()`, and `chunk_text()`. I will verify the output by printing at least 5 sample chunks, checking that each chunk is readable and self-contained, and confirming that every chunk includes the correct source title, URL, and chunk position.

**Milestone 4 — Embedding and retrieval:**  
I plan to use ChatGPT or Copilot to help implement the embedding and retrieval layer. I will give the AI my Retrieval Approach section and Architecture diagram, including the required embedding model, vector store, and top-k value. I will ask it to write code that embeds chunks with `sentence-transformers` using `all-MiniLM-L6-v2`, stores them in ChromaDB with metadata, and retrieves the top 5 chunks for a user query.

I expect the AI to produce functions such as `build_vector_store()` and `retrieve(query, top_k=5)`. I will verify the output by running at least 3 evaluation questions before adding generation. For each query, I will inspect the retrieved chunks and distance scores to make sure the results actually answer the question rather than just matching broad words like “project,” “portfolio,” or “GitHub.”

**Milestone 5 — Generation and interface:**  
I plan to use ChatGPT or Copilot to help wire retrieval into a grounded response generator and a simple query interface. I will give the AI my Evaluation Plan, Retrieval Approach, and grounding requirement: the model must answer only from retrieved chunks and cite sources. I will ask it to create an `ask(question)` function that retrieves relevant chunks, passes them to Groq’s `llama-3.3-70b-versatile`, and returns an answer plus source list.

I expect the AI to produce the generation prompt, Groq API call, and a simple Gradio or command-line interface. I will verify the output by asking both in-scope and out-of-scope questions. For in-scope questions, the answer must cite retrieved sources. For out-of-scope questions, the system should say it does not have enough information instead of guessing from general knowledge.