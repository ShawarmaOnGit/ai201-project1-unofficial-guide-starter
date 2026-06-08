# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

My system covers unofficial student advice about studying Computer Science at the University at Buffalo.

This knowledge is useful because official UB pages show course requirements, but they don't show what students actually say about workload, professors, difficult classes, internships, or transfer experience. Most of this advice is in Reddit threads, so my system helps users search it and get answers with sources.

---

## Document Sources

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | How is Computer Science at UBuffalo? | Reddit thread | https://www.reddit.com/r/UBreddit/comments/10xaxf7/how_is_computer_science_at_ubuffalo/ |
| 2 | CS/AI/ML track advice | Reddit thread | https://www.reddit.com/r/UBreddit/comments/17wuvab/how_is_csaiml_track_for_someone_whos_only_getting/ |
| 3 | How to CSE115? | Reddit thread | https://www.reddit.com/r/UBreddit/comments/18e884x/how_to_cse115/ |
| 4 | Tips for preparing for CSE116 and CSE191 | Reddit thread | https://www.reddit.com/r/UBreddit/comments/18po39o/tips_for_preparing_for_cse116_and_cse191/ |
| 5 | CSE250 | Reddit thread | https://www.reddit.com/r/UBreddit/comments/khvrxt/cse250/ |
| 6 | Is BS Computer Science hard here or even below? | Reddit thread | https://www.reddit.com/r/UBreddit/comments/1c86ts7/is_bs_computer_science_hard_here_or_even_below/ |
| 7 | Is it worth coming to UB for CS as a transfer? | Reddit thread | https://www.reddit.com/r/UBreddit/comments/1dqkacr/is_it_worth_coming_to_ub_for_cs_as_a_transfer/ |
| 8 | Experience as a computer science student looking... | Reddit thread | https://www.reddit.com/r/UBreddit/comments/1evn8zd/experience_as_a_computer_science_student_looking/ |
| 9 | Help me pick my professors for computer... | Reddit thread | https://www.reddit.com/r/UBreddit/comments/1gr8800/help_me_pick_my_professors_for_computer/ |
| 10 | Incoming Computer Science Freshman Fall 2021 | Reddit thread | https://www.reddit.com/r/UBreddit/comments/n69wz8/incoming_computer_science_freshman_fall_2021/ |

---

## Chunking Strategy

**Chunk size:** 700 characters

**Overlap:** 150 characters

**Why these choices fit your documents:** My documents are Reddit threads, so they are made of posts and comments. I used 700 characters because I wanted each chunk to have enough context to make sense, but not be so long that it mixes too many topics together. I used 150 characters of overlap so that if useful advice is near the edge of one chunk, it can still show up in the next chunk. Before chunking, I cleaned the text by removing extra whitespace and repeated empty lines.

**Final chunk count:** 31 chunks

## Sample Chunks

1. Source: ub_cs_difficulty_reddit.txt, chunk 0  
   Text: "Coming from an average student freshman year, even the hw assignments took me days of nonstop work to complete, and don’t even get me started on the labs and projects..."

2. Source: ub_cs_general_experience_reddit.txt, chunk 0  
   Text: "Like all programs, it is what you make of it. You can squeeze tons of value out of the UB CS program if you put in the effort for good grades, network with professors and peers, and take advantage of resources..."

3. Source: ub_cs_internship_advice_reddit.txt, chunk 0  
   Text: "If it's a local small-medium company, you don't need much leetcode. Just something that demonstrates competency. If it's a startup, they value relevant projects way more..."

4. Source: ub_cse116_advice_reddit.txt, chunk 0  
   Text: "For 116, I would recommend familiarizing yourself with Java syntax. And then learn concepts of OOP like classes and polymorphism..."

5. Source: ub_cse250_advice_reddit.txt, chunk 0  
   Text: "CSE 250 is the main filter course for CS graduates... Everyone who has good basics, solid fundamentals and is willing to put in the crazy work..."

---

## Embedding Model

**Model used:** all-MiniLM-L6-v2 from sentence-transformers

**Production tradeoff reflection:** I used all-MiniLM-L6-v2 because it runs locally, is free, and works well enough for a class project. For a real system, I would compare models based on accuracy, speed, cost, context length, and how well they understand informal student language.

## Retrieval Test Results

