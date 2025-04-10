from django.test import TestCase, Client
from pescadores.models import Uf, Municipio
from django.urls import reverse
from rest_framework import status
from unittest import skip
import json

class MunicipioViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        return super().setUp()

    # GET /pescadores/municipios/
    def test_list_municipios(self):
        self.create_municipios()
        response = self.client.get(reverse('pescadores:municipio_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
            "municipios": [
                {'id': 1, 'nome': 'Salvador', 'uf': 1},
                {'id': 2, 'nome': 'Ilhéus', 'uf': 1},
                {'id': 3, 'nome': 'Recife', 'uf': 2},
                {'id': 4, 'nome': 'Maceió', 'uf': 3},
            ]
        })

    def test_list_municipios_empty(self):
        response = self.client.get(reverse('pescadores:municipio_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
            "municipios": []
        })

    # POST /pescadores/municipios/
    def test_create_municipio(self):
        estado = Uf.objects.create(nome="Bahia", sigla="BA")
        new_municipio = {'nome': 'Ilhéus', 'uf': estado.id}
        response = self.client.post(reverse('pescadores:municipio_list'), data=json.dumps(new_municipio), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), {
            "municipio": {'id': 1, 'nome': 'Ilhéus', 'uf': estado.id}
        })

    def test_create_municipio_empty(self):
        response =  self.client.post(reverse('pescadores:municipio_list'), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # PUT /pescadores/municipios/
    # def test_put_municipios(self):

    # DELETE /pescadores/municipios/x/
    def test_delete_municipio(self):
        self.create_municipios()
        response = self.client.delete(reverse('pescadores:municipio_detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_municipio_not_exist(self):
        self.create_municipios()
        response = self.client.delete(reverse('pescadores:municipio_detail', kwargs={'pk': 12}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

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