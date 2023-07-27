---
layout: page
permalink: /team/
title: team
description: "<em>I can’t believe what a bunch of nerds we are.</em> — Michael"
nav: true
nav_order: 2
---

<ul class="team">
	
	{% for person in site.data.team %}
		<li>
			<div class="square-image">
                <img src="/assets/img/{{ person.image_path }}" alt="{{ person.name }}"/>
            </div>
			<h5>{{ person.title }} {{ person.name }}</h5>
			<div class="role">{{ person.role }}</div>
			<small>
				<div class="role"><a href="mailto:{{ person.email }}">{{ person.email }}</a></div>
			</small>
			{% if person.education %}
			    <h5 class="subsection">Education</h5>
				{% for degree in person.education %}
					<div class="degree">{{ degree }}</div>
				{% endfor %}
			{% endif %}
			{% if person.identifiers %}
			    <h5 class="subsection">Identifiers</h5>
			    <div>
					{% if person.identifiers.orcid %}
						<span class="identifier">
							<img decoding="async" loading="lazy" width="16" height="16" style="width: 16px;" src="https://info.orcid.org/wp-content/uploads/2020/12/orcid_16x16.gif">
							<a href="https://orcid.org/{{ person.identifiers.orcid }}">{{ person.identifiers.orcid }}</a>
						</span>
					{% endif %}
					{% if person.identifiers.google %}
						<span class="identifier">
							<img decoding="async" loading="lazy" width="16" height="16" class="wp-image-9646" style="width: 16px;" src="/assets/svg/google-scholar.svg">
							<a href="https://scholar.google.de/citations?user={{ person.identifiers.google }}">{{ person.identifiers.google }}</a>
						</span>
					{% endif %}
					{% if person.identifiers.github %}
						<span class="identifier">
							<img decoding="async" loading="lazy" width="16" height="16" class="wp-image-9646" style="width: 16px;" src="/assets/svg/github-mark.svg">
							<a href="https://github.com/{{ person.identifiers.github }}">{{ person.identifiers.github }}</a>
						</span>
					{% endif %}
					{% if person.identifiers.gitlab %}
						<span class="identifier">
							<img decoding="async" loading="lazy" width="16" height="16" class="wp-image-9646" style="width: 16px;" src="/assets/svg/gitlab-logo-500.svg">
							<a href="https://gitlab.com/{{ person.identifiers.gitlab }}">{{ person.identifiers.gitlab }}</a>
						</span>
					{% endif %}
				</div>
			{% endif %}
		</li>
	{% endfor %}

</ul>
