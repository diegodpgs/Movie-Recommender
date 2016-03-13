#coding: UTF-8
import urllib2
from oscars import *
import sys

def parseStars():
	mystars = open('my_stars.txt').read()
	mystars = mystars.split('\n')
	stars_dic = {}
	for ms in mystars:
		stars_dic[ms.split(';')[0]] = (float(ms.split(';')[1]),int(ms.split(';')[2]))
		
	
	return stars_dic
	
def getCast(movie_url, stars):
	actors = []
	movie_page	= urllib2.urlopen(movie_url).readlines()
	oscars = {}
	score_cast = []
	
	for index in xrange(len(movie_page)):
		if '- IMDb</title>' in movie_page[index]:
			print 'Score for %s' % (movie_page[index].split('- IMDb</title>')[0].split('>')[1])
			
		if '<span class="itemprop" itemprop="name">' in movie_page[index]:
			name = movie_page[index].split('<span class="itemprop" itemprop="name">')[1].split('<')[0]
			
			if '/name/' in movie_page[index-1]:
				url = movie_page[index-1].split('<a href="')[1].split('?ref')[0]
				oscars_star = getNameOscars('http://www.imdb.com/%s' % url)
				
				if oscars_star['name'] in stars and stars[oscars_star['name']][1]> 1:
					score_cast.append(stars[oscars_star['name']][0])
					
				if len(oscars_star['name']) > 1 and (oscars_star['won']+oscars_star['nominated']) > 0:
					if oscars_star['name'] not in oscars:
						oscars[oscars_star['name']] = (oscars_star['won'],oscars_star['nominated'])

	return (oscars,sum(score_cast)/max(len(score_cast),1))
	
	
	



cast,score_cast = getCast('http://www.imdb.com/title/%s/' % sys.argv[1],parseStars())

cast = zip(cast.values(),cast.keys())
cast.sort()


to = 0
tn = 0

for star in cast[::-1]:
	to += star[0][0]
	tn += star[0][1]
	print '%s has %d Oscars and %d Nominations' % (star[1].ljust(20),star[0][0],star[0][1])

print 'The Cast has a score of %1.2f ' % score_cast	
print 'Total of %d Oscars and %d Nominations\n\n' % (to,tn)



