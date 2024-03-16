# Puzzle hero solutions 2024


This repo contains the solutions for the following puzzle heroes 2024

```
iaccuse
zscorescam
aoe2civstechs
```

## Theory

The main thing to do for a participant is to read  pdfs of the solutions. They contain the theoretical explanations. They can be found in the theory folder.

## Code

For iaccuse and zscorescam, (not aoe2civstechs), the code that computes the solution from scratch is also available. The py mains in the root directory can be executed to generate the solutions in the "out" subfolders.

The execution of the mains also automatically generate the files (writeups, .yml challenges parameters...) that were needed to set the puzzles ont the puzzle hero page. That's why you see some code even for aoe2civstechs, but the aoe2 main already starts with the solution, it does not compute it by itself.

Code is not commented properly, unfortunately. So read the theory!

The repo is organized in many subfolder:

- iaccuse, zscorescam, aoe2civstechs contain code and data specific to their respective puzzle
- commonpy and commonfiles contain general functions or tools be all packages

Note that participants did not need to code as much code as is used here. A lot of code in this project is for additional confidence for the puzzle cretor (make sure there is no error). Roughly speaking, you don't need to look in commonfiles, commonpy and validating files to understand the solutions.

### How to execute

cd your way to the root, then

```
python main_iaccuse_both.py
```
or
```
python main_zscorescam.py
```

"out" subfolder in each puzzle folder contains the output. What you want to look at is the flag-steps files.