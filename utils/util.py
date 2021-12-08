from dataclasses import dataclass
import uuid
from urllib.parse import urlparse


@dataclass
class Utils():
    """
        Clase para utilidades
    """
    __url: str = None

    def uuid_conversor(self) -> str:
        try:
            """
                crea un uuid
                :return: Retorna el uuid
                :treturn: string
            """
            random_id = uuid.uuid4().hex
            return str(random_id)
        except:
            return f"No pudo crearse el id"

    def validate_url(self) -> str:
        try:
            """
                valida un url
                :return: Retorna true o false
                :treturn: bool
            """
            result = urlparse(self.__url)
            return all([result.scheme, result.netloc])
        except:
            return False

    def __str__(self) -> str:
        return f"Url: {self.__url}"

    def __repr__(self):
        return f'{self.__class__.__name__}({repr(self.__url)})'


if __name__ == "__main__":
    a = 'http://www.cwi.nl:80/%7Eguido/Python.html'
    b = '/data/Python.html'
    c = 532
    d = u'dkakasdkjdjakdjadjfalskdjfalk'
    e = 'https://stackoverflow.com'
    f = "https://www.mercadolibre.com.ar/mario-kart-live-home-circuit-mario-set-standard-edition-nintendo-switch-fisico/p/MLA16212203#reco_item_pos=1&reco_backend=msd-item-homes&reco_backend_type=function&reco_client=home_navigation-recommendations&reco_id=529c05cd-1ba5-407b-9a00-2f069e26fd81&c_id=/home/navigation-recommendations/element&c_element_order=2&c_uid=f0496ed9-9720-4300-8c1d-2e4bba63f4a6"
    utilidades = Utils()
    print(utilidades.uuid_conversor())
    utilidades2 = Utils(f)
    print(utilidades2.validate_url())
    utilidades3 = Utils(d)
    print(utilidades3.validate_url())
    utilidades4 = Utils(c)
    print(utilidades4.validate_url())
    utilidades5 = Utils(b)
    print(utilidades5.validate_url())
    utilidades6 = Utils(a)
    print(utilidades6.validate_url())
    utilidades7 = Utils(e)
    print(utilidades7.validate_url())
