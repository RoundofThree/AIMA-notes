# Tutorial 6 ─ Unsupervised learning

## Cluster distance

Calculate the Manhattan distance between the following 5-dimensional data points. 

- $x_1 = [1,3,4,5,2]​$
- $x_2 = [1,4,2,3,2] ​$

>Manhattan distance: $\Sigma_{i=1}^{d}|x_i - y_i|$
>Euclidean distance: $\sqrt{\Sigma_{i=1}^{d}(x_i-y_i)^2}$

So, the solution is $|1-1|+|3-4|+|4-2|+|5-3|+|2-2|=5$

## K-means clustering

- Using the K-means algorithm ($K = 3$), cluster the following eight points, using Euclidean distance as the distance metric. 
- Suppose initially we assign A1, A4 and A7 as the centroids. 

### Iteration 1

|  Point 			|  Centroid 1 (2, 10) 	| Centroid 2  (5, 8)	| Centroid 3  (1, 2)	| Cluster 	|
|---					|---								|---							|---							|--- 			|
|  A1 (2, 10) 	| $0$						| $3^2+2^2=13$| $1^2+8^2=65$|  1			|
|  A2 (2, 5) 		| $0^2+5^2=25$ 			| $3^2+3^2=18$| $1^2+3^2=10$|  3			|	
|  A3 (8, 4) 		| $6^2 + 6^2=72$	| $3^2+4^2=25$| $7^2+2^2=53$| 2			|
|  A4 (5, 8)		| $3^2+2^2=13$	| $0$					| $4^2+6^2=52$| 2			|				
|  A5 (7, 5)		| $5^2+5^2=50$	| $2^2+3^2=13$| $6^2+3^2=45$| 2			|  								
|  A6 (6, 4)		| $4^2+6^2=52$	| $1^2+4^2=17$| $5^2+2^2=29$| 2			|  							
|  A7 (1, 2)  		| $1^2+8^2=65$	| $4^2+6^2=52$| $0$					| 3 			|							
|   A8 (4, 9)		| $2^2+1^2=5$ 		| $1^2+1^2=2$	| $3^2+7^2=58$| 2 			|  		
- What are the three cluster centroids after the first round of execution (iteration)?

We take the mean of x and y for all the points in the same cluster. 
Centroid 1 (2, 10), Centroid 2 (6, 6), Centroid 3 (1.5, 3.5)

- What are the three final clusters? 

After the 4th iteration, Centroid 1 (3.67, 9), Centroid 2 (7, 4.33), Centroid (1.5, 3.5). 

## Hierarchical clustering

Using hierarchical clustering, cluster and draw the dendogram of the following points, first, using single linkage and, then complete linkage. 

|       | A  | B  | C | D | E |
|   -   |  - | -  | - | - | - |
| **A** | 0  |    |   |   |   |
| **B** | 9  | 0  |   |   |   |
| **C** | 3  | 7  | 0 |   |   |
| **D** | 6  | 5  | 9 | 0 |   |
| **E** | 11 | 10 | 2 | 8 | 0 |

### Single linkage
1. **C** and **E**

|       | A  | B  | C, E | D |
|   -   |  - | -  | - | - |
| **A** | 0  |    |   |   |
| **B** | 9  | 0  |   |   |
| **C, E** | 3  | 7  | 0 |   |
| **D** | 6  | 5  | 8 | 0 |

2. **A** and **C, E**

|       | A, C, E  | B  | D |
|   -   |  - | -  | - |
| **A, C, E** | 0  |    |   |
| **B** | 7  | 0  |   |
| **D** | 6  | 5  | 0 |

3. **B** and **D**

|       | A, C, E  | B, D  |
|   -   |  - | -  |
| **A, C, E** | 0  |    |
| **B, D** | 6  | 0  |

4. **A, C, E** and **B, D**

### Complete linkage
1. **C** and **E**

|       | A  | B  | C, E | D |
|   -   |  - | -  | - | - |
| **A** | 0  |    |   |   |
| **B** | 9  | 0  |   |   |
| **C, E** | 11  | 10  | 0 |   |
| **D** | 6  | 5  | 9 | 0 |

2. **B** and **D**

|       | A  | B, D  | C, E |
|   -   |  - | -  | - |
| **A** | 0  |    |   |
| **B, D** | 9  | 0  |   |
| **C, E** | 11  | 10  | 0 |

3. **A** and **B, D**

|       | A, B, D  | C, E |
|   -   |  - | -  |
| **A, B, D** | 0  | 0  |
| **C, E** | 11  | 0  |

4. **A, B, D** and **C, E**

## Association rules

Consider the supermarket transactions shown in the table.

|Transaction ID|Products Bought|
|---|---|
|1|$\{A, D, E\}$|
|2|$\{A, B, C, E\}$|
|3|$\{A, B, D, E\}$|
|4|$\{A, C, D, E\}$|
|5|$\{B, C, E\}$|
|6|$\{B, D, E\}$|
|7|$\{C, D\}$|
|8|$\{A, B, C\}$|
|9|$\{A, D, E\}$|
|10|$\{A, B, E\}$|

### Support
Compute the support for item-sets:

- $\{E\}:\frac{8}{10}=0.8$​
-  $\{B, D\}:\frac{2}{10}=0.2$​ 
-  $\{B, D, E\}:\frac{2}{10}=0.2$

### Confidence
Compute the confidence for association rules:

-  $\{B,D\} \to \{E\} = \frac{support(\{B,D,E\})}{support(\{B,D\})} = \frac{0.2}{0.2}=1$
- $\{E\} \to \{B, D\} = \frac{support(\{B,D,E\})}{support(\{E\})} = \frac{0.2}{0.8}=0.25$