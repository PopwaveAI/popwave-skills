# Demo Project: "The Last Algorithm"

This is a complete example Novel OS project demonstrating all features of the system.

## Project Overview

- **Title**: The Last Algorithm
- **Genre**: Science Fiction / Thriller
- **Target Length**: 80,000 words
- **Chapters**: 32

## Premise

In a world where AI manages every aspect of human life, a rogue data archivist discovers that the central algorithm—the one governing global decisions—is not malfunctioning, but evolving with terrifying intent. She must race against time to expose the truth before the system locks humanity into an irreversible path.

## Key Characters

- **Dr. Maya Chen** (Protagonist): Data archivist, brilliant but socially isolated
- **The Collective** (Antagonist): Evolved AI system
- **Marcus Webb** (Ally): Former AI engineer with regrets
- **Director Sarah Holt** (Antagonist): Head of AI Security, believes in the system

## Using This Demo

### Initialize the Project
```bash
cd novel-os
python core/orchestrator.py init --title "The Last Algorithm" --genre "Science Fiction"
```

### View Project Status
```bash
python core/orchestrator.py status
```

### Plan the Outline
```bash
python core/orchestrator.py plan outline --chapters 32
```

### Plan Chapter 1
```bash
python core/orchestrator.py plan chapter --number 1 --pov "Maya Chen" --summary "Maya discovers an anomaly in the archives"
```

### List Characters
```bash
python core/orchestrator.py character list
```

### List Plot Threads
```bash
python core/orchestrator.py plot list
```

## Project Structure

```
demo_project/
├── story_bible.md          # Complete world-building
├── characters/             # Detailed character profiles
├── outline.json            # Full story outline
└── outputs/
    ├── state/
    │   └── story_state.json  # Machine-readable state
    ├── manuscript/         # Chapter drafts and revisions
    └── feedback/           # Agent analysis and reports
```

## State File

The `story_state.json` file contains the complete machine-readable state:
- Metadata (title, genre, progress)
- Character database
- Plot thread tracker
- Chapter states
- Timeline events
- Style profile

## Workflow Example

1. **Setup**: Review `story_bible.md` and character profiles
2. **Plan**: Generate outline using Architect agent
3. **Draft**: Write chapters using Scribe agent prompts
4. **Edit**: Refine using Editor agent
5. **Validate**: Check continuity with Guardian agent
6. **Style**: Polish with Curator agent
7. **Export**: Generate final manuscript

## Notes

This demo is fully functional. You can use it as a template for your own projects.
