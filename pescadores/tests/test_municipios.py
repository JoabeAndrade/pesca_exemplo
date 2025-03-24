from django.test import TestCase, Client
from pescadores.models import Uf, Municipio
from unittest import skip
import json

class MunicipioViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        return super().setUp()

    # GET /pescadores/municipios/
    def test_list_municipios(self):
        self.create_municipios()
        response = self.client.get('/pescadores/municipios/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "municipios": [
                {'id': 1, 'nome': 'Salvador', 'uf': 1},
                {'id': 2, 'nome': 'Ilhéus', 'uf': 1},
                {'id': 3, 'nome': 'Recife', 'uf': 2},
                {'id': 4, 'nome': 'Maceió', 'uf': 3},
            ]
        })

    def test_list_municipios_empty(self):
        response = self.client.get('/pescadores/municipios/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "municipios": []
        })

    # POST /pescadores/municipios/
    def test_create_municipio(self):
        estado = Uf.objects.create(nome="Bahia", sigla="BA")
        new_municipio = {'nome': 'Ilhéus', 'uf': estado.id}
        response = self.client.post('/pescadores/municipios/', data=json.dumps(new_municipio), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {
            "municipio": {'id': 1, 'nome': 'Ilhéus', 'uf': estado.id}
        })

    def test_create_municipio_empty(self):
        response =  self.client.post('/pescadores/municipios/', content_type='aplication/json')
        self.assertEqual(response.status_code, 400)

    # PUT /pescadores/municipios/
    # def test_put_municipios(self):

    # DELETE /pescadores/municipios/x/
    def test_delete_municipio(self):
        self.create_municipios()
        response = self.client.delete('/pescadores/municipios/1/')
        self.assertEqual(response.status_code, 204)

    def test_delete_municipio_not_exist(self):
        self.create_municipios()
        response = self.client.delete('/pescadores/municipios/12/')
        self.assertEqual(response.status_code, 404)

    def create_municipios(self):
        ba = Uf.objects.create(nome='Bahia', sigla='BA')
        pe = Uf.objects.create(nome='Pernambuco', sigla='PE')
        al = Uf.objects.create(nome='Alagoas', sigla='AL')

        municipio_data = [
            ('Salvador', ba,),
            ('Ilhéus', ba,),
            ('Recife', pe,),
            ('Maceió', al,),
        ]
        for mun in municipio_data:
            Municipio.objects.create(nome=mun[0], uf=mun[1])