
graph LR	
subgraph Instructor
lmr[Master Repo] --> ls1[Student 1]
lmr --> ls2[Student 2]
lmr --> ls3[Student 3]
end

classDef blue fill:#b3cde3,stroke:#386b94,stroke-width:2px;
classDef red fill:#fbb4ae,stroke:#c31909,stroke-width:2px;
classDef green fill:#ccebc5,stroke:#469834,stroke-width:2px;

class lmr,ls1,ls2,ls3 blue
class rs1,rs2,rs3 red
class ss1,ss2,ss3 green