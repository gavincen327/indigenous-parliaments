# Extracting CSVs from the Nunavut Hansard PDFs
The Hansards are at the following link: https://assembly.nu.ca/hansard
They need to be downloaded and parsed into a CSV with two columns: speech, speaker.
This is done by running get_nunavut_hansards.py as follows:


python get_nunavut_hansards.py 20100331 where the passed integer is the date of the hansard. 


The problems are as follows:
1. How to get all of the hansards down when the format of the URL changes frequently? Maybe the function should cycle through 5-6 observed formats.
2. The punctuation was stripped in the code but it is better to re-add it.
3. The texts below are appearing buggy:


Nunavut 20090324:


"Thank you Mr Speaker The fill station was one of the projects that we approved during the supplementary appropriations last week Once the new fiscal year starts the department plans to get the request for proposals out   Hon Hunter Tootoo: Thank you Mr Speaker As the member pointed out yes there were issues that happened prior to me being the housing minister but if he could clarify what particular issues hes talking about I would be able to respond to him   Tuesday March 24 2009   There are all kinds of housing issues that have gone on over the last while all over the territory So maybe if he could clarify specifically what issue he was talking about I would be more than happy to respond to him Thank you Mr Speaker"


Note that Hon Hunter Too too's speach is squished into there. The header date is appearing in there but I believe that I already resolved this issue.


Nunavut 20141027:


"The Minister's responses seem to be missing in this exchange. It's three speech acts from Ms. Angnakak in a row but it seems like there were other responses in between.


8	Ms Angnakak	 Thank you Mr Speaker I would like to direct my question to the Minister of Family Services Mr Speaker after our hearings with the Auditor General of Canada to discuss the delivery of child and family services across Nunavut it was clear that there are a number of gaps in service delivery Can the minister clarify whether her department will be allocating any additional funding or resources to implement the Child and Family Services Act?  
9	Ms Angnakak	 Thank you Mr Speaker I recognize that there are challenges in hiring skilled and trained social workers in the Nunavut communities Can the minister provide an update on what efforts are being made in the area? Thank you Mr Speaker 
10	Ms Angnakak	 Thank you Mr Speaker I realize that the minister just said that theres going to be a workshop and some training opportunities coming up in the near future but Im wondering if you can describe what kind of training opportunities you have now within the department and whether or not youre going to be allocating any additional resources to ensure that more training opportunities are made available on a consistent basis Thank you Mr Speaker" 