### Query 1: What do students say about the overall difficulty of CS at UB?

Top returned chunks:
- ub_cse250_advice_reddit.txt chunk 0
- ub_cs_transfer_value_reddit.txt chunk 3
- ub_cse115_advice_reddit.txt chunk 0
- ub_cs_transfer_value_reddit.txt chunk 1
- ub_cs_transfer_value_reddit.txt chunk 5

These chunks are relevant because they discuss the difficulty of UB CS, including CSE 250 being a filter course, the program being rigorous and students needing dedication to succeed.

### Query 2: How is CSE 115?

Top returned chunks:
- ub_cse250_advice_reddit.txt chunk 0
- ub_cse115_advice_reddit.txt chunk 0
- ub_cs_incoming_student_advice_reddit.txt chunk 1
- ub_cs_professor_advice.txt chunk 0
- ub_cse116_advice_reddit.txt chunk 2

These chunks are only partially relevant. The CSE 115 chunk is useful because it directly explains that CSE 115 is rough and focuses on problem solving, but the retriever also returned unrelated chunks from CSE 250, professor advice, and CSE 116.

### Query 3: How should students prepare for CSE 116 and CSE 191?

Top returned chunks:
- ub_cse116_advice_reddit.txt chunk 0
- ub_cse116_advice_reddit.txt chunk 1
- ub_cse115_advice_reddit.txt chunk 0
- ub_cse250_advice_reddit.txt chunk 0
- ub_cse116_advice_reddit.txt chunk 2

These chunks are relevant because the top CSE 116 chunks mention Java syntax, OOP, data structures, IntelliJ, recitations, set theory, graphs, and proofs.

---

## Grounded Generation

**System prompt grounding instruction:** The system tells the model to answer using only the retrieved chunks. If the retrieved chunks dooesn't contain enough information, the model must say "I don't have enough information from the documents to answer that." This helps stop the model to not hallucinate.

**How source attribution is surfaced in the response:** After the answer, the system shows the retrieved source files and chunk numbers. For example, it displays sources like "ub_cse250_advice_reddit.txt (chunk 0)". This makes it clear where the answer came from.

## Example System Responses

### Example 1

Question: What do students say about the overall difficulty of CS at UB?

Answer: Students say that the CS program at UB is "extremely challenging" and "rigorous", with a high dropout rate, especially after taking CSE 250, which is considered a filter course. However, some students also believe that with dedication and hard work, the program is "completely doable."

Sources:
- ub_cse250_advice_reddit.txt chunk 0
- ub_cs_transfer_value_reddit.txt chunk 3
- ub_cse115_advice_reddit.txt chunk 0
- ub_cs_transfer_value_reddit.txt chunk 1
- ub_cs_transfer_value_reddit.txt chunk 5

### Example 2

Question: How should students prepare for CSE 116 and CSE 191?

Answer: To prepare for CSE 116, students should learn Java syntax, OOP concepts like classes and polymorphism, and basic data structures like linked lists, trees, and graphs. For CSE 191, students should put in effort during the class, attend recitations, and optionally learn set theory, graphs, and basic proofs.

Sources:
- ub_cse116_advice_reddit.txt chunk 0
- ub_cse116_advice_reddit.txt chunk 1
- ub_cse115_advice_reddit.txt chunk 0
- ub_cse250_advice_reddit.txt chunk 0
- ub_cse116_advice_reddit.txt chunk 2

### Out-of-Scope Example

Question: What is the best dining hall at UB?

Answer: I don't have enough information from the documents to answer that.

Sources: The retrieved chunks were not about dining halls, so the system refused to answer (expected behavior).

## Query Interface

I built a simple Gradio interface in `app.py`.

The interface has:
- A text box where the user enters a question
- An Ask button
- An answer box that shows the generated response
- A sources box that shows the retrieved source files and chunk numbers

Sample interaction:

Question: How should students prepare for CSE 116 and CSE 191?

Answer: To prepare for CSE 116, students should familiarize themselves with Java syntax, OOP concepts, and data structures. For CSE 191, students should attend recitations, take notes, and learn basics like set theory, graphs, and proofs.

Sources:
- ub_cse116_advice_reddit.txt chunk 0
- ub_cse116_advice_reddit.txt chunk 1
- ub_cse116_advice_reddit.txt chunk 2

