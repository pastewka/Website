import json
import html
import re

import bibtexparser
from crossref.restful import Works


journal_map = {
	'molecular simulation': 'Mol. Sim.',
	'phys rev materials': 'Phys. Rev. Mater.',
}

def mangle_journal(title):
	normalized_title = html.unescape(title).lower().replace('.', '')
	if normalized_title in journal_map:
		return journal_map[normalized_title].lower().replace('.', '')
	else:
		return normalized_title


def match_crossref(libentry, crossref, libkey, crkey, normalize=lambda x: html.unescape(x).lower()):
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
		else:
			print(f"    UPDATE: Setting library key '{libkey}' from crossref.")
			entry.set_field(bibtexparser.model.Field(libkey, crvalue))
	else:
		if libkey not in entry.fields_dict:
			print(f"    WARNING: Library key '{libkey}' does not exist, but neither does crossref key '{crkey}'. Cannot obtain missing information.")


works = Works()

library = bibtexparser.parse_file('journals.bib')

for entry in library.entries:
	for field in entry.fields:
		# Convert all keys to lowercase
		field.key = field.key.lower()
		# Strip multiple white spaces
		field.value = re.sub(r'\s+', ' ', field.value)
	print(f"---> {entry['title']} <---")
	# Warn if DOI is missing
	if 'doi' not in entry.fields_dict:
		doi = None
	else:
		doi = entry['doi'].strip()
		if doi.startswith('http'):
			doi = doi.split('/')[-1].strip()
			entry['doi'] = doi
		if doi is None or len(doi) == 0:
			doi = None

	if doi is None:
		print(f'    DOI missing! Cannot get Crossref information')
	else:
		#print(f'Looking up DOI {doi} via Crossref...')
		crossref = works.doi(doi)

		if crossref is None:
			print('Crossref did not find this paper!')
		else:
			match_crossref(entry, crossref, 'title', 'title')
			match_crossref(entry, crossref, 'abstract', 'abstract',
				lambda x: x.replace('<jats:p>', '').replace('</jats:p>', ''))
			match_crossref(entry, crossref, 'journal', 'short-container-title',
				mangle_journal)  # ignore differences in dots
			match_crossref(entry, crossref, 'volume', 'volume')
			match_crossref(entry, crossref, 'number', 'issue')
			match_crossref(entry, crossref, 'pages', 'article-number')

			if 'author' in crossref:
				author_str = ''
				for author in crossref['author']:
					author_str += f"{author['family']}, {author['given']} and "
				author_str = author_str[:-5]
				if entry['author'] != author_str:
					print(f"    UPDATE: Author mismatch: {entry['author']} !=  {author_str}")

bibtexparser.write_file('tmp.bib', library)