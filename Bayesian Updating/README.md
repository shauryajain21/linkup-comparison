# Bayesian Belief Updating Experiment

An interactive web-based experiment to study how participants update their probability estimates based on sequential evidence.

## Overview

This experiment investigates Bayesian reasoning by having participants:
- Draw balls from jars with unknown black:white ratios
- Observe the color of each drawn ball
- Estimate the probability that the next ball will be black
- Update their beliefs over 20 trials per jar across 3 different jars

## Experiment Design

### Structure
- **11 total jars** with different ratios: 0:10, 1:9, 2:8, 3:7, 4:6, 5:5, 6:4, 7:3, 8:2, 9:1, 10:0 (black:white)
- **3 jars per participant** randomly selected from the 11 available
- **20 trials per jar** (60 total trials)
- **Sampling with replacement** - each ball is returned after drawing

### Participant Flow
1. Enter participant ID
2. Read instructions
3. For each of 3 jars:
   - Draw a ball (color is revealed)
   - See history of all previous draws from this jar
   - Estimate probability next ball will be black (0-100% using slider)
   - Submit estimate
   - Repeat for 20 draws
4. Download data at completion

## Running the Experiment

### Local Usage
Simply open `index.html` in any modern web browser:
```bash
open index.html
```

### Web Hosting
Upload the `index.html` file to any web server or hosting service:
- GitHub Pages
- Netlify
- Vercel
- Any standard web hosting

No server-side code or database required - runs entirely in the browser!

## Data Collection

### Exported Data Format
Data is exported as CSV with the following columns:

| Column | Description |
|--------|-------------|
| `participantId` | Unique identifier entered by participant |
| `timestamp` | ISO timestamp of the response |
| `jarId` | ID of the jar (0-10) |
| `jarRatioBlack` | Number of black balls in the jar (0-10) |
| `jarRatioWhite` | Number of white balls in the jar (0-10) |
| `jarNumber` | Which jar in sequence (1-3) |
| `trialInJar` | Trial number within current jar (1-20) |
| `totalTrial` | Overall trial number (1-60) |
| `drawnColor` | Color of ball drawn ('black' or 'white') |
| `estimatedProbability` | Participant's probability estimate (0-100) |
| `responseTimeMs` | Time taken to make estimate (milliseconds) |

### Example Data Row
```csv
participantId,timestamp,jarId,jarRatioBlack,jarRatioWhite,jarNumber,trialInJar,totalTrial,drawnColor,estimatedProbability,responseTimeMs
P001,2025-01-15T10:30:45.123Z,5,5,5,1,1,1,black,60,3421
```

## Theoretical Bayesian Analysis

### Prior
If participants don't know which jar they have, the prior should be uniform over all 11 possible ratios.

### Likelihood
For each draw, the likelihood of drawing a black ball from a jar with ratio `k` black balls out of 10:
```
P(Black | k) = k/10
```

### Posterior Update
Using Bayes' theorem after observing sequence of draws:
```
P(jar=k | draws) ∝ P(draws | jar=k) × P(jar=k)
```

### Expected Probability
The Bayesian estimate for next ball being black:
```
P(next=black | draws) = Σ P(jar=k | draws) × (k/10)
```

## Customization

### Modify Jar Ratios
Edit the `CONFIG.jarRatios` array in `index.html`:
```javascript
jarRatios: [
    [0, 10], [1, 9], [2, 8], // etc.
]
```

### Change Number of Trials
Edit `CONFIG.trialsPerJar`:
```javascript
trialsPerJar: 20  // Change to desired number
```

### Change Number of Jars per Participant
Edit `CONFIG.jarsPerExperiment`:
```javascript
jarsPerExperiment: 3  // Change to desired number
```

## Features

### User Interface
- ✅ Clean, modern design with animations
- ✅ Visual ball drawing with color-coded history
- ✅ Slider for probability estimation (0-100%)
- ✅ Progress tracking (jar, trial, overall progress)
- ✅ Responsive design for different screen sizes

### Data Quality
- ✅ Response time tracking
- ✅ Complete draw history preserved
- ✅ Participant ID tracking
- ✅ Timestamp for each response
- ✅ CSV export for easy analysis

### Experiment Control
- ✅ Random jar selection
- ✅ True random sampling with replacement
- ✅ Sequential trial structure
- ✅ No feedback on "correctness"

## Analysis Suggestions

### Key Metrics to Analyze
1. **Deviation from Bayesian posterior**: Compare participant estimates to theoretical Bayesian calculations
2. **Learning rate**: How quickly estimates converge toward true ratio
3. **Recency bias**: Over-weighting recent draws vs. entire history
4. **Representativeness heuristic**: Over-interpreting small samples
5. **Response time patterns**: Correlation with uncertainty or difficulty
6. **Individual differences**: Clustering of update strategies

### Visualization Ideas
- Plot estimated probability over trials (overlay Bayesian posterior)
- Heatmap of estimates by true jar ratio
- Scatter plot: estimated vs. Bayesian probability
- Distribution of final estimates by jar type

## Browser Compatibility

Tested and working on:
- ✅ Chrome/Edge (v90+)
- ✅ Firefox (v88+)
- ✅ Safari (v14+)

## License

This experiment tool is provided for research and educational purposes.

## Live Demo

Try the experiment: https://shauryajain21.github.io/bayesian-updating-experiment/

## Citation

If you use this tool in your research, please cite:
```
Bayesian Belief Updating Experiment Tool (2025)
https://github.com/shauryajain21/bayesian-updating-experiment
```

## Contact

For questions or suggestions about the experiment design, please open an issue on GitHub.
