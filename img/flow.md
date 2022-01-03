
flowchart LR
	subgraph FLOW
	direction LR
		subgraph Instructor
			lmr[Main Repo]
			ls1[Student 1]
			ls2[Student 2]
			ls3[Student 3]
		end
		subgraph GitHub
			rs1[Student 1]
			rs2[Student 2]
			rs3[Student 3]
		end
		subgraph Users
			ss1[Student 1]
			ss2[Student 2]
			ss3[Student 3]
		end
	end
	
lmr --> ls1
lmr --> ls2
lmr --> ls3
ls1 -.-> rs1
rs1 -.-> ls1
ls2 -.-> rs2
rs2 -.-> ls2
ls3 -.-> rs3
rs3 -.-> ls3
rs1 -.-> ss1[Student 1]
rs2 -.-> ss2[Student 2]
rs3 -.-> ss3[Student 3]
ss1 -.-> rs1
ss2 -.-> rs2
ss3 -.-> rs3

classDef blue fill:#b3cde3,stroke:#386b94,stroke-width:2px;
classDef red fill:#fbb4ae,stroke:#c31909,stroke-width:2px;
classDef green fill:#ccebc5,stroke:#469834,stroke-width:2px;
classDef grey fill:#fff,stroke:#fff,stroke-width:2px,padding-bottom:2em;

class lmr,ls1,ls2,ls3 blue
class rs1,rs2,rs3 red
class ss1,ss2,ss3 green
class FLOW grey
