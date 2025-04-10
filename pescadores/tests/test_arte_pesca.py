import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from pescadores.models import ArtePesca

class ArtePescaViewTest(APITestCase):

    def setUp(self):
        super().setUp()
        self.arte1 = ArtePesca.objects.create(nome='Arte 1')
        self.arte2 = ArtePesca.objects.create(nome='Arte 2')
        self.arte3 = ArtePesca.objects.create(nome='Arte 3')

    # GET
    def test_arte_pesca_list(self):
        response = self.client.get(reverse('pescadores:arte_pesca_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
            'arte_pesca': [
                {'id': self.arte1.id, 'nome': 'Arte 1'},
                {'id': self.arte2.id, 'nome': 'Arte 2'},
                {'id': self.arte3.id, 'nome': 'Arte 3'},
            ]
        })

    def test_arte_pesca_list_empty(self):
        ArtePesca.objects.all().delete()
        response = self.client.get(reverse('pescadores:arte_pesca_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'arte_pesca': []})

    # POST
    def test_create_arte_pesca(self):
        new_arte_pesca = {'nome': 'Arte Teste 4'}
        response = self.client.post(
            reverse('pescadores:arte_pesca_list'),
            data=json.dumps(new_arte_pesca),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), {
            'arte_pesca': {
                'id': response.json()['arte_pesca']['id'],
                'nome': 'Arte Teste 4'
            }
        })

    def test_create_arte_pesca_no_data(self):
        response = self.client.post(
            reverse('pescadores:arte_pesca_list'),
            data='',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_arte_pesca_empty(self):
        response = self.client.post(
            reverse('pescadores:arte_pesca_list'),
            data=json.dumps({}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # DELETE
    def test_delete_arte_pesca(self):
        response = self.client.delete(
            reverse('pescadores:arte_pesca_detail', kwargs={'pk': self.arte2.id})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_arte_pesca_does_not_exist(self):
        response = self.client.delete(
            reverse('pescadores:arte_pesca_detail', kwargs={'pk': 999})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # PUT
    def test_put_arte_pesca(self):
        updated_data = {'nome': 'Arte Atualizada'}
        response = self.client.put(
            reverse('pescadores:arte_pesca_detail', kwargs={'pk': self.arte2.id}),
            data=json.dumps(updated_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
            'arte_pesca': {'id': self.arte2.id, 'nome': 'Arte Atualizada'}
        })

    def test_put_arte_pesca_does_not_exist(self):
        updated_data = {'nome': 'Arte Atualizada'}
        response = self.client.put(
            reverse('pescadores:arte_pesca_detail', kwargs={'pk': 999}),
            data=json.dumps(updated_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
