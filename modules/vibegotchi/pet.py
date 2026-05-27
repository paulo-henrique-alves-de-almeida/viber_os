class Vibegotchi:
    def __init__(self, nome):
        self.nome = nome
        self.fome = 50
        self.energia = 100
        self.humor = 100
        self.aura = 100
        self.vezes_alimentado = 0  # contador pra conquista vg_cuidado
    
    def alimentar(self):
        self.fome -= 10
        self.energia += 5
        self.humor += 5
        self.aura += 100
        self.vezes_alimentado += 1
    
    def brincar(self):
        self.fome += 5
        self.energia -= 10
        self.humor += 15
        self.aura -= 100

    def dormir(self):
        self.fome += 5
        self.energia += 20
        self.humor += 10
        self.aura += 100
    
    def limitar_valores(self):
        self.fome = max(0, min(self.fome, 100))
        self.energia = max(0, min(self.energia, 100))
        self.humor = max(0, min(self.humor, 100))
        self.aura = max(0, min(self.aura, 1000))
    
    def passar_tempo(self):
        self.fome += 5
        self.energia -= 5
        self.humor -= 5
        self.aura -= 10
        self.limitar_valores()
    
    def para_dict(self):
        return {
            "nome": self.nome,
            "fome": self.fome,
            "energia": self.energia,
            "humor": self.humor,
            "aura": self.aura,
            "vezes_alimentado": self.vezes_alimentado
        }

    @classmethod
    def de_dict(cls, dados):
        pet = cls(dados["nome"])
        pet.fome = dados["fome"]
        pet.energia = dados["energia"]
        pet.humor = dados["humor"]
        pet.aura = dados["aura"]
        pet.vezes_alimentado = dados.get("vezes_alimentado", 0)
        return pet
