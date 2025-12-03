Data used for training comes directly from the EternaFold fasta files, which are included, and for testing are those not included in Eternafold fasta files . I should separate this from the training NB . (Create a new data splitting NB ) .


From the HWS paper : "We used riboswitches designed by the automated RiboLogic34 algorithm for riboswitch training data (n = 1,295)." So check that there are 1,295 values in the ribologic training data. 


To ensure a rigorous separation of training and test data, each test dataset was filtered for sequence similarity to all training data at 80% using a windowed Levenshtein metric (Methods). 

Test sets for chemical mapping and riboswitch data came from completely different experimental rounds than those used in training to avoid learning experiment-specific biases.

 z-score ranking over nine riboswitch test sets for riboswitch KMS2 prediction filtered to contain constructs with <80% sequence similarity to all training data, n = 9 datasets with 4,018 independent constructs total. 
 
 
 Riboswitch data
We partitioned the RiboLogic dataset into our training, holdout and test sets due to the high signal-noise ratio and diversity of structures, subdividing the riboswitches so that each split contained identical fractions of FMN-, theophylline- and tryptophan-responsive riboswitches. This left the rest of the Eterna riboswitch rounds as test sets (Extended Data Fig. 3d). 
