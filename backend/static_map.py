import requests

# URLs antiguas
# url = "https://maps.googleapis.com/maps/api/staticmap?center=-38.25466,-4.971062&zoom=13&size=600x300&maptype=roadmap&markers=color:blue|label:S|40.702147,-74.015794&markers=color:green|label:G|40.711614,-74.012318&markers=color:red|label:C|40.718217,-73.998284"
tmp_url = "https://maps.googleapis.com/maps/api/staticmap?center={},{}&zoom={}&size=500x500&maptype=satellite&key={}"

def crea_url(data):
    return tmp_url.format(data["lat"], data["lon"], data["zoom"], data["key"])  

def save_imagen(data, image_name):
    url = crea_url(data)
    r = requests.get(url)
    f = open('%s.png' % image_name,'wb')
    f.write(r.content)
    f.close()

# proxy = ""  # In case you need a proxy
# proxies = {"http": proxy, "https": proxy}
# sesion = requests.Session()
# sesion.proxies = proxies

# Aqui se modifican los datos
data = {"lat": 6.755331569175543, "lon": -4.530004939961217, 
        "zoom": 16, "key":"AIzaSyCdnVX6p6LQ9v5NhwL-wJtijkCsmKw4_rU"}
image_name = "./../database/data/map/gm2img"
save_imagen(data, image_name)