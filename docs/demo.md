# Demo: Smart Pricing Playground

This page provides an overview of how the Smart Pricing Playground works from a user’s perspective.  
It demonstrates the main workflow for creating experiments, assigning prices, collecting data, and viewing real-time analytics.

---

## 1. Overview of the Demo

The demo showcases how marketers or product managers can:

- Upload a product
- Define price variants
- Launch a pricing experiment
- Automatically allocate traffic using Thompson Sampling
- Review real-time analytics
- Identify the optimal price efficiently

The system is fully automated and does not require statistical expertise.

---

## 2. Step-by-Step Demo Workflow

### **Step 1 — Upload or Select a Product**

Users begin by creating a new product or selecting an existing one.

Uploaded metadata includes:
- Product name  
- Description  
- Image  
- Price options  

**Example:**
- Product: "Wireless Fitness Tracker"
- Price Variants: $29, $39, $49

---

### **Step 2 — Define Price Variants**

The user specifies all price points they want to test.

The platform allows:
- Any number of price options  
- Either even or custom initial distribution  
- Optional per-variant description or label  

The system initializes a bandit agent for each price.

---

### **Step 3 — Launch the Experiment**

Once price variants are saved, the experiment becomes active.

The system starts:
- Tracking impressions  
- Tracking conversions (purchase / click)
- Logging revenue events
- Updating posterior probability distributions for each price arm

This marks the start of adaptive learning.

---

### **Step 4 — Real-Time Visitor Interactions**

Visitors land on the demo product page and see a single price option.

- The first several visitors are shown random prices
- As data accumulates, Thompson Sampling begins prioritizing strong performers
- Low-performing prices automatically receive less traffic

The system records:
- Which price the visitor saw
- Whether they converted
- How much revenue was generated

---

### **Step 5 — Thompson Sampling in Action**

As soon as conversions begin, the learning loop runs:

1. For each price, sample from its posterior distribution  
2. Select the price with the highest sampled value  
3. Serve this price to the next user  
4. Update posteriors after each interaction  

This ensures:
- Faster convergence to the optimal price  
- Lower regret  
- More efficient experimentation  

---

## 3. Demo Interface Components

### **Product Display**
Shows:
- Product name
- Product image
- Descrip
