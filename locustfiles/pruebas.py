from locust import HttpUser, task, between
from random import randint


class webSiteUser(HttpUser):
    wait_time = between(1,5)

    @task(2)
    def ver_desembolsos(self):
        desembolso_id = randint(216,430)
        self.client.get(f'/custodia/desembolso_update/{desembolso_id}/', name='/custodia/desembolsos')
    @task(4)
    def lista_desembolsos(self):
        self.client.get('/custodia/desembolso_list/', name='custodia/desembolso_list')

    @task(2)
    def lista_historial(self):
        self.client.get('/custodia/historial/', name='custodia/historial_list')
    @task(1)
    def ver_historial(self):
        id = randint(6,170)
        self.client.get(f'/custodia/detalle_historial/{id}/', name='/custodia/historial')
