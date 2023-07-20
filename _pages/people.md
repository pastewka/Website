---
layout: page
permalink: /people/
title: people
description: Members of the group.
nav: true
nav_order: 2
---

<ul class="staff">
	{% for person in site.people %}
		<li>
			<div class="square-image">
                <img src="/assets/img/{{ person.image_path }}" alt="{{ person.name }}"/>
            </div>
			<div class="name">{{ person.title }} {{ person.name }}</div>
			<div class="role">{{ person.role }}</div>
			<div class="degree">{{ person.degree }}</div>
		</li>
	{% endfor %}
</ul>
