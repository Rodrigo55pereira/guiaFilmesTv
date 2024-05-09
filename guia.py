import requests
import re
from bs4 import BeautifulSoup

# numero de canais da tv
channels = {
    "A&E": 12,
    "AMC": 4,
    "AXN": 10,
    "CANAL BRASIL": 45,
    "CINEMAX": 76,
    "DISNEY CHANNEL": 104,
    "FX": 137,
    "HBO": 164,
    "HBO 2": 160,
    "HBO FAMILY": 163,
    "HBO SIGNATURE": 170,
    "MEGAPIX": 194,
    "PARAMOUNT": 225,
    "PRIME BOX BRASIL": 254,
    "SONY": 66,
    "SPACE": 331,
    "STAR HITS": 342,
    "STUDIO UNIVERSAL": 343,
    "SYFY": 0,
    "TBS": 0,
    "TCM": 370,
    "TELECINE ACTION": 348,
    "TELECINE CULT": 350,
    "TELECINE FUN": 352,
    "TELECINE PIPOCA": 354,
    "TELECINE PREMIUM": 356,
    "TELECINE TOUCH": 358,
    "TNT": 373,
    "UNIVERSAL CHANNEL": 440,
    "WARNER TV": 447
}


def get_number_channel(channel):
    return channels.get(channel)


def guide_movie_channel():
    link = "https://guiadefilmes.com.br"

    # Defina um cabeçalho do User-Agent para simular uma solicitação de navegador
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    req = requests.get(link, headers=headers)
    page = BeautifulSoup(req.text, "html.parser")
    ul_page = page.find("ul", class_="collection")
    channel_list = []

    for li in ul_page.find_all("li", class_="collection-item avatar"):
        # Inicializo o dicionário para armazenar informações do filme
        channel_info = {}

        # Pega nome do canal
        title = li.find("span", class_="title")
        if title:
            title_text = title.text
            channel_info['movie_channel'] = title.text.strip().upper()

        # Pega o número do canal
        channel_info['movie_channel_number'] = get_number_channel(title.text.strip().upper())

        # Pega imagem do canal
        img = li.find("img", class_="circle")
        if img and img.has_attr("src"):
            if title.text.strip().upper() == "STAR HITS":
                channel_info["img_movie_channel"] = "https://telaviva.com.br/wp-content/uploads/2021/02/STARCHANNEL.jpg"
            elif title.text.strip().upper() == "DISNEY CHANNEL":
                channel_info["img_movie_channel"] = "https://static.wikia.nocookie.net/disney-wik/images/8/8a/Disney_Channel.jpg"
            else:
                channel_info["img_movie_channel"] = img['src']

        # Pega hora inicial do filme
        strong_tags = li.find("strong")
        if strong_tags is not None:
            time_init_movie = re.search(r'\b\d{1,2}:\d{2}\b', strong_tags.get_text())
            channel_info['time_init_movie'] = time_init_movie.group()

        # Pega titulo inicial do filme
        b_tags = li.find("b")
        if b_tags is not None:
            title_init_movie = b_tags.text.strip()
            channel_info['title_init_movie'] = title_init_movie

        # Pega tipo inicial do filme
        i_tags = li.find("i")
        if i_tags is not None:
            type_init_movie = i_tags.text.strip()
            channel_info['type_init_movie'] = type_init_movie

        # Pega a porcentagem do filme inicial
        progress = li.find("div", class_="determinate")
        if progress and progress.has_attr("style"):
            style = progress['style']
            percent_pos = style.find('%')
            if percent_pos != -1:
                channel_info['progress_init_movie'] = style[:percent_pos + 1].split(":")[-1].strip()


        # Pega os próximos filmes
        # Encontrar todas as tags <p> dentro do elemento <li> e filtrar apenas aquelas com <strong> dentro
        next_movies = li.find_all('p')
        next_movies = [p for p in next_movies if p.find('strong')]
        ignore = True
        info_filmes = []
        for item in next_movies:
            strong_tag = item.find('strong')
            if strong_tag is not None:
                if ignore:
                    ignore = False
                    continue
                time = strong_tag.get_text(strip=True)
                filme = item.get_text(strip=True).replace(time, '').strip()
                index = filme.rfind('-')
                filme = filme[:index] + '- ' + filme[index+1:]
                info_filmes.append(f"{time} - {filme}")

        if len(info_filmes) > 0:
            next_movie_info = info_filmes[0]
            next_movie_info2 = info_filmes[1]
            channel_info['next_movie_info'] = next_movie_info
            channel_info['next_movie_info2'] = next_movie_info2

        channel_list.append(channel_info)

    return channel_list

