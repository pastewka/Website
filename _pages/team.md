---
layout: page
permalink: /team/
title: team
description: "<em>I can’t believe what a bunch of nerds we are.</em> — Michael"
nav: true
nav_order: 3
---

<ul class="team">
	
	{% assign last_role = '' %}
	{% for person in site.data.team %}
	    {% if person.role != last_role %}
	       <h2><span>{{ person.role }}</span></h2>
	    {% endif %}
		<li>
            {% if person.role == 'alumni' %}
                <div class="image-placeholder"></div>
            {% else %}
				<div class="square-image">
				    {% if person.image_path %}
					    <div class="circular-inset">
		                	<img src="/assets/img/{{ person.image_path }}" alt="{{ person.name }}"/>
		                </div>
		            {% else %}
	                	<div class="circle"></div>
		            {% endif %}
	            </div>
            {% endif %}
			<h5 class="name">{{ person.title }} {{ person.name }}</h5>
		    {% if person.function %}
				<div class="role">{{ person.function }}</div>
            {% endif %}
            {% if person.email %}
			<small>
				<div class="role"><i class="fa fa-envelope" aria-hidden="true"></i> <a href="mailto:{{ person.email }}">{{ person.email }}</a></div>
			</small>
			{% endif %}
			{% if person.website %}
				<small>
					<div class="role"><i class="fa fa-globe" aria-hidden="true"></i> <a href="{{ person.website }}">{{ person.website }}</a></div>
				</small>
			{% endif %}
			{% if person.current %}
			    <div class="current">{{ person.current }}</div>
			{% endif %}
			{% if person.education %}
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
		{% assign last_role = person.role %}
	{% endfor %}

</ul>
