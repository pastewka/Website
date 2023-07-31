import json
import html
import re

import bibtexparser
from crossref.restful import Works


journal_map = {
	'molecular simulation': 'Mol. Sim.',
	'phys rev materials': 'Phys. Rev. Mater.',
	'mrs communications': 'MRS Comm.',
	'microfluidics and nanofluidics': 'Microfluid. Nanofluid.',
	'physical chemistry chemical physics': 'Phys. Chem. Chem. Phys.',
	'frontiers in physics': 'Front. Phys.',
	'frontiers in physics': 'Front. Physics',
	'front phys': 'Front. Physics',
	'communications in computational physics': 'Commun. Comput. Phys.',
	'new journal of physics': 'New J. Phys.',
	'microsystem technologies': 'Microsyst. Technol.',
	'ieee sensors journal': 'IEEE Sensors J.',
	'philosophical transactions of the royal society a: mathematical, physical and engineering sciences': 'Phil. Trans. R. Soc. A.',
	'the european physical journal special topics': 'Eur. Phys. J. Spec. Top.',
	'international journal for multiscale computational engineering': 'Int. J. Mult. Comp. Eng.',
	'international journal of modern physics c': 'Int. Mod. Phys. C',
	'physical review e': 'Phys. Rev. E',
	'physical review b': 'Phys. Rev. B',
	'physical review letters': 'Phys. Rev. Lett.',
	'semiconductor science and technology': 'Semicond. Sci. Technol.',
	'physica status solidi (b)': 'phys. stat. sol. (b)',
	'optical and quantum electronics': 'Opt. Quant. Electron.',
	'journal of microelectromechanical systems': 'J. Microelectromech. Syst.',
	'macromolecular theory and simulations': 'Macromol. Theory Simul.',
	'sensor letters': 'Sen. Lett.',
	'ieee transactions on computer-aided design of integrated circuits and systems': 'IEEE Trans. Comput.-Aided Des. Integr. Circuits Syst.',
	'tribology international': 'Tribol. Int.',
	'journal of the mechanics and physics of solids': 'J. Mech. Phys. Solids',
	'computer physics communications': 'Comput. Phys. Commun.',
	'mrs bulletin': 'MRS Bull.',
	'applied mathematics and computation': 'Appl. Math. Comput.',
	'the journal of chemical physics': 'J. Chem. Phys.',
	'mathematical and computer modelling of dynamical systems': 'Math. Comput. Model. Dyn. Syst.',
	'journal of the european ceramic society': 'J. Eur. Ceram. Soc.',
}

def normalize_journal(title):
	normalized_title = html.unescape(title).lower().replace('.', '')
	if normalized_title in journal_map:
		return journal_map[normalized_title]
	else:
		return title


def match_crossref(libentry, crossref, libkey, crkey, normalize=lambda x: html.unescape(x).lower(),
				   override=False):
	if crkey in crossref:
		crvalue = crossref[crkey]
		if isinstance(crvalue, list):
			if len(crvalue) != 1:
				print(f"    Crossref key '{crkey}' is list of length {len(crvalue)}")
				return
			crvalue, = crvalue

		if libkey in entry.fields_dict:
			libvalue_normalized = normalize(entry[libkey])
			crvalue_normalized = normalize(crvalue)
			if libvalue_normalized != crvalue_normalized:
				print(f"    WARNING: Mismatch for library key '{libkey}'/crossref key '{crkey}': {entry[libkey]} != {crvalue}")
				if override:
					print(f"    UPDATE: Setting library key '{libkey}' from crossref.")
					entry.set_field(bibtexparser.model.Field(libkey, crvalue))					
		else:
			print(f"    UPDATE: Setting library key '{libkey}' from crossref.")
			entry.set_field(bibtexparser.model.Field(libkey, crvalue))
	#else:
	#	if libkey not in entry.fields_dict:
	#		print(f"    WARNING: Library key '{libkey}' does not exist, but neither does crossref key '{crkey}'. Cannot obtain missing information.")


works = Works()

library = bibtexparser.parse_file('journals.bib')

for entry in library.entries:
	doi = None
	
	# Clean all fields
	for field in entry.fields:
		# Convert all keys to lowercase
		field.key = field.key.lower()
		# Strip multiple white spaces
		field.value = re.sub(r'\s+', ' ', field.value)

	# Normalize journals
	entry.set_field(bibtexparser.model.Field('journal', normalize_journal(entry['journal'])))

	print(f"---> {entry['title']} <---")
	# Warn if DOI is missing
	if 'doi' in entry.fields_dict:
		doi = entry['doi'].strip()
		if doi.startswith('http'):
			doi = doi.split('/')[-1].strip()
			entry['doi'] = doi
		if len(doi) == 0:
			doi = None

	if doi is None:
		print(f'    DOI missing! Cannot get Crossref information')
	else:
		#print(f'Looking up DOI {doi} via Crossref...')
		crossref = works.doi(doi)

		if crossref is None:
			print('Crossref did not find this paper!')
		else:
			match_crossref(entry, crossref, 'title', 'title',
				lambda x: x)
			match_crossref(entry, crossref, 'abstract', 'abstract',
				lambda x: x.replace('<jats:p>', '').replace('</jats:p>', ''))
			match_crossref(entry, crossref, 'journal', 'short-container-title',
				lambda x: normalize_journal(x).lower().replace('.', ''))  # ignore differences in dots
			match_crossref(entry, crossref, 'volume', 'volume', override=True)
			#match_crossref(entry, crossref, 'number', 'issue', override=True)
			match_crossref(entry, crossref, 'pages', 'article-number', override=True)
			match_crossref(entry, crossref, 'pages', 'page', override=True)

			if 'author' in crossref:
				author_str = ''
				for author in crossref['author']:
					if 'family' in author and 'given' in author:
						author_str += f"{author['family']}, {author['given']} and "
					else:
						print(f'    WARNING: Ignoring author {author}!')
				author_str = author_str[:-5]
				if entry['author'] != author_str:
					print(f"    WARNING: Author mismatch: {entry['author']} != {author_str}")
					#entry.set_field(bibtexparser.model.Field('author', author_str))	

bibtexparser.write_file('tmp.bib', library)