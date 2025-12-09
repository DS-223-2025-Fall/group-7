# ETL Pipeline for Smart Pricing Playground

This document describes the end-to-end ETL (Extract–Transform–Load) process used to collect user interaction data, clean and structure it, and prepare it for analysis within the Smart Pricing Playground platform.  
The ETL pipeline ensures that data required for Thompson Sampling and business analytics is accurate, consistent, and always up to date.

---

## 1. Overview of the ETL System

The ETL pipeline supports the adaptive pricing engine by:

- Collecting real-time data from user interactions
- Validating and cleaning incoming events
- Transforming raw events into structured datasets
- Calculating key metrics needed by Thompson Sampling
- Storing final outputs in a database accessible by the API and dashboard

The ETL workflow runs continuously as new impressions and conversions occur.

---

## 2. Extract Phase

### **2.1 Data Sources**

The system extracts data from the following sources:

- **Frontend Interaction Events**
  - Impressions (user sees a price)
  - Conversions (user purchases or clicks)
  - Revenue events
  - Device/time metadata

- **Backend API Requests**
  - Price selection logs
  - Experiment triggers
  - Bandit updates

### **2.2 Event Capture**

Each time a user interacts with the product page, the frontend sends an event to the backend:

- `impression_event`  
- `conversion_event`  
- `revenue_event`

Each event includes:
- Experiment ID  
- Bandit/price ID  
- Timestamp  
- User/session identifier  
- Outcome data (click, purchase, amount)  

Raw events are stored in a staging table or collection.

---

## 3. Transform Phase

The Transform phase prepares raw data for learning and analytics.

### **3.1 Data Cleaning**
- Remove malformed records  
- Validate experiment ID and price ID  
- Enforce proper types (boolean, numeric, timestamp)  
- Merge duplicate impressions for the same session  
- Normalize revenue values  

### **3.2 Feature Engineering**
The pipeline generates fields required for Thompson Sampling:

#### For Bernoulli TS (conversion):
- `trials` → number of impressions
- `successes` → number of conversions
- `failures` → trials – successes

#### For Gaussian TS (revenue):
- `n` → number of revenue events
- `mean` → average revenue per user
- `variance` → revenue variability

### **3.3 Aggregation Logic**

Aggregation is done per:
- Experiment
- Price arm
- Time window (optional)

**Example aggregated output:**

| price_id | impressions | conversions | conversion_rate | mean_reward | variance |
|---------|-------------|-------------|-----------------|-------------|----------|
| 1       | 120         | 18          | 0.15            | 3.20        | 1.4      |
| 2       | 115         | 26          | 0.23            | 3.85        | 1.1      |

### **3.4 Thompson Sampling Parameter Construction**

For each variant:

**Bernoulli TS:**
- α = successes + 1  
- β = failures + 1  

**Gaussian TS:**
- μ = sample mean  
- σ² = sample variance  
- n = count  

These become the priors/posteriors used for sampling and price selection.

---

## 4. Load Phase

### **4.1 Database Storage**

Transformed data is loaded into structured tables accessible to:

- The API layer  
- The analytics dashboard  
- The Thompson Sampling engine  

Common stored datasets include:

1. `experiments` (metadata)
2. `bandits` (price variants)
3. `impressions` (raw events)
4. `conversions` (raw events)
5. `aggregates` (daily/hourly summaries)
6. `posterior_parameters` (α, β, mean, variance)

### **4.2 API Exposure**

Loaded data is used by:
- `/bandits/select` → selects next price via Thompson Sampling  
- `/bandits/performance` → returns analytics tables  
- `/bandits/posterior` → returns posterior distributions  

### **4.3 Analytics Dashboard Integration**

The final outputs feed into:
- Price performance tables  
- Conversion charts  
- Revenue graphs  
- Posterior distribution visualizations  

This allows marketers to monitor experiments in real time.

---

## 5. ETL Workflow Summary

1. **Extract**  
   Capture real-time interactions, store them as raw events.

2. **Transform**  
   Clean events, compute metrics, aggregate results, generate TS parameters.

3. **Load**  
   Store final datasets, update dashboards, support the learning algorithm.

The ETL pipeline ensures that the adaptive pricing engine has accurate, timely data to make smarter allocation decisions and provide reliable insights.

---

## 6. Why ETL Matters

The performance of Thompson Sampling depends entirely on high-quality structured data.

A robust ETL pipeline delivers:
- Accurate conversion and reward metrics  
- Rapid updates to support real-time learning  
- Reliable analytics for business decisions  
- Scalability for large experiments  

The ETL layer is therefore a critical component of the Smart Pricing Playground architecture.

