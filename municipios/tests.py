from django.test import TestCase, Client
from municipios.models import Uf, Municipio
from unittest import skip
import json

class EstadoViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        return super().setUp()

    # GET /municipios/estados/
    def test_uf_list(self):
        self.create_ufs()
        response = self.client.get('/municipios/estados/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "ufs": [
                {'id': 1, 'nome': 'Bahia', 'sigla': 'BA'},
                {'id': 2, 'nome': 'Pernambuco', 'sigla': 'PE'},
                {'id': 3, 'nome': 'Alagoas', 'sigla': 'AL'},
            ]
        })

    def test_uf_list_empty(self):
        response = self.client.get('/municipios/estados/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "ufs": []
        })

    # POST /municipios/estados/
    def test_create_uf(self):
        new_uf_data = {'nome': 'Goiás', 'sigla': 'GO'}
        response = self.client.post(
            '/municipios/estados/',
            data=json.dumps(new_uf_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {
            'uf': {'id': 1, 'nome': 'Goiás', 'sigla': 'GO'},
        })

    def test_create_uf_no_data(self):
        response = self.client.post(
            '/municipios/estados/',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_create_uf_data_empty(self):
        response = self.client.post(
            '/municipios/estados/',
            data=json.dumps({}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_create_uf_wrong_data(self):
        response = self.client.post(
            '/municipios/estados/',
            data=json.dumps({'nome': 'João', 'idade': 25}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_get_uf(self):
        Uf.objects.create(nome='Amazonas', sigla='AM')
        response = self.client.get('/municipios/estados/1/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "uf": {'id': 1, 'nome': 'Amazonas', 'sigla': 'AM'},
        })

    def test_get_uf_does_not_exist(self):
        response = self.client.get('/municipios/estados/1/')
        self.assertEqual(response.status_code, 404)

    # DELETE /municipios/estados/x/
    def test_delete_uf(self):
        self.create_ufs()
        response = self.client.delete('/municipios/estados/2/')
        self.assertEqual(response.status_code, 204)
    
    def test_delete_uf_does_not_exist(self):
        self.create_ufs()
        response = self.client.delete('/municipios/estados/9/')
        self.assertEqual(response.status_code, 404)
    
    # PUT /municipios/estados/x/
    def test_put_uf(self):
        self.create_ufs()
        response = self.client.put('/municipios/estados/3/', data=json.dumps({
            'nome': 'Pará', 'sigla': 'PA'
        }))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'uf': {'id': 3, 'nome': 'Pará', 'sigla': 'PA'}
        })
    
    def test_put_uf_does_not_exist(self):
        response = self.client.put('/municipios/estados/8/', data=json.dumps({'nome': 'Pará', 'sigla': 'PA'}))
        self.assertEqual(response.status_code, 404)

    @skip
    def test_put_uf_no_data(self):
        self.create_ufs()
        response = self.client.put('/municipios/estados/1/', data=json.dumps({}))
        self.assertEqual(response.status_code, 400)

    @skip
    def test_put_uf_invalid_data(self):
        self.create_ufs()
        response = self.client.put('/municipios/estados/1/', data=json.dumps({
            'marca': 'Toyota', 'ano': 2020
        }))
        self.assertEqual(response.status_code, 400)

    def test_put_uf_insufficient_data(self):
        self.create_ufs()
        response = self.client.put('/municipios/estados/1/', data=json.dumps({
            'nome': 'Maranhão',
        }))
        self.assertEqual(response.status_code, 400)

    def create_ufs(self):
        ufs_data = [
            ('Bahia', 'BA',),
            ('Pernambuco', 'PE',),
            ('Alagoas', 'AL',),
        ]
        for uf in ufs_data:
            Uf.objects.create(nome=uf[0], sigla=uf[1])


class MunicipioViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        return super().setUp()

    # GET /municipios/
    def test_list_municipios(self):
        self.create_municipios()
        response = self.client.get('/municipios/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "municipios": [
                {'id': 1, 'nome': 'Salvador', 'uf': 1},
                {'id': 2, 'nome': 'Ilhéus', 'uf': 1},
                {'id': 3, 'nome': 'Recife', 'uf': 2},
                {'id': 4, 'nome': 'Maceió', 'uf': 3},
            ]
        })

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
