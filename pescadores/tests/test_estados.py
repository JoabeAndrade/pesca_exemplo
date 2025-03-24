from django.test import TestCase, Client
from pescadores.models import Uf
from unittest import skip
import json

class EstadoViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        return super().setUp()

    # GET /pescadores/estados/
    def test_uf_list(self):
        self.create_ufs()
        response = self.client.get('/pescadores/estados/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "ufs": [
                {'id': 1, 'nome': 'Bahia', 'sigla': 'BA'},
                {'id': 2, 'nome': 'Pernambuco', 'sigla': 'PE'},
                {'id': 3, 'nome': 'Alagoas', 'sigla': 'AL'},
            ]
        })

    def test_uf_list_empty(self):
        response = self.client.get('/pescadores/estados/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "ufs": []
        })

    # POST /pescadores/estados/
    def test_create_uf(self):
        new_uf_data = {'nome': 'Goiás', 'sigla': 'GO'}
        response = self.client.post(
            '/pescadores/estados/',
            data=json.dumps(new_uf_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {
            'uf': {'id': 1, 'nome': 'Goiás', 'sigla': 'GO'},
        })

    def test_create_uf_no_data(self):
        response = self.client.post(
            '/pescadores/estados/',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_create_uf_data_empty(self):
        response = self.client.post(
            '/pescadores/estados/',
            data=json.dumps({}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_create_uf_wrong_data(self):
        response = self.client.post(
            '/pescadores/estados/',
            data=json.dumps({'nome': 'João', 'idade': 25}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_get_uf(self):
        Uf.objects.create(nome='Amazonas', sigla='AM')
        response = self.client.get('/pescadores/estados/1/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "uf": {'id': 1, 'nome': 'Amazonas', 'sigla': 'AM'},
        })

    def test_get_uf_does_not_exist(self):
        response = self.client.get('/pescadores/estados/1/')
        self.assertEqual(response.status_code, 404)

    # DELETE /pescadores/estados/x/
    def test_delete_uf(self):
        self.create_ufs()
        response = self.client.delete('/pescadores/estados/2/')
        self.assertEqual(response.status_code, 204)
    
    def test_delete_uf_does_not_exist(self):
        self.create_ufs()
        response = self.client.delete('/pescadores/estados/9/')
        self.assertEqual(response.status_code, 404)
    
    # PUT /pescadores/estados/x/
    def test_put_uf(self):
        self.create_ufs()
        response = self.client.put('/pescadores/estados/3/', data=json.dumps({
            'nome': 'Pará', 'sigla': 'PA'
        }))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'uf': {'id': 3, 'nome': 'Pará', 'sigla': 'PA'}
        })
    
    def test_put_uf_does_not_exist(self):
        response = self.client.put('/pescadores/estados/8/', data=json.dumps({'nome': 'Pará', 'sigla': 'PA'}))
        self.assertEqual(response.status_code, 404)

    @skip
    def test_put_uf_no_data(self):
        self.create_ufs()
        response = self.client.put('/pescadores/estados/1/', data=json.dumps({}))
        self.assertEqual(response.status_code, 400)

    @skip
    def test_put_uf_invalid_data(self):
        self.create_ufs()
        response = self.client.put('/pescadores/estados/1/', data=json.dumps({
            'marca': 'Toyota', 'ano': 2020
        }))
        self.assertEqual(response.status_code, 400)

    def test_put_uf_insufficient_data(self):
        self.create_ufs()
        response = self.client.put('/pescadores/estados/1/', data=json.dumps({
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