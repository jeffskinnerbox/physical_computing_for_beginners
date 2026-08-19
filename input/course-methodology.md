
READ THESE DOCs
* [How to Apply Coding Agents to Non-Programming Tasks](https://towardsdatascience.com/how-to-apply-coding-agents-to-non-programming-tasks/)
* [Claude Code for Non-Coding Projects/Work: A Complete Getting Started Guide](https://www.reddit.com/r/ClaudeAI/comments/1q403xw/claude_code_for_noncoding_projectswork_a_complete/)

----

A class is a single educational session,
a course is a full series of classes that covers a broad subject over time,
and a workshop is a short, hands-on gathering focused on building a specific practical skill or working on an active project.

* Class
  * Definition: A single meeting or lesson.
  * Focus: Learning a specific topic or taking part in a scheduled instruction period.
  * Duration: Usually lasts one hour to a few hours.
* Course
  * Definition: A complete program made of multiple classes.
  * Focus: Comprehensive learning, often with a syllabus, homework, grades, or a certificate at the end.
  * Duration: Weeks, months, or an entire academic semester.
* Workshop
  * Definition: An interactive, highly practical session.
  * Focus: Doing, building, or solving a problem rather than just listening to a lecture. Participants often bring their own work or collaborate.
  * Duration: Typically short, lasting from a few hours to a couple of days.

Lectures are large, formal presentations where an instructor speaks to an entire course.
Seminars are smaller, interactive group discussions exploring past topics.
Tutorials are intimate, practical problem-solving sessions focusing on specific coursework, assignments, or individual help.

* Lectures
  * Size: Large groups, often ranging from 50 to hundreds of students in an auditorium or theater.
  * Format: One-way communication where the professor presents theories, core concepts, and the "big picture".
  * Student Role: Active listening and intensive note-taking; little to no direct interaction.
  * Preparation: Usually no advance preparation or reading is required.
* Seminars
  * Size: Smaller groups of 15 to 30 students.
  * Format: Discussion-based sessions examining specific readings, case studies, or student presentations.
  * Student Role: Active participation, debating ideas, and sharing analysis with peers.
  * Preparation: Advance reading or assigned work is mandatory.
* Tutorials
  * Size: Very small groups (10 to 15 students) or sometimes one-on-one with a tutor.
  * Format: Highly practical, collaborative problem-solving and assignment clarification.
  * Student Role: Asking specific questions, solving technical problems, and reviewing tricky lecture material.
  * Preparation: Bringing specific questions or unfinished coursework from previous classes.

----

# Course Creation Methodology
I have come to believe the following:
Coding agents are a way I can interact with basically any tasks that I work on.
There’s rarely a reason for me to work on a task, all by myself, without any help from coding agents.

Why do I believe this:
1. I might forgot some context fr my task, and the coding agent can help keep this information active while I address the task.
1. Much of the supporting work for a task,
   e.g. documents, slides, assembly instructions, research, etc.,
   can be done and automated through the coding agent.
1. I can ask the coding agent to plan sub-task, creating a work program for my task,
   and then the coding agent can just complete it for me with reminders in the future.
1. By using sub-agents, I can do more sub-tasks at the same time, simply becoming more productive.

## My Prompt
Review this entire directory concerning the course I will be teaching.
I have completed a detail vision of how the course will operate, goals/expectations, etc.
all documented in @input/my-vision.md.
From @input/my-vision.md, I have generated the contents of the @lesson_plans directory.

I now want you to help me generate lesson scrips for each each class.
I define a lesson scripts as follows:
1. A lesson script is a markdown file that gives very detail instruction to the instructor on how to build and code the class project.
1. The lesson script will be given to the students of the class to follow along.
   The lesson script will be accessible to the student and instructor via a GitHub site,
   and the student will use the lesson script to copy&paste commands and code for their creation of the project.
1. The lesson script will be a combination of explanatory text and CircuitPython code (or other types of code) needed for the project.
1. The lesson script needs to be sufficiently detailed so that a student, without the aid of the instructor, can do the project.
1. The example code (considered pseudo-code) in the lesson plans is lightly commented,
   but the expectation is the code in the lesson script will be commented in more detail and must complete in every why.
1. The explanatory text in the lesson script should describe each of the breakout boards, devices, key CircuitPython modules, PIN outs, etc.
1. The code in the lesson script will build the project in phases,
   as outline in its corresponding lesson plan document in @lesson_plan/ directory.
   You should include print statements so the student can see what is happening in the code.
1. The lesson script will not only provide code for the project but will also provide a detail plan to construct the project physically.
   This includes a wiring table of the breadboard, microcontroller, breakout boards, discrete components (switches, LED, resistors, etc.), etc.
1. At the very end of the lesson script, the projects entire CircuitPython code should be listed,
   with comments, but amount of print statements could be reduced to avoid clutter.
   Also a wiring table should be provided for the physical build.
   This last section should be useful for a student to jump to the end and build the whole project
   without going through all the earlier build steps in the lesson script.
1. The first section in the lesson script should say what this project is all about,
   and the last section should outline what the student should have learned.
1. All lesson script should look similar and have the same structure and flow.
1. The naming convention for the lesson script documents will follow the same pattern as that used for the lesson plans.

Step 1:
If you see any ambiguity or error in this task I'm asking of you, first ask me for clarification.
Ask as many question you need to make the task clear to you.

Step 2:
Propose a documentation template that will be used for all the lesson scripts.
Pause and let me review your template and provide feedback.

Step 3:
Create a lesson plan for the first class (class-01) then stop and let me review it.



