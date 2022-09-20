import asyncio
import time
import requests
from discord_webhook import DiscordWebhook, DiscordEmbed

url = 'https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search'

headers = {

}


class Currency:
    def __init__(self, asset, trade_type, pay_type, url):
        self.asset = asset
        self.trade_type = trade_type
        self.pay_type = pay_type
        self.url = url

    async def check_orders(self):
        data = {
            'asset': self.asset,
            'countries': [],
            'fiat': "RUB",
            'page': 1,
            'payTypes': self.pay_type,
            'proMerchantAds': 'false',
            'publisherType': None,
            'rows': 10,
            'tradeType': self.trade_type
        }

        data2 = {
            'asset': self.asset,
            'countries': [],
            'fiat': "RUB",
            'page': 1,
            'payTypes': self.pay_type,
            'proMerchantAds': 'false',
            'publisherType': None,
            'rows': 10,
            'tradeType': 'SELL'
        }

        response = requests.post(url, headers=headers, json=data).json()
        response_sell = requests.post(url, headers=headers, json=data2).json()
        percent = 100 - (float(response['data'][0]['adv']['price']) / (float(response_sell['data'][0]['adv']['price'])/100))
        print(round(percent, 2))
        if percent >= 0.5:
            webhook = DiscordWebhook(
                url='your webhook link')
            embed = DiscordEmbed(title='Good Price Detected!', description='Found something delicious for you 💸',
                                 color='5865F2')
            embed.set_timestamp()

            embed.add_embed_field(name='Limit:', value=f'{round(float(response["data"][0]["adv"]["minSingleTransAmount"]))} - {round(float(response["data"][0]["adv"]["maxSingleTransAmount"]))} RUB')
            embed.add_embed_field(name='Available:', value=f'{response["data"][0]["adv"]["tradableQuantity"]} {self.asset}')
            embed.add_embed_field(name='Spread:', value=f'{round(float(response_sell["data"][0]["adv"]["price"]) - float(response["data"][0]["adv"]["price"]), 2)} RUB')
            embed.add_embed_field(name='Selling Price:', value=f'{float(response_sell["data"][0]["adv"]["price"])} RUB')
            embed.add_embed_field(name='Detected Price:', value=f'{float(response["data"][0]["adv"]["price"])} RUB')
            embed.add_embed_field(name='Percent:', value=f'{round(percent, 2)}%')
            embed.add_embed_field(name='Income:', value=f'{round(float(response["data"][0]["adv"]["tradableQuantity"]) * round(float(response_sell["data"][0]["adv"]["price"]) - float(response["data"][0]["adv"]["price"]), 2))}  RUB')
            embed.add_embed_field(name='Payment Methods:', value=f'{self.pay_type[0]}')
            embed.set_thumbnail(url=self.url)
            embed.set_footer(text='Astrum Software', icon_url='https://gateway.pinata.cloud/ipfs/QmUCn5R2vEAAc1L8pFhcCdGK3ePaXwYPGQWSAd3PebfCru')
            embed.set_url(
                url=f'https://p2p.binance.com/ru/advertiserDetail?advertiserNo={response["data"][0]["advertiser"]["userNo"]}')

            webhook.add_embed(embed)

            response = webhook.execute()
            time.sleep(60)
        else:
            print(self.asset)
            time.sleep(1)


'''def check_median():
    price_sum = 0
    response = requests.post(url, headers=headers, json=data).json()
    for i in range(len(response['data'])):
        price_sum = price_sum + response['data'][i]['adv']['price']
    return price_sum / len(response['data'])'''