"""
Diegos-MacBook-Air:Recomender happyhour$ sh oscars.sh 
Score for Amor a Toda Prova (2011) 
The Cast has a score of 7.11 
Julianne Moore       has 1 Oscars and 4 Nominations
Marisa Tomei         has 1 Oscars and 2 Nominations
Steve Carell         has 0 Oscars and 1 Nominations
Ryan Gosling         has 0 Oscars and 1 Nominations
Emma Stone           has 0 Oscars and 1 Nominations
Total of 2 Oscars and 9 Nominations


Score for O Grande Hotel Budapeste (2014) 
The Cast has a score of 7.48 
Tilda Swinton        has 1 Oscars and 0 Nominations
F. Murray Abraham    has 1 Oscars and 0 Nominations
Adrien Brody         has 1 Oscars and 0 Nominations
Wes Anderson         has 0 Oscars and 6 Nominations
Edward Norton        has 0 Oscars and 3 Nominations
Willem Dafoe         has 0 Oscars and 2 Nominations
Tom Wilkinson        has 0 Oscars and 2 Nominations
Ralph Fiennes        has 0 Oscars and 2 Nominations
Jude Law             has 0 Oscars and 2 Nominations
Saoirse Ronan        has 0 Oscars and 1 Nominations
Jeff Goldblum        has 0 Oscars and 1 Nominations
Harvey Keitel        has 0 Oscars and 1 Nominations
Bill Murray          has 0 Oscars and 1 Nominations
Total of 3 Oscars and 21 Nominations


Score for Quero Ser John Malkovich (1999) 
The Cast has a score of 6.75 
Spike Jonze          has 1 Oscars and 3 Nominations
Charlie Kaufman      has 1 Oscars and 2 Nominations
Octavia Spencer      has 1 Oscars and 0 Nominations
John Malkovich       has 0 Oscars and 2 Nominations
Catherine Keener     has 0 Oscars and 2 Nominations
Total of 3 Oscars and 9 Nominations


Score for Adam (2009) 
The Cast has a score of 7.33 
Amy Irving           has 0 Oscars and 1 Nominations
Total of 0 Oscars and 1 Nominations


Score for Ed Wood (1994) 
The Cast has a score of 7.28 
Martin Landau        has 1 Oscars and 2 Nominations
Patricia Arquette    has 1 Oscars and 0 Nominations
Johnny Depp          has 0 Oscars and 3 Nominations
Tim Burton           has 0 Oscars and 2 Nominations
Bill Murray          has 0 Oscars and 1 Nominations
Total of 2 Oscars and 8 Nominations


Score for Quanto Mais Quente Melhor (1959) 
The Cast has a score of 0.00 
Billy Wilder         has 6 Oscars and 15 Nominations
Jack Lemmon          has 2 Oscars and 6 Nominations
I.A.L. Diamond       has 1 Oscars and 2 Nominations
Tony Curtis          has 0 Oscars and 1 Nominations
Total of 9 Oscars and 24 Nominations


Score for O Sétimo Selo (1957) 
The Cast has a score of 6.67 
Ingmar Bergman       has 0 Oscars and 9 Nominations
Max von Sydow        has 0 Oscars and 2 Nominations
Total of 0 Oscars and 11 Nominations


Score for A Onda (2008) 
The Cast has a score of 0.00 
Total of 0 Oscars and 0 Nominations


Score for Laranja Mecânica (1971) 
Stanley Kubrick      has 1 Oscars and 12 Nominations
The Cast has a score of 0.00 
Total of 1 Oscars and 12 Nominations


Score for O Homem da Terra (2007) 
The Cast has a score of 0.00 
Total of 0 Oscars and 0 Nominations


Diegos-MacBook-Air:Recomender happyhour$ sh oscars.sh 
Score for Amor a Toda Prova (2011) 
Julianne Moore       has 1 Oscars and 4 Nominations
Marisa Tomei         has 1 Oscars and 2 Nominations
Steve Carell         has 0 Oscars and 1 Nominations
Ryan Gosling         has 0 Oscars and 1 Nominations
Emma Stone           has 0 Oscars and 1 Nominations
The Cast has a score of 7.11 
Total of 2 Oscars and 9 Nominations


Score for O Grande Hotel Budapeste (2014) 
Tilda Swinton        has 1 Oscars and 0 Nominations
F. Murray Abraham    has 1 Oscars and 0 Nominations
Adrien Brody         has 1 Oscars and 0 Nominations
Wes Anderson         has 0 Oscars and 6 Nominations
Edward Norton        has 0 Oscars and 3 Nominations
Willem Dafoe         has 0 Oscars and 2 Nominations
Tom Wilkinson        has 0 Oscars and 2 Nominations
Ralph Fiennes        has 0 Oscars and 2 Nominations
Jude Law             has 0 Oscars and 2 Nominations
Saoirse Ronan        has 0 Oscars and 1 Nominations
Jeff Goldblum        has 0 Oscars and 1 Nominations
Harvey Keitel        has 0 Oscars and 1 Nominations
Bill Murray          has 0 Oscars and 1 Nominations
The Cast has a score of 7.48 
Total of 3 Oscars and 21 Nominations


Score for Quero Ser John Malkovich (1999) 
Spike Jonze          has 1 Oscars and 3 Nominations
Charlie Kaufman      has 1 Oscars and 2 Nominations
Octavia Spencer      has 1 Oscars and 0 Nominations
John Malkovich       has 0 Oscars and 2 Nominations
Catherine Keener     has 0 Oscars and 2 Nominations
The Cast has a score of 6.75 
Total of 3 Oscars and 9 Nominations


Score for Adam (2009) 
Amy Irving           has 0 Oscars and 1 Nominations
The Cast has a score of 7.33 
Total of 0 Oscars and 1 Nominations


Score for Ed Wood (1994) 
Martin Landau        has 1 Oscars and 2 Nominations
Patricia Arquette    has 1 Oscars and 0 Nominations
Johnny Depp          has 0 Oscars and 3 Nominations
Tim Burton           has 0 Oscars and 2 Nominations
Bill Murray          has 0 Oscars and 1 Nominations
The Cast has a score of 7.28 
Total of 2 Oscars and 8 Nominations


Score for Quanto Mais Quente Melhor (1959) 
Billy Wilder         has 6 Oscars and 15 Nominations
Jack Lemmon          has 2 Oscars and 6 Nominations
I.A.L. Diamond       has 1 Oscars and 2 Nominations
Tony Curtis          has 0 Oscars and 1 Nominations
The Cast has a score of 0.00 
Total of 9 Oscars and 24 Nominations


Score for O Sétimo Selo (1957) 
Ingmar Bergman       has 0 Oscars and 9 Nominations
Max von Sydow        has 0 Oscars and 2 Nominations
The Cast has a score of 6.67 
Total of 0 Oscars and 11 Nominations


Score for A Onda (2008) 
The Cast has a score of 0.00 
Total of 0 Oscars and 0 Nominations


Score for Laranja Mecânica (1971) 
Stanley Kubrick      has 1 Oscars and 12 Nominations
The Cast has a score of 0.00 
Total of 1 Oscars and 12 Nominations


Score for O Homem da Terra (2007) 
The Cast has a score of 0.00 
Total of 0 Oscars and 0 Nominations


Score for Donnie Darko (2001) 
Mary McDonnell       has 0 Oscars and 2 Nominations
Maggie Gyllenhaal    has 0 Oscars and 1 Nominations
Jake Gyllenhaal      has 0 Oscars and 1 Nominations
The Cast has a score of 7.33 
Total of 0 Oscars and 4 Nominations


Score for O Grande Lebowski (1998) 
Joel Coen            has 4 Oscars and 9 Nominations
Ethan Coen           has 4 Oscars and 9 Nominations
Jeff Bridges         has 1 Oscars and 5 Nominations
Julianne Moore       has 1 Oscars and 4 Nominations
Philip Seymour Hoffman has 1 Oscars and 3 Nominations
The Cast has a score of 6.37 
Total of 11 Oscars and 30 Nominations


Score for Coração Valente (1995) 
Mel Gibson           has 2 Oscars and 0 Nominations
Randall Wallace      has 0 Oscars and 1 Nominations
The Cast has a score of 6.58 
Total of 2 Oscars and 1 Nominations


Score for A Origem (2010) 
Michael Caine        has 2 Oscars and 4 Nominations
Marion Cotillard     has 1 Oscars and 1 Nominations
Leonardo DiCaprio    has 0 Oscars and 5 Nominations
Christopher Nolan    has 0 Oscars and 3 Nominations
Tom Berenger         has 0 Oscars and 1 Nominations
Pete Postlethwaite   has 0 Oscars and 1 Nominations
Ken Watanabe         has 0 Oscars and 1 Nominations
Ellen Page           has 0 Oscars and 1 Nominations
The Cast has a score of 8.43 
Total of 3 Oscars and 17 Nominations


Score for O Tesouro da Sierra Madre (1948) 
John Huston          has 2 Oscars and 13 Nominations
Walter Huston        has 1 Oscars and 3 Nominations
Humphrey Bogart      has 1 Oscars and 2 Nominations
The Cast has a score of 0.00 
Total of 4 Oscars and 18 Nominations


Score for A Malvada (1950) 
Joseph L. Mankiewicz has 4 Oscars and 6 Nominations
Bette Davis          has 2 Oscars and 9 Nominations
Celeste Holm         has 1 Oscars and 2 Nominations
Anne Baxter          has 1 Oscars and 1 Nominations
George Sanders       has 1 Oscars and 0 Nominations
Thelma Ritter        has 0 Oscars and 6 Nominations
The Cast has a score of 0.00 
Total of 9 Oscars and 24 Nominations


Score for No Limite do Amanhã (2014) 
Christopher McQuarrie has 1 Oscars and 0 Nominations
Tom Cruise           has 0 Oscars and 3 Nominations
The Cast has a score of 7.25 
Total of 1 Oscars and 3 Nominations


Score for Família do Bagulho (2013) 
The Cast has a score of 6.33 
Total of 0 Oscars and 0 Nominations


Score for Serenity: A Luta Pelo Amanhã (2005) 
Joss Whedon          has 0 Oscars and 1 Nominations
Chiwetel Ejiofor     has 0 Oscars and 1 Nominations
The Cast has a score of 7.00 
Total of 0 Oscars and 2 Nominations


Score for O Lado Bom da Vida (2012) 
Robert De Niro       has 2 Oscars and 5 Nominations
Jennifer Lawrence    has 1 Oscars and 2 Nominations
David O. Russell     has 0 Oscars and 5 Nominations
Bradley Cooper       has 0 Oscars and 4 Nominations
Jacki Weaver         has 0 Oscars and 2 Nominations
The Cast has a score of 7.27 
Total of 3 Oscars and 18 Nominations


Score for Aconteceu Naquela Noite (1934) 
Frank Capra          has 3 Oscars and 3 Nominations
Robert Riskin        has 1 Oscars and 4 Nominations
Claudette Colbert    has 1 Oscars and 2 Nominations
Clark Gable          has 1 Oscars and 2 Nominations
The Cast has a score of 0.00 
Total of 6 Oscars and 11 Nominations


Score for Simplesmente Amor (2003) 
Emma Thompson        has 2 Oscars and 3 Nominations
Colin Firth          has 1 Oscars and 1 Nominations
Keira Knightley      has 0 Oscars and 2 Nominations
Richard Curtis       has 0 Oscars and 1 Nominations
Liam Neeson          has 0 Oscars and 1 Nominations
Chiwetel Ejiofor     has 0 Oscars and 1 Nominations
The Cast has a score of 7.42 
Total of 3 Oscars and 9 Nominations


Score for A Separação (2011) 
Asghar Farhadi       has 0 Oscars and 1 Nominations
The Cast has a score of 0.00 
Total of 0 Oscars and 1 Nominations


Score for Stardust: O Mistério da Estrela (2007) 
Peter O'Toole        has 0 Oscars and 8 Nominations
Ian McKellen         has 0 Oscars and 2 Nominations
The Cast has a score of 8.33 
Total of 0 Oscars and 10 Nominations


Score for Dublê de Anjo (2006) 
Dan Gilroy           has 0 Oscars and 1 Nominations
The Cast has a score of 0.00 
Total of 0 Oscars and 1 Nominations


Score for Não Me Abandone Jamais (2010) 
Keira Knightley      has 0 Oscars and 2 Nominations
Sally Hawkins        has 0 Oscars and 1 Nominations
Carey Mulligan       has 0 Oscars and 1 Nominations
The Cast has a score of 7.55 
Total of 0 Oscars and 4 Nominations


Diegos-MacBook-Air:Recomender happyhour$ 

"""
	

			