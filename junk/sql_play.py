select * from ts_stat('select tsv from poems') order by nentry desc, ndoc desc, word
;

^most frequent words in a document collection^
https://www.postgresql.org/docs/8.3/static/textsearch-features.html



        ^ts_headline code


Angular? subjects page
D3 vis of something?
incorporate displacy??
practice w machine learning
TESTING

represent meta groupings (d3?)
isolate sentences???
practice with jupyter, machine learning, where to go next w project??

for position information, split tsv column of returned entries into dicts and find position for lexeme of searched term?

    


    locations = dict((k.strip('\''), int(v.replace(',', ''))) for k,v in (x.split(':') for x in b.split()))




    SELECT 
    p.*, 
    ts_headline(body, q) AS headline, 
    a.name, 
    r.region_name, 
    s.subject_name 
INTO TEMP TABLE 
    temporary 
FROM poems p
    LEFT JOIN authors a 
        USING (author_id) 
    LEFT JOIN regions r 
        USING(region_id) 
    LEFT JOIN poems_subjects ps 
        USING (poem_id) 
    LEFT JOIN subjects s 
        USING (subject_id)
    , to_tsquery('kiss') q 
WHERE q @@ tsv