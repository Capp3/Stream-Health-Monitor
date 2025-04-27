🎨🎨🎨 ENTERING CREATIVE PHASE: Algorithm Design 🎨🎨🎨

## Component Description
The algorithm component responsible for computing a unified health score for each stream by combining multiple metrics (e.g., availability, bitrate, packet loss, latency) into a single, interpretable value.

## Requirements & Constraints
- Compute health score in real-time (sub-second latency)
- Score must be normalized (0–100) for easy interpretation
- Handle missing or stale metric values gracefully
- Configurable weighting for each metric via YAML
- Thresholds for triggering alerts based on score
- Lightweight implementation suitable for Python 3.12 and Docker

## Options Analysis

### Option 1: Weighted Sum of Normalized Metrics
**Description**: Normalize each metric to a 0–1 scale, apply configurable weights, and sum to produce a composite score.
**Pros**:
- Simple and transparent computation
- Easy to configure and understand
- Low computational overhead
**Cons**:
- Assumes linear relationship between metrics and overall health
- Harder to capture non-linear interactions
**Complexity**: Low
**Implementation Time**: Short

### Option 2: Rule-Based Threshold Classification
**Description**: Define a set of if/else rules assigning discrete health categories (e.g., Good, Warning, Critical) based on metric thresholds.
**Pros**:
- Highly interpretable rules
- Easy to adjust individual thresholds
**Cons**:
- Produces categorical outputs, not continuous score
- Complex rule sets become hard to manage at scale
**Complexity**: Medium
**Implementation Time**: Medium

### Option 3: Statistical/ML Anomaly Detection
**Description**: Use statistical models or lightweight machine learning (e.g., z-score, clustering) to detect deviations from normal behavior and derive a health indicator.
**Pros**:
- Can capture non-linear relationships and anomalies
- Adaptive to evolving baseline behavior
**Cons**:
- Higher complexity and dependencies
- Requires training data and ongoing maintenance
- Potentially less transparent to users
**Complexity**: High
**Implementation Time**: Long

## Recommended Approach
Use **Option 1: Weighted Sum of Normalized Metrics**.

**Rationale**:
- Meets real-time and transparency requirements
- Simplest to implement and configure initially
- Facilitates quick iteration and tuning via YAML weights

## Implementation Guidelines
- Implement normalization functions for each metric (e.g., mapping bitrate range to [0,1])
- Load metric weights from configuration (`config.yaml`)
- Compute score: `score = sum(weight_i * normalized_metric_i) * 100`
- Expose health score via a FastAPI endpoint (`/health_score`)
- Include unit tests for boundary values and missing data handling

## Verification Checkpoint
- Health score computed within latency budget? [YES/NO]
- Score values range 0–100? [YES/NO]
- Configurable weights applied correctly? [YES/NO]
- Missing metrics handled without errors? [YES/NO]
- Alerts trigger when score falls below threshold? [YES/NO]

🎨🎨🎨 EXITING CREATIVE PHASE: Algorithm Design 🎨🎨🎨 