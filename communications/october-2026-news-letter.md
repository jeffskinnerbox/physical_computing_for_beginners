# Title

## Ideas
Mid-October I finished instructing a course here at Makersmiths titled [Physical Computing for Beginners](https://www.makersmiths.org/event-6785489).
The goal was for the to students learned a few things about building a electronic device,
how sensors & actuators can interface with the physical world via a microcomputers computation.
But most of all, I want them to experience how they might be able to do this on their own.

The current state of software & hardware makes building DIY electronics easy.
Yes, this is a bit of of an over statement, because you must first acquire the foundational knowledge,
but I strongly believe there is a learning path for even a complete novice.
So what does this "learning path" look like?

I purposely structured the course so they had to do all the physical and software building of their project, but not the coding.
Having the students design, write, and test the software would have been instructive
but would have greatly lengthened the course.
My main objective was to empower them with elementary knowledge about assembling/building the electronics project.

Open source software & hardware has provided inexpensive components to a sufficiently motived amateur.
Along with this is a huge number of well documented project on the Internet.

Why physical computing?
Its the foundation for the Internet of Things (IoT), Physical AI, Robotics.

Just in case you haven't noticed, there is a great deal of excitement around artificial intelligence (AI) today,
to the point where every new business/product appears to be part of some grand AI plan.
This excitement has become so extreme that many people don't have a very informed understanding of it.

## Next Course
1. **Random Rover Tuning** - Dive deeper into the design/architecture of the robot to understand how to optimize the performance.
   Use simulation to trial improvements followed by class competition for the fastest robot.
   New students would have a pre-class to assemble the robot.
1. **Line Following Robot** - This could be a new build or a reuse of the Random Rover augment with with line following sensors and logic.
   New students would have a pre-class to assemble the robot.
1. **ROS2 Robot Simulation** - Introduce students to industrial robotics software (ROS2) using simulation tools.
   Don't build a robot this time, simulate it like professionals would do.
   Its faster, safer, and more economical.
1. **AI Algorithm Experiments** - Walk student through 70 years of AI research & development
   and stopping along the way for hands on experimentation with
   Perceptron, Q-Learning, Grokking, Physics Informed Neural Networks (PINN), etc.
   Follow a chart of Landmark milestones (e.g. Deep Blue, AlphaGo, ChatGPT) pulling out for experimentation Technical breakthroughs (e.g. Perceptron, Backpropagation)
1. **GrowBot** - Hands on learning how RL trained robot can be combined with agentic AI.
1. **Resurrection of TurtleBot 3** -
1. **xxx** - xxx

## Natural Progression of Course
Physical Computing for Beginners (Random Rover) --> ??? (We create an algorithm to escape) solve some engineering problems like battery quality and  explore additional sensors that could be helpful
                                                --> ??? (We create a simulation for training to escape)
                                                --> ??? (Rover self-learns an algorithm to escape)
                                                --> ??? (Hybrid using SLAM and planner like A*)
                                                --> ??? (TurtlBot3 with Lidar)

Concepts to learn:
* system 1 & system 2 brain - System 1 and System 2 are two mental modes of thinking popularized by psychologist Daniel Kahneman in his book _Thinking, Fast and Slow_. They are not separate physical structures in the brain, but rather a framework for understanding how we make decisions. See [The Evolution of AI: Chain of Thought and System 2 Thinking](https://ramonbnuezjr.medium.com/the-evolution-of-ai-chain-of-thought-and-system-2-thinking-f7820f568b50)
* self-supervised learning
* gorkking

Prompt:
I'm creating a game where a robot, who can sense surfaces / objects, is to escape an enclosed space with only one exit.
Has AI or machine learning been used to solve this problem?
If so, give me some insight on how this challenge has been solved.

Prompt:
I want the robot to learn to escape through training

```text
Algorithm choice

* Small fixed grid: tabular Q-learning, about 50 lines of Python and good for a first working version.
* Larger or randomized grids: DQN, or PPO with a recurrent policy.
* Continuous movement: recurrent PPO.

In Python, the usual stack is Gymnasium for the environment and Stable-Baselines3 for the algorithms (RecurrentPPO is in sb3-contrib). MiniGrid is a ready-made grid environment worth studying, since it is essentially this problem.

Is your game world a grid or continuous space? That decides which of these I’d sketch out in code for you.
```

Prompt:
My game world is not a grid but a continuous space.

---

Here are my ten, in chronological order rather than ranked.
This is a judgment call, and reasonable people would swap one or two.

1. Perceptron (1958): the first model that learned its own weights from examples instead of being hand-programmed.
1. Heuristic search (1956–68, culminating in A*): made problem-solving tractable by using estimates to prune the search space, like a GPS that ignores roads heading the wrong way.
1. Backpropagation (1986): efficient training of multi-layer networks. It works like a postmortem that traces a failure back through the call stack and assigns each function its share of the blame.
1. Probabilistic graphical models (1988): Pearl’s Bayesian networks gave AI a principled way to reason under uncertainty rather than with brittle if-then rules.
1. Temporal-difference learning and Q-learning (1988–89): the core of reinforcement learning, where the model learns from its own predictions, like revising your ETA mid-drive instead of waiting until you arrive.
1. Convolutional networks (1989): weight sharing across an image, so one small stencil slides everywhere instead of a separate detector being learned per pixel.
1. LSTM (1997): gated memory cells that fixed vanishing gradients in sequence models, essentially a register with learned write, keep, and erase lines.
1. GPU-trained deep networks (AlexNet, 2012): the proof that depth, data, and compute together beat hand-engineered features. The designs already existed; this was the engine finally strong enough for the airframe.
1. Attention and the transformer (2014–17): every token can look directly at every other token, giving random access instead of reading a tape, and it parallelizes well.
1. Self-supervised pretraining at scale (2018–20): train once on raw text by predicting missing or next tokens, then adapt to anything. This is what produced foundation models.

The close calls I left out are residual connections (2015), word embeddings (2013), and generative models (GANs in 2014, diffusion from 2015 to 2020).


