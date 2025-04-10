from django.test import TestCase, Client
from rest_framework import status
from pescadores.models import Uf
from django.urls import reverse
from unittest import skip
import json

class EstadoViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        return super().setUp()

    # GET /pescadores/estados/
    def test_uf_list(self):
        self.create_ufs()
        response = self.client.get(reverse('pescadores:uf_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
            "ufs": [
                {'id': 1, 'nome': 'Bahia', 'sigla': 'BA'},
                {'id': 2, 'nome': 'Pernambuco', 'sigla': 'PE'},
                {'id': 3, 'nome': 'Alagoas', 'sigla': 'AL'},
            ]
        })

    def test_uf_list_empty(self):
        response = self.client.get(reverse('pescadores:uf_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
            "ufs": []
        })

    # POST /pescadores/estados/
    def test_create_uf(self):
        new_uf_data = {'nome': 'Goiás', 'sigla': 'GO'}
        response = self.client.post(
            reverse('pescadores:uf_list'),
            data=json.dumps(new_uf_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), {
            'uf': {'id': 1, 'nome': 'Goiás', 'sigla': 'GO'},
        })

    def test_create_uf_no_data(self):
        response = self.client.post(
            reverse('pescadores:uf_list'),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_uf_data_empty(self):
        response = self.client.post(
            reverse('pescadores:uf_list'),
            data=json.dumps({}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_uf_wrong_data(self):
        response = self.client.post(
            reverse('pescadores:uf_list'),
            data=json.dumps({'nome': 'João', 'idade': 25}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_uf(self):
        Uf.objects.create(nome='Amazonas', sigla='AM')
        response = self.client.get(reverse('pescadores:uf_detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
            "uf": {'id': 1, 'nome': 'Amazonas', 'sigla': 'AM'},
        })

    def test_get_uf_does_not_exist(self):
        response = self.client.get(reverse('pescadores:uf_detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # DELETE /pescadores/estados/x/
    def test_delete_uf(self):
        self.create_ufs()
        response = self.client.delete(reverse('pescadores:uf_detail', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_delete_uf_does_not_exist(self):
        self.create_ufs()
        response = self.client.delete(reverse('pescadores:uf_detail', kwargs={'pk': 9}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    # PUT /pescadores/estados/x/
    def test_put_uf(self):
        self.create_ufs()
        response = self.client.put(reverse('pescadores:uf_detail', kwargs={'pk': 3}), data=json.dumps({
            'nome': 'Pará', 'sigla': 'PA'
        }))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
            'uf': {'id': 3, 'nome': 'Pará', 'sigla': 'PA'}
        })
    
    def test_put_uf_does_not_exist(self):
        response = self.client.put(reverse('pescadores:uf_detail', kwargs={'pk': 8}), data=json.dumps({'nome': 'Pará', 'sigla': 'PA'}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @skip
    def test_put_uf_no_data(self):
        self.create_ufs()
        response = self.client.put(reverse('pescadores:uf_detail', kwargs={'pk': 1}), data=json.dumps({}))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @skip
    def test_put_uf_invalid_data(self):
        self.create_ufs()
        response = self.client.put(reverse('pescadores:uf_detail', kwargs={'pk': 1}), data=json.dumps({
            'marca': 'Toyota', 'ano': 2020
        }))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_uf_insufficient_data(self):
        self.create_ufs()
        response = self.client.put(reverse('pescadores:uf_detail', kwargs={'pk': 1}), data=json.dumps({
            'nome': 'Maranhão',
        }))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def create_ufs(self):
        ufs_data = [
            ('Bahia', 'BA',),
            ('Pernambuco', 'PE',),
            ('Alagoas', 'AL',),
        ]
        for uf in ufs_data:
            Uf.objects.create(nome=uf[0], sigla=uf[1])