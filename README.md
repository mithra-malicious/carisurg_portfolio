# carisurg_portfolio
Welcome to my clinical data analytics portfolio project. This repository contains end-to-end data pipelines developed to process, clean, and visualize electronic health records (EHR) from Mercer General Hospital's Emergency Department Triage System.
The primary objective of these foundational workflows is to convert highly chaotic, human-entered triage tracking data into an analytical-grade dataset suitable for clinical predictive modeling and operational auditing.
# Clone the repository
git clone https://github.com/mithra_malicious/carisurg-portfolio.git
cd carisurg-portfolio
Install required packages
pip install pandas numpy matplotlib jupyter
python -m notebook

# Tutorial 1: 
The initial phase of the data pipeline focuses on cleaning and standardizing the demographic variables recorded during patient intake. Human operators frequently log entry parameters using highly inconsistent formats, creating structural gaps that prevent automated software engines from sorting or filtering records correctly. To resolve this friction, an automated script isolates the column and targets variations in capitalization and spacing to establish a reliable baseline.
- First, the pipeline executes a string conversion technique that forces all mixed entry types into a uniform textual format so that numbers and letters can be processed under a single set of rules.
- Second, case-crushing and whitespace stripping mechanisms are applied to eliminate hidden formatting traps, such as inconsistent capitalization or accidental spaces added during frantic data entry.
- Third, the script runs the standardized data through a strict key-value translation map that shifts diverse text categories into clean binary indicators, creating a stable layout ready for analytical processing.
# Tutorial 2: 
The second phase of the architecture shifts toward advanced numerical auditing designed to evaluate the physiological reality of the patient files. In medical informatics, data points can easily be mathematically valid while remaining entirely impossible from a clinical standpoint due to keyboard typos or sensor errors. The engineered pipeline monitors incoming vital signs against strict physiological constraints to ensure that corrupted entries are caught and handled safely without breaking the system execution.
- First, a forced numeric conversion protocol searches the vital columns and automatically coerces text artifacts or entry mistakes into missing value markers to keep the program from crashing.
- Second, a boundary evaluation mask maps every row against logical medical thresholds for vital parameters to isolate ad purge extreme data spikes that do not match living human ranges.
- Third, an imputation engine identifies the remaining empty cells and populates them using historical column medians rather than mean averages, which strategically insulates the dataset against statistical skewing.
# Tutorial 3
The final phase of the framework moves from data engineering into diagnostic visual communication using specialized plotting libraries. Once the underlying data is scrubbed of structural noise and impossible variables, raw terminal arrays are translated into high-impact graphical interfaces that surface operational insight at a glance. These visual steps allow clinical teams to audit emergency room trends and detect patient care volumes interactively.
- First, the framework renders distribution histograms that group patient vitals into distinct columns, allowing supervisors to see the immediate spread and frequency of incoming cases.
- Second, a dedicated axis marking protocol overlays explicit medical reference lines onto the plots to clearly emphasize critical diagnostic thresholds, such as a definitive marker for an active fever.
- Third, two-variable scatter plots map the direct relationship between overlapping vital indicators to isolate physiological correlation trends and clusters across the active triage cohort.
