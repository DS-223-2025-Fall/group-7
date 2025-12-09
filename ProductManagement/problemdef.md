# DS223 - Marketing Analytics  
## Group Project – Problem Definition  
**Group 7**  
**Date:** 09.11.2025  

---

## 1. Problem Area

The selected problem area for the Marketing Analytics group project is **Pricing Strategy and Product Testing**.

Pricing plays a crucial role in determining a product’s market success. However, many businesses struggle to determine the optimal price point for their products, especially during the early stages of product introduction. Traditional methods such as surveys or static A/B testing often fail to:

- Adapt to changing consumer behavior  
- Learn efficiently from incoming data  
- Maximize revenue during the testing phase  

As a result, companies may lose revenue opportunities and make slower, less informed pricing decisions.

---

## 2. Preliminary Research

In today’s digital environment, businesses have access to **real-time user interaction data** from online platforms. Yet, most companies still rely on **static A/B pricing tests**, which:

- Divide users evenly among price options  
- Wait until a large sample size is reached to determine a winner  
- Do not adapt allocation based on performance in real time  

This approach is **inefficient, slow**, and does not fully utilize available data.

Recent research and industry applications suggest that **multi-armed bandit algorithms**, such as **Thompson Sampling**, can make pricing tests more dynamic and intelligent. These algorithms:

- Continuously learn from incoming data  
- Automatically adjust which price options are shown more frequently  
- Accelerate decision-making  
- Maximize cumulative conversions or revenue  

Recent studies have highlighted the benefits of adaptive learning approaches in dynamic pricing contexts. For example, algorithms capable of updating strategies in response to observed demand have been shown to significantly improve revenue outcomes (Qu, 2024).

Other studies emphasize the limitations of traditional A/B testing, which allocates equal traffic to all variants and delays decision-making. According to Kumar (2023), multi-armed bandit algorithms such as **Thompson Sampling**, **UCB**, and **Epsilon-Greedy** provide a more adaptive framework by continuously updating allocation based on real-time feedback. His findings show that Thompson Sampling achieves:

- Higher cumulative rewards  
- Lower regret  
- Better scalability in dynamic environments  

This supports our project’s use of **Thompson Sampling** as the core method for optimizing product pricing tests.

---

## 3. Specific Problem

Businesses lack a **data-driven, adaptive framework** that enables them to efficiently test and identify the best price for a product based on real-time consumer behavior.

**Research question:**

> How can companies dynamically test multiple price points for a product and automatically adapt to customer responses to find the optimal price?

---

## 4. Proposed Solution and Methodology

### 4.1 Data Collection

The proposed system will collect user interaction data from experimental product pages, including:

- **Impressions** – how many users saw each price  
- **Clicks or purchases** – conversion behavior  
- **Time of interaction**

These data points will feed directly into the learning algorithm.

### 4.2 Analytical Techniques

We will apply **Thompson Sampling**, a probabilistic multi-armed bandit method, to dynamically allocate traffic among different price variants.

The approach will use:

- **Bernoulli Thompson Sampling** for conversion-focused metrics  
  - Binary outcomes such as purchase / no purchase  

- **Normal (Gaussian) Thompson Sampling** for revenue-focused metrics  
  - Continuous outcomes such as purchase amount or total revenue per user  

### 4.3 Implementation Plan

1. Create a **web-based platform** where companies can upload products and define several price variants (e.g., three price points).  
2. Initially, **randomly assign** visitors to different variants.  
3. Track user interactions in real time and store them in a database.  
4. Run the **Thompson Sampling model** periodically to update which price option receives more exposure.  
5. Display **analytics dashboards** for marketers to monitor results, including:
   - Conversion rates  
   - Revenue per price point  
   - Algorithm learning curves and allocation over time  

---

## 5. Expected Outcomes

By implementing this system, companies are expected to:

- Identify optimal pricing **faster** and with **fewer user samples**  
- Increase **conversion rates** and **overall revenue**  
- Reduce the inefficiencies and delays of static A/B testing  
- Make **data-driven pricing decisions** supported by live customer feedback  

---

## 6. Evaluation Metrics

The effectiveness of the proposed solution will be assessed using the following **Key Performance Indicators (KPIs)**:

- **Revenue Uplift**  
  Increase in total sales achieved by faster convergence to the optimal pricing strategy.

- **Regret Minimization**  
  Reduction in potential revenue lost during the pricing test compared to an ideal strategy that always chooses the best price.

- **Model Efficiency**  
  Number of iterations or time steps required to identify the best-performing price option with high confidence.

---

## 7. References

Kumar, S. (2023). *Multi-Armed Bandit Algorithms in A/B Testing: Comparing the Performance of Various Multi-Armed Bandit Algorithms in the Context of A/B Testing.* Journal of Mathematical & Computer Applications, 2(2), 1–4. <https://doi.org/10.47363/JMCA/2023(2)159>  

Qu, J. (2024). *Survey of dynamic pricing based on multi-armed bandit algorithms.* Applied and Computational Engineering, 37(1), 160–165. <https://doi.org/10.54254/2755-2721/37/20230497>
