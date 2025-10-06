# AIAgent
*(No time for pithy, pseudo-philosophical name branding)*

### IMPORTANT DISCLAIMER
This is a toy. This is not a production-level LLM assistant. It was built by a novice. It does not have the robust guardrails you would find in a production. It also currently has the ability to ***run arbitrary code*** and ***write files to disk***. 
Do not trust it. This code is provided as a proof-of-concept ONLY, and is provided as-is without any warranty, promisse, or guarantee, express or implied. In fact, I am actively warning you that you should not use this project in its current form
for any level of production. Caveat emptor.

-# Also, my legal representation advises me to state that no AIs were harmed in the making of this agent. Despite our best efforts.

## Description
Project Guidelines: https://www.boot.dev/courses/build-ai-agent-python

This is the product of a guided Boot.dev project that teaches learners how to put together an LLM agent that can act as a coding assistant. The project guidance did not simply instruct the learner to "copy this code and run it", but instead
provided high-level instructions on the intended goals and referenced the relevant documentation that could help achieve them.

## Capabilities
This LLM agent currently leverages Google Gemini to parse text prompts, and has a small suite of tools to assist with software development. It can:
- Parse a directory for file information (this allows the Gemini LLM to see and identify files in its working directory to act on them)
- Read and write files on disk (constrained to its working directory, but please, please, please be careful. See above IMPORTANT DISCLAIMER)
- Run Python scripts (Primarily to gain read/write access to files)

## What This Cannot Do
- Make you a programming god (sorry, vibe coders)
- Take over the world
- Replace your higher cognitive functions
- Act as your therapist
- Make you tea

## How to Use It
1. Clone the project locally
2. Go to [Google AI Studio](https://aistudio.google.com/api-keys) and get your own API key (no piggybacking off of my precious API quota)
3. In the project root folder, create a file named ".env", and paste the following:
```GEMINI_API_KEY="[YOUR API KEY GOES HERE]" ```
4. Run command line:
```python3 main.py "PROMPT GOES HERE" [--verbose]```
5. ~~Sob hysterically as it sudo rm -rf / --NO-PRESERVE-ROOTs your hard drive and deletes your entire hardfought collection of memes~~ 
Sit back in amazement as I offload the LLM functions to Google, giving the false impression of unprecedented competence.
6. ???
7. Profit!

## Future Project Plans
- Continual improvement of guardrails until I am convinced that giving this... thing... the ability to read, write, and execute code wasn't a phenomenally bad idea.
- Giving it a nice GUI so that you don't have to dirty your precious hands with CLI
