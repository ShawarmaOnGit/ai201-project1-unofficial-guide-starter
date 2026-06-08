# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

My domain is student advice about studying Computer Science at the University at Buffalo.

This is useful because official UB pages show course requirements, but doesn't show what students actually think about the classes, professors, workload, transfer experience, or any paths. Instead, this informatio is available on Reddit threads, so my system will help answer questions using those student comments.

---

## Documents

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | How is Computer Science at UBuffalo? | General UB CS student opinions | https://www.reddit.com/r/UBreddit/comments/10xaxf7/how_is_computer_science_at_ubuffalo/ |
| 2 | CS/AI/ML track advice | Advice about the CS/AI/ML path | https://www.reddit.com/r/UBreddit/comments/17wuvab/how_is_csaiml_track_for_someone_whos_only_getting/ |
| 3 | How to CSE115? | Advice for CSE 115 | https://www.reddit.com/r/UBreddit/comments/18e884x/how_to_cse115/ |
| 4 | CSE116 and CSE191 prep | Advice for preparing for CSE 116 and CSE 191 | https://www.reddit.com/r/UBreddit/comments/18po39o/tips_for_preparing_for_cse116_and_cse191/ |
| 5 | CSE250 | Advice about CSE 250 | https://www.reddit.com/r/UBreddit/comments/khvrxt/cse250/ |
| 6 | BS Computer Science difficulty | Opinions about how hard UB CS is | https://www.reddit.com/r/UBreddit/comments/1c86ts7/is_bs_computer_science_hard_here_or_even_below/ |
| 7 | UB CS as a transfer | Advice about transferring to UB for CS | https://www.reddit.com/r/UBreddit/comments/1dqkacr/is_it_worth_coming_to_ub_for_cs_as_a_transfer/ |
| 8 | CS student experience | Student experience and internships search | https://www.reddit.com/r/UBreddit/comments/1evn8zd/experience_as_a_computer_science_student_looking/ |
| 9 | Picking CS professors | Advice about choosing CS professors | https://www.reddit.com/r/UBreddit/comments/1gr8800/help_me_pick_my_professors_for_computer/ |
| 10 | Incoming CS freshman | Advice for incoming CS freshmen | https://www.reddit.com/r/UBreddit/comments/n69wz8/incoming_computer_science_freshman_fall_2021/ |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:** About 700 characters

**Overlap:** About 150 characters

**Reasoning:** My documents are Reddit threads, so they are short posts and comments. I want each chunk to be long enough to contain a full idea, but not so long that it mixes many different topics. The overlap helps if any important advice is split between the two chunks.

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:** all-MiniLM-L6-v2 from sentence-transformers

**Top-k:** 5

**Production tradeoff reflection:** I would compare models based on accuracy, speed, cost, and how well they understand informal student language. A local model is cheaper and private, but a stronger API model might return better search results.

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | What do students say about the overall difficulty of CS at UB? | Students say CS can be difficult and workload-heavy, but it is manageable if students stay consistent and use resources. |
| 2 | What advice do students give for CSE 115? | Students should practice often, keep up with assignments, and not fall behind. |
| 3 | How should students prepare for CSE 116 and CSE 191? | Students should prepare for programming, data structures, logic, and basic solid math. |
| 4 | What do students say about CSE 250? | Students describe CSE 250 as an important and difficult course that needs consistent studying. |
| 5 | What do students say about choosing CS professors? | Students look at teaching style, difficulty, grading, and other students' experiences. |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. Reddit text can be noisy. Some comments may include jokes, deleted posts, usernames, or side conversations that are not useful.

2. Some threads talk about many topics at once. If my chunks are too big, one chunk may mix courses, professors, and career advice together.

3. I need to keep source names with every chunk because if I lose the source metadata, the final answers will not have good citations.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

```text
-> Document Ingestion (load Reddit text files) 
-> Cleaning (remove empty lines and extra noise) 
-> Chunking (700 characters, 150 overlap) 
-> Embeddings (all-MiniLM-L6-v2) 
-> Vector Store (ChromaDB) 
-> Retrieval (top 5 chunks) 
-> Generation (answer from retrieved chunks) 
-> Interface (user question -> answer + sources)
```


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

**Milestone 3 — Ingestion and chunking:** I will use Claude Code to help build the ingestion and chunking code. I will give it my documents folder structure, my chunk size, and my overlap. I expect it to write code that loads the .txt files, cleans the text, and creates chunks with source names attached.

**Milestone 4 — Embedding and retrieval:** I will use Claude Code to help build the embedding and retrieval code. I will tell it to use the all-MiniLM-L6-v2, ChromaDB, and top-k = 5.

**Milestone 5 — Generation and interface:** I will use Claude Code to help connect retrieval to the LLM and make a simple query interface. I will give it my rule that answers must only use retrieved chunks and must show sources.