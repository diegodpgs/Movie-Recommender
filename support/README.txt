1 - Download the srt file from http://www.opensubtitles.org/ in english language
2 - Rename the str file using the title code of the movie
In the following format
name_of_movie_titlecode.srt
Inside.Out.2015.720p.BluRay.x264-SPARKS -> inside_out_tt2096673.srt

3 - copie the files to the folder original_data_new/SRT/new
  
4 - run parse_srt.py
	once it come from the parsed file, it doesn't need cut words that has less than 2 times
	the function parser.applyThreshold remove words that appear less than twice times.
	when the amount of files are small (less than 40) use the vocabulary_srt.voc
		the file vocabulary_srt.voc have to be update once a year.
			IF that file doesn't exist, then
				run the code compute_vocabulary.py
				example: python compute_vocabulary.py parsed_data/SRT vocabulary_srt.voc

3 - run get_reviews
4 - run parse_reviews
	once it come from the parsed file, it doesn't need cut words that has less than 2 times
	the function parser.applyThreshold remove words that appear less than twice times.
	when the amount of files are small (less than 40) use the vocabulary_review.voc
		the file vocabulary_review.voc have to be update once a year.
			IF that file doesn't exist, then
				run the code compute_vocabulary.py
				example: python compute_vocabulary.py parsed_data/Review vocabulary_review.voc
5 - run get_tags
6 - run parse_tags
7 - run bayes
parei aqui
#run run.py
#AttributeError: 'NaiveBayes' object has no attribute 'p_tk_in_c'
#resolver o problema de valores altos
8 - run testa



NEXT STEP : Clean the code