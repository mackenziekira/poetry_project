love = PoemSubject.query.filter_by(subject_id = 40).all()
love_poems = []
for s in love:
    love_poems.append(s.poem_id)

nature = PoemSubject.query.filter_by(subject_id = 29).all()
nature_poems = []
for s in nature:
    nature_poems.append(s.poem_id)

social = PoemSubject.query.filter_by(subject_id = 263).all()
social_poems = []
for s in social:
    social_poems.append(s.poem_id)

politics = PoemSubject.query.filter_by(subject_id = 16).all()
politic_poems = []
for s in social:
    politic_poems.append(s.poem_id)

poem_ids = love_poems + social_poems + nature_poems + politic_poems
poem_ids = set(poem_ids)

text = []
for poem in poem_ids:
    p = Poem.query.get(poem)
    text.append(p.body)