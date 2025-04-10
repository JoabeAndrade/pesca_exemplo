import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from pescadores.models import AreaPesca

class AreaPescaViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        return super().setUp()
    
    def create_area_pesca(self):
        area1 = AreaPesca.objects.create(descricao='Área Teste 1')
        area2 = AreaPesca.objects.create(descricao='Área Teste 2')
        return area1, area2

    # GET
    def test_area_pesca_list(self):
        self.create_area_pesca()
        response = self.client.get(reverse('pescadores:area_pesca_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
            'areas_pescas': [
                {'id': 1, 'descricao': 'Área Teste 1'},
                {'id': 2, 'descricao': 'Área Teste 2'}
            ]
        })

    def test_area_pesca_list_empty(self):
        response = self.client.get(reverse('pescadores:area_pesca_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
            'areas_pescas': []
        })

    # POST
    def test_create_area_pesca(self):
        new_area_pesca = {'descricao': 'Área Teste 3'}
        response = self.client.post(
            reverse('pescadores:area_pesca_list'), 
            data=json.dumps(new_area_pesca), 
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), {
            'area_pesca': {'id': 1, 'descricao': 'Área Teste 3'}
        })

    def test_create_area_pesca_no_data(self):
        response = self.client.post(
            reverse('pescadores:area_pesca_list'), 
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_area_pesca_empty(self):
         response = self.client.post(
            reverse('pescadores:area_pesca_list'),
            data=json.dumps({}),
            content_type='application/json'
        )
         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # DELETE
    def test_delete_area_pesca(self):
        _, area2 = self.create_area_pesca()
        response = self.client.delete(reverse('pescadores:area_pesca_detail', kwargs={'pk': area2.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_delete_area_pesca_does_not_exist(self):
        self.create_area_pesca()
        response = self.client.delete(reverse('pescadores:area_pesca_detail', kwargs={'pk': 9}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    # PUT
    def test_put_area_pesca(self):
        self.create_area_pesca()
        response = self.client.put(reverse('pescadores:area_pesca_detail', kwargs={'pk': 2}), data=json.dumps({
            'descricao': 'Área Teste 5'
        }))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
            'area_pesca': {'id': 2, 'descricao': 'Área Teste 5'}
        })
    
    def test_put_area_pesca_does_not_exist(self):
        response = self.client.put(reverse('pescadores:area_pesca_detail', kwargs={'pk': 8}), data=json.dumps({'descricao': 'Área Teste 5'}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)