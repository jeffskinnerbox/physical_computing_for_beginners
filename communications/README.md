
# README

Everything here is about talking to students and parents, not teaching them: marketing copy,
a one-off kick-off note, and the registration roster. None of it feeds the syllabus/lesson-plan/
BOM generation pipeline described in the root [README][01].


## Contents

```text
.
├── course-description.md   # public-facing course pitch (Makersmiths event listing text)
├── kick-off-message.md     # a personal note to a student/parent confirming a class meetup
├── october-2026-news-letter.md  # draft Makersmiths newsletter item written after the course finished
└── registration.md         # student roster — contains PII, see Notes below
```


## Purpose / Role in Repository

`course-description.md` is the marketing version of the course: the same physical-computing
pitch as `input/my-vision.md`'s Course Description section, but written for a public event
listing rather than as a generation seed. `kick-off-message.md` is a real, already-sent message
to a specific student and parent — it documents that communications happened, it isn't a template
to reuse. `october-2026-news-letter.md` is a draft newsletter item (title and ideas, not finished
copy) looking back on the course after its last class. None of these files is read by any of the
course-generation skills.


## Usage

Nothing runs here — it's reference copy, not source material for anything else in the repo.


## Notes

- `registration.md` holds real students' names, emails, phone numbers, and addresses. Treat it as
  sensitive PII: don't quote it, summarize its rows, or copy it into any generated doc, explainer,
  or handout. This README deliberately says nothing about its contents beyond "it exists and it's
  the registration roster."
- `kick-off-message.md` is a real message. The student's name is replaced with `[student]` and
  the signature's name and phone number are removed. Keep it that way — this repo is public. If
  you're drafting a new message in this style, write it fresh and don't add identifying details.
- See the root [README][01] for how this directory fits alongside the rest of the course repo.


[01]:../README.md
</content>
