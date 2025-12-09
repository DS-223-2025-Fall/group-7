# Core Pipeline for Smart Pricing Playground

This document describes the end-to-end **Core Pipeline** used to collect user interaction data, validate and structure it, and prepare it for pricing analytics within the Smart Pricing Playground platform.
The pipeline ensures that data used for Thompson Sampling and performance analysis is accurate, consistent, and updated continuously.

---

## 1. Overview of the Core Pipeline

The Core Pipeline supports the adaptive pricing engine by:

* Collecting real-time interaction data
* Validating and cleaning incoming events
* Transforming raw events into structured analytical datasets
* Computing metrics required by Thompson Sampling
* Storing final outputs for access by the API and dashboard

This workflow runs continuously as user activity takes place.

---

## 2. Data Collection (Extract Layer)

### 2.1 Sources of Data

Data is collected from:

* **Frontend interaction events**

  * Impressions
  * Conversions
  * Revenue events
  * Metadata (device, timestamp, session)

* **Backend API events**

  * Price selection logs
  * Experiment lifecycle events
  * Bandit updates

### 2.2 Event Capture Logic

When a user interacts with a pricing experiment, the frontend sends events such as:

* `impression_event`
* `conversion_event`
* `revenue_event`

Each event includes:

* Experiment ID
* Price/Bandit ID
* Timestamp
* Session or user identifier
* Outcome details (click, purchase, revenue)

Raw events are stored in a designated staging layer.

---

## 3. Data Refinement (Transform Layer)

### 3.1 Cleaning and Validation

The pipeline performs:

* Removal of malformed records
* Validation of experiment and price IDs
* Type enforcement (numeric, boolean, timestamp)
* Deduplication of impressions within a session
* Revenue normalization

### 3.2 Feature Construction

Metrics required for Thompson Sampling are computed:

#### Bernoulli conversion model

* `trials` = impressions
* `successes` = conversions
* `failures` = trials – successes

#### Gaussian revenue model

* `n` = count of revenue observations
* `mean` = average revenue
* `variance` = observed reward variance

### 3.3 Aggregation

Data is aggregated per:

* Experiment
* Price arm
* Optional time windows

**Example output**

| price_id | impressions | conversions | conversion_rate | mean_reward | variance |
| -------- | ----------- | ----------- | --------------- | ----------- | -------- |
| 1        | 120         | 18          | 0.15            | 3.20        | 1.4      |
| 2        | 115         | 26          | 0.23            | 3.85        | 1.1      |

### 3.4 Thompson Sampling Parameters

For each price arm:

**Bernoulli TS**

* α = successes + 1
* β = failures + 1

**Gaussian TS**

* μ = sample mean
* σ² = sample variance
* n = observation count

These parameters form the priors/posteriors used for price selection.

---

## 4. Data Storage and Delivery (Load Layer)

### 4.1 Database Structures

Processed data is stored in:

* `experiments`
* `bandits`
* `impressions`
* `conversions`
* `aggregates`
* `posterior_parameters`

These tables feed the algorithm, dashboard, and analytics API.

### 4.2 API Integration

Stored outputs are used by endpoints such as:

* `/bandits/select` – computes the next price via Thompson Sampling
* `/bandits/performance` – returns experiment metrics
* `/bandits/posterior` – returns posterior distributions

### 4.3 Dashboard Integration

The dashboard uses refined data to show:

* Conversion and revenue performance
* Price-arm comparisons
* Posterior distribution graphs
* Experiment progress in real time

---

## 5. Core Pipeline Summary

1. **Data Collection**
   Capture user interactions and store raw records.

2. **Data Refinement**
   Clean, validate, structure, and aggregate data. Compute Thompson Sampling parameters.

3. **Data Storage & Delivery**
   Persist processed datasets. Power API endpoints and dashboards.

---

## 6. Importance of the Core Pipeline

Accurate adaptive pricing requires a reliable data pipeline.
A strong Core Pipeline provides:

* Reliable conversion and revenue metrics
* Fast updates for real-time learning
* High-quality analytics for business insights
* Scalability for larger experiments

The Core Pipeline is therefore a foundational component of the Smart Pricing Playground system.

---
