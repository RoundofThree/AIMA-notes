# Tutorial 7 ─ Supervised learning
## Classification

Consider the training data shown here from a binary classification problem. 

| Record ID | Gender | Income | Credit Rating | Class |
| --- | --- | --- | --- | --- |
| 1 | M | High | Fair | A |
| 2 | M | Medium | Excellent | A |
| 3 | M | Medium | Excellent | A |
| 4 | M | Medium | Poor | A |
| 5 | M | Medium | Poor | A |
| 6 | M | Medium | Poor | A |
| 7 | F | Medium | Fair | A |
| 8 | F | Medium | Fair | A |
| 9 | F | Medium | Excellent | A |
| 10 | F | Low | Poor | A |
| 11 | M | High | Poor | B |
| 12 | M | High | Excellent | B |
| 13 | M | High | Excellent | B |
| 14 | M | Low | Poor | B |
| 15 | F | Low | Fair | B |
| 16 | F | Low | Fair | B |
| 17 | F | Low | Excellent | B |
| 18 | F | Low | Excellent | B |
| 19 | F | Low | Excellent | B |
| 20 | F | Low | Poor | B |

### Question 1
Calculate the GINI index for all attributes. 

**Gender**:

$GINI(gender=M) = 1 - (6/10)^2 - (4/10)^2 = 0.48$

$GINI(gender=F) = 1 - (4/10)^2 - (6/10)^2 = 0.48$

$GINI_{split} = \frac{10}{20} * 0.48 + \frac{10}{20} * 0.48 = 0.48$

**Income**:

$GINI(income=low) = 1 - (1/8)^2 - (7/8)^2 = 0.21875$

$GINI(income=high) = 1 - (1/4)^2 - (3/4)^2 = 0.375$

$GINI(income=medium) = 1 - (8/8)^2 - (0/8)^2 = 0$

$GINI_{split} = \frac{8}{20} * 0.21875 + \frac{4}{20} * 0.375 = 0.1625$

**Credit Rating**:

$GINI(credit=poor) = 1 - (4/7)^2 - (3/7)^2 = \frac{24}{49}$

$GINI(credit=fair) = 1 - (3/5)^2 - (2/5)^2 = 0.48$

$GINI(credit=excellent) = 1 - (3/8)^2 - (5/8)^2 = 0.46875$

$GINI_{split} = \frac{7}{20} * \frac{24}{49} + \frac{5}{20} * 0.48 + \frac{8}{20} * 0.46875 = 0.4789$


### Question 2
Which attribute would be first split (ie. the root node) of the decision tree?

**Answer**: Income.

## Regression
### Question 1 

Which of the following statements is true?

The line described by a regression function attempts to:

- Pass through as many points as possible.
- Pass through as few points as possible. 
- Minimise the number of points it touches. 
- **Minimise the squared distance from the points.**

### Question 2 
A regression equation has slope $33.57$. The mean $y$ is $132.71$ and the mean $x$ is $2.71$. What is the value of the intercept?

**Answer**: $y_0 = 132.71 - 33.57 * 2.71 = 123.0353$.

### Question 3
The regression equation $y = 5.57 - 0.065x$. How many tickets would you predict for a twenty-year-old?

**Answer**: $4.27$ tickets, roughly $4$.