async def main():
    while True:
        usdt_tink = asyncio.create_task(Currency('USDT', 'BUY', ["TinkoffNew"], 'https://gateway.pinata.cloud/ipfs/Qme6HbCcvh4sqEBT6dbh3CVwpTTBB4Lcj6ALQgxVTeZ8pZ/usdt.png').check_orders())
        btc_tink = asyncio.create_task(Currency('BTC', 'BUY', ["TinkoffNew"], 'https://gateway.pinata.cloud/ipfs/Qme6HbCcvh4sqEBT6dbh3CVwpTTBB4Lcj6ALQgxVTeZ8pZ/btc.png').check_orders())
        busd_tink = asyncio.create_task(Currency('BUSD', 'BUY', ["TinkoffNew"], 'https://gateway.pinata.cloud/ipfs/Qme6HbCcvh4sqEBT6dbh3CVwpTTBB4Lcj6ALQgxVTeZ8pZ/busd.png').check_orders())
        bnb_tink = asyncio.create_task(Currency('BNB', 'BUY', ["TinkoffNew"], 'https://gateway.pinata.cloud/ipfs/Qme6HbCcvh4sqEBT6dbh3CVwpTTBB4Lcj6ALQgxVTeZ8pZ/bnb.png').check_orders())
        eth_tink = asyncio.create_task(Currency('ETH', 'BUY', ["TinkoffNew"], 'https://gateway.pinata.cloud/ipfs/Qme6HbCcvh4sqEBT6dbh3CVwpTTBB4Lcj6ALQgxVTeZ8pZ/eth.png').check_orders())
        usdt_raif = asyncio.create_task(Currency('USDT', 'BUY', ["RaiffeisenBank"], 'https://gateway.pinata.cloud/ipfs/Qme6HbCcvh4sqEBT6dbh3CVwpTTBB4Lcj6ALQgxVTeZ8pZ/usdt.png').check_orders())
        btc_raif = asyncio.create_task(Currency('BTC', 'BUY', ["RaiffeisenBank"], 'https://gateway.pinata.cloud/ipfs/Qme6HbCcvh4sqEBT6dbh3CVwpTTBB4Lcj6ALQgxVTeZ8pZ/btc.png').check_orders())
        busd_raif = asyncio.create_task(Currency('BUSD', 'BUY', ["RaiffeisenBank"], 'https://gateway.pinata.cloud/ipfs/Qme6HbCcvh4sqEBT6dbh3CVwpTTBB4Lcj6ALQgxVTeZ8pZ/busd.png').check_orders())
        bnb_raif = asyncio.create_task(Currency('BNB', 'BUY', ["RaiffeisenBank"], 'https://gateway.pinata.cloud/ipfs/Qme6HbCcvh4sqEBT6dbh3CVwpTTBB4Lcj6ALQgxVTeZ8pZ/bnb.png').check_orders())
        eth_raif = asyncio.create_task(Currency('ETH', 'BUY', ["RaiffeisenBank"], 'https://gateway.pinata.cloud/ipfs/Qme6HbCcvh4sqEBT6dbh3CVwpTTBB4Lcj6ALQgxVTeZ8pZ/eth.png').check_orders())
        usdt_ros = asyncio.create_task(Currency('USDT', 'BUY', ["RosBankNew"], 'https://gateway.pinata.cloud/ipfs/Qme6HbCcvh4sqEBT6dbh3CVwpTTBB4Lcj6ALQgxVTeZ8pZ/usdt.png').check_orders())
        btc_ros = asyncio.create_task(Currency('BTC', 'BUY', ["RosBankNew"], 'https://gateway.pinata.cloud/ipfs/Qme6HbCcvh4sqEBT6dbh3CVwpTTBB4Lcj6ALQgxVTeZ8pZ/btc.png').check_orders())
        busd_ros = asyncio.create_task(Currency('BUSD', 'BUY', ["RosBankNew"], 'https://gateway.pinata.cloud/ipfs/Qme6HbCcvh4sqEBT6dbh3CVwpTTBB4Lcj6ALQgxVTeZ8pZ/busd.png').check_orders())
        bnb_ros = asyncio.create_task(Currency('BNB', 'BUY', ["RosBankNew"], 'https://gateway.pinata.cloud/ipfs/Qme6HbCcvh4sqEBT6dbh3CVwpTTBB4Lcj6ALQgxVTeZ8pZ/bnb.png').check_orders())
        eth_ros = asyncio.create_task(Currency('ETH', 'BUY', ["RosBankNew"], 'https://gateway.pinata.cloud/ipfs/Qme6HbCcvh4sqEBT6dbh3CVwpTTBB4Lcj6ALQgxVTeZ8pZ/eth.png').check_orders())
        await asyncio.wait([usdt_tink, btc_tink, busd_tink, bnb_tink, eth_tink, usdt_raif, btc_raif, busd_raif, bnb_raif, eth_raif, usdt_ros, btc_ros, busd_ros, bnb_ros, eth_ros])


if __name__ == '__main__':
    asyncio.run(main())