---

## Evaluation Report

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What do students say about the overall difficulty of CS at UB? | It is hard and students have to put in consistent work. Students should not blindly go through the program without using resources or planning carefully. | Students say UB CS is extremely challenging and rigorous, but doable for students who dedicate themselves to learning. It also mentions difficult courses like CSE 250. | Relevant | Accurate |
| 2 | How is CSE 115? | It focuses on programming fundamentals and problem solving. Students need to pay attention to details, practice, and build intuition instead of only memorizing syntax. | The system said CSE 115 is rough and focuses on using the language to solve problems, not just learning the language. It also said students may feel behind. | Partially relevant | Partially accurate |
| 3 | How should students prepare for CSE 116 and CSE 191? | For CSE 116, students should learn basic Java, OOP, and data structures. For CSE 191, students should focus on logic, discrete math ideas, recitations, and good notes. | The system recommended Java syntax, OOP, data structures, IntelliJ, set theory, graphs, proofs, recitations, and notes. | Relevant | Accurate |
| 4 | What do students say about CSE 250? | It is not an easy course. Students describe it as difficult and workload-heavy, and they need strong fundamentals and consistent effort. | The system said CSE 250 is extremely difficult and complicated, and described it as a filter course for CS students. | Relevant | Accurate |
| 5 | What do students say about choosing CS professors? | Students say there are good and bad professors. Some professors have strong teaching styles, and students choose based on lecture style, live coding, grading, and personal preference. | The system said some professors are fantastic, such as Hertz, Jesse, and Paul, but also mentioned that there are some bad professors. | Relevant | Accurate |

---

## Failure Case Analysis

**Question that failed:** How is CSE 115?

**What the system returned:** The system gave a mostly correct answer. It said CSE 115 is rough and focuses on solving problems, not just learning the programming language. However, it also retrieved wrong chunks

**Root cause (tied to a specific pipeline stage):** The issue was in the retrieval stage where it retrieved the correct CSE 115 chunk, but it also retrieved unrelated chunks from CSE 250, incoming freshman advice, professor advice, and CSE 116. This happened because the question was short and vague, so the retriever matched general CS course difficulty instead of only CSE 115.


**What you would change to fix it:** I would add more CSE 115 texts and use metadata filtering by course. I could also improve the interface by asking users to write more specific questions, like "What advice do students give for CSE 115?"

---

## Spec Reflection

**One way the spec helped you during implementation:** The spec helped me stay organized because I already knew my domain, document folder, chunk size, embedding model, and top-k value before coding. This made it easier to tell Claude Code exactly what to build instead of asking for random code.

**One way your implementation diverged from the spec, and why:** My original goal was to get more chunks from the documents, but my final system had 31 chunks. I kept this because the chunks were readable and useful, even though the count was lower than ideal. If I had more time, I would collect more Reddit comments so the system has better coverage.

---

## AI Usage
**Instance 1**

- *What I gave the AI:* I gave Claude Code my documents/raw folder structure and my chunking plan from planning.md. I told it to load .txt files, clean the text, split it into 700 character chunks with 150 character overlap and then save the chunks to JSON.
- *What it produced:* Claude Code created ingest.py, which loads the raw Reddit text files, cleans them, creates chunks, and saves them to documents/chunks/chunks.json.
- *What I changed or overrode:* I checked the output chunks and noticed the first version only created 19 chunks. I added more Reddit comments to the raw files and reran the pipeline until it gave 31 chunks.

**Instance 2**

- *What I gave the AI:* I gave Claude Code my retrieval plan and told it to use all-MiniLM-L6-v2, ChromaDB and top-k = 5.
- *What it produced:* Claude Code created retrieve.py, which embeds the chunks, storeed them in ChromaDB and returned the top retrieved chunks for a question.
- *What I changed or overrode:* I tested the retrieval with my evaluation questions and checked that the returned chunks were actually related to the questions before moving to generation.

**Instance 3**

- *What I gave the AI:* I gave Claude Code my grounded generation requirement and told it to use Groq, answer only from retrieved chunks, and show sources.
- *What it produced:* Claude Code created query.py and app.py, which connects retrieval to the LLM and show a simple Gradio interface.
- *What I changed or overrode:* I tested an unrelated question about dining halls to make sure the system refused instead of making up an answer.