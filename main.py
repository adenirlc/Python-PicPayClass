import string
from random import random
from picpay import PicPay
from config import x_seller_token, x_picpay_token

# ConfiguraÃ§Ãµes do PicPay
picpay = PicPay(x_picpay_token=x_picpay_token,
                x_seller_token=x_seller_token)


def id_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class PicPay:
    @staticmethod
    def generate_payment(value: float):
        """
        Gera um pedido e retorna-o
        :param value:
        :return:
        """
        reference_id_generated = id_generator()
        payment = picpay.payment(
            reference_id=f"{reference_id_generated}",
            callback_url="https://localhost/callback/picpay",
            return_url=f"https://localhost/pedido/{reference_id_generated}",
            value=value,
            buyer={}
        )
        return payment

    @staticmethod
    def get_status(reference_id):
        """
        A funÃ§Ã£o irÃ¡ retornar o seguinte json:
        {
            "authorizationId": "",
            "referenceId": "",
            "status": ""
        }
        authorizationId -> NÃºmero de autorizaÃ§Ã£o do pagamento (apenas se jÃ¡ tiver sido pago)
        referenceId     -> ID do Pedido
        status          -> RetornarÃ¡ o status, resultados: "created", "expired", "analysis", "paid", "completed", "refunded", "chargeback"

        :param reference_id:
        :return:
        """
        return picpay.status(reference_id=reference_id)

    @staticmethod
    def cancel_order(reference_id):
        """
        Cancela um pedido

        Caso o pedido jÃ¡ foi sido pago, ele estorna o valor Ã  conta do cliente.

        A funÃ§Ã£o retorna as seguintes chaves em um JSON:

        referenceId    -> ID do Pedido
        cancellationId -> ID Ãºnico de cancelamento

        :param reference_id:
        :return:
        """
        cancel = picpay.cancellation(reference_id=reference_id)

        return cancel
