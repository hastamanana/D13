from ads.models import Ad, Offer


def counters(request):
    if request.user.is_authenticated:
        return {
            'all_ads': Ad.objects.all(),
            'user_ads': Ad.objects.filter(author=request.user),
            'user_offers': Offer.objects.filter(ad__author=request.user),
        }
    else:
        return {
            'all_ads': Ad.objects.none(),
            'user_ads': Ad.objects.none(),
            'user_offers': Offer.objects.none(),
        }
