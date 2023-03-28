import asyncio

from rest_framework import mixins, viewsets
from rest_framework.response import Response

from wildberries.serializer import CardSerializer
from wildberries.utils import get_card_info, get_cards_info


class CardView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = CardSerializer

    def get_wild_data(self, request):
        if 'file' in request:
            data = []
            for i in asyncio.run(get_cards_info(request['file'])):
                try:
                    data.append(i.dict())
                except Exception:
                    article_error = {
                        'article_error: article not found'
                    }
                    return Response(article_error)
            return Response(data)
        elif 'article' in request:
            try:
                data = get_card_info(request['article']).dict()
            except Exception:
                article_error = {
                    f'article_error: article {request["article"]} not found'
                }
                return Response(article_error)
            return Response(data)

    def post(self, request):
        self.create(request)
        data = self.get_wild_data(request.data)
        return data
