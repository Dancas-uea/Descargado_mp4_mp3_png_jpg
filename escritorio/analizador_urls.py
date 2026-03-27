from urllib.parse import urlparse


class AnalizadorURLs:
    def __init__(self):
        self.plataformas = {
            'youtube': ['youtube.com', 'youtu.be'],
            'tiktok': ['tiktok.com'],
            'instagram': ['instagram.com'],
            'twitter': ['twitter.com', 'x.com']
        }

    def analizar(self, url):
        try:
            dominio = urlparse(url).netloc.lower()

            for plataforma, dominios in self.plataformas.items():
                if any(d in dominio for d in dominios):
                    tipo_detectado = self._detectar_tipo(url, plataforma)
                    return {
                        'plataforma': plataforma,
                        'url': url,
                        'tipo_detectado': tipo_detectado
                    }
            return None
        except Exception as e:
            return None

    def _detectar_tipo(self, url, plataforma):
        if plataforma == 'youtube':
            if '/playlist' in url or 'list=' in url:
                return 'playlist'
            return 'video'
        elif plataforma == 'tiktok':
            return 'video'
        elif plataforma == 'instagram':
            if '/reel/' in url or '/p/' in url:
                return 'video'
            return 'imagen'
        elif plataforma == 'twitter':
            return 'video'
        return 'desconocido'