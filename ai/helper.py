def transformData(str):
    first_string = str.find('"fd-f1">')
    second_string = str.find('<aside class="f-vacancylist-rightwrap-outer">')
    etap_1 = str[first_string + 8:second_string]
    h1 = etap_1.find('<dd>')
    h2 = etap_1.find('Следующая')
    t1 = etap_1[h1:h2 + 9]
    etap_2 = etap_1.replace(t1, '').replace('Горячая вакансия поднятая работодателем вверх списка', '')
    etap_2 = etap_2.replace("href='/company", "target=\"_blank\" href='https://rabota.ua/company")
    etap_2 = etap_2.replace("href=\"/company", "target=\"_blank\" href=\"https://rabota.ua/company")
    h3 = etap_2.find('<ul class="f-reset-list"')
    h4 = etap_2.find('</ul>')
    etap_2 = etap_2.replace(etap_2[h3:h4], '')
    etap_2 = etap_2.replace("Ведущие работодатели", '')
    h5 = etap_2.find('<noindex>')
    h6 = etap_2.find('</noindex>')
    etap_2 = etap_2.replace(etap_2[h5:h6], '')
    return etap_2