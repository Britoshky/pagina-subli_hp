from flask import Blueprint, render_template, request, redirect, url_for
from utils.data_utils import load_ads, save_ads
from collections import defaultdict
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from config import MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD, MAIL_SENDER

ads_bp = Blueprint('ads', __name__, template_folder='templates')

def get_ad_by_id(ad_id):
    ads = load_ads()
    return next((ad for ad in ads if ad['id'] == ad_id), None)

@ads_bp.route('/ads')
def list_ads():
    ads = load_ads()
    check_due_payments()  # Llamada para verificar pagos vencidos

    # Calcular el total formateado sin decimales
    total_sum = sum(ad['total'] for ad in ads)
    formatted_total = f"{int(total_sum):,}".replace(",", ".")

    # Procesar datos para el gráfico
    date_totals = defaultdict(int)
    for ad in ads:
        date = ad['payment_date']
        date_totals[date] += ad['total']

    # Ordenar por fecha y calcular acumulado
    sorted_dates = sorted(date_totals.keys(), key=lambda x: datetime.strptime(x, '%Y-%m-%d'))
    cumulative_totals = []
    running_total = 0
    for date in sorted_dates:
        running_total += date_totals[date]
        cumulative_totals.append({'date': date, 'total': running_total})

    print("Cumulative Totals:", cumulative_totals)
    return render_template('ads_list.html', ads=ads, cumulative_data=cumulative_totals, formatted_total=formatted_total)


@ads_bp.route('/ads/add', methods=['GET', 'POST'])
@ads_bp.route('/ads/edit/<int:id>', methods=['GET', 'POST'])
def ad_form(id=None):
    ad = get_ad_by_id(id) if id else None
    if request.method == 'POST':
        ad_data = {
            'id': id if id else max((ad['id'] for ad in load_ads()), default=0) + 1,
            'company_name': request.form['company_name'],
            'schedule': request.form.get('schedule').split(','),
            'payment_date': request.form['payment_date'],
            'total': float(request.form['total'])
        }
        ads = load_ads()
        if ad:
            ads = [ad_data if ad['id'] == id else ad for ad in ads]
        else:
            ads.append(ad_data)
        save_ads(ads)
        return redirect(url_for('ads.list_ads'))
    return render_template('ad_form.html', ad=ad or {})

@ads_bp.route('/ads/update/<int:id>', methods=['POST'])
def update_ad(id):
    ad = get_ad_by_id(id)
    if ad:
        ad.update({
            'company_name': request.form['company_name'],
            'schedule': request.form.get('schedule').split(','),
            'payment_date': request.form['payment_date'],
            'total': float(request.form['total'])
        })
        ads = load_ads()
        ads = [ad if ad['id'] == id else x for x in ads]
        save_ads(ads)
    return redirect(url_for('ads.list_ads'))
@ads_bp.route('/ads/edit/<int:id>', methods=['GET', 'POST'])
def edit_ad(id):
    ad = get_ad_by_id(id)
    if request.method == 'POST':
        # Lógica de actualización
        return redirect(url_for('ads.list_ads'))
    return render_template('ad_form.html', ad=ad)


@ads_bp.route('/ads/delete/<int:id>')
def delete_ad(id):
    ads = load_ads()
    ads = [ad for ad in ads if ad['id'] != id]
    save_ads(ads)
    return redirect(url_for('ads.list_ads'))


# Función para enviar correos
def send_email(to, subject, body):
    try:
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = MAIL_SENDER
        msg["To"] = to

        with smtplib.SMTP(MAIL_SERVER, MAIL_PORT) as server:
            server.starttls()
            server.login(MAIL_USERNAME, MAIL_PASSWORD)
            server.sendmail(MAIL_SENDER, to, msg.as_string())
        print(f"Correo enviado a {to}")
    except Exception as e:
        print(f"Error enviando correo: {e}")

# Función para verificar deudas
def check_due_payments():
    try:
        ads = load_ads()
        today = datetime.now().date()
        for ad in ads:
            payment_date = datetime.strptime(ad["payment_date"], "%Y-%m-%d").date()
            days_to_payment = (payment_date - today).days

            # Verifica si faltan exactamente 5 días
            if days_to_payment == 5:
                subject = f"Recordatorio: Pago próximo para {ad['company_name']}"
                body = (
                    f"Hola,\n\n"
                    f"Este es un recordatorio de que el pago para la empresa {ad['company_name']} está próximo.\n"
                    f"Total a pagar: ${ad['total']:,.0f}\nFecha de vencimiento: {ad['payment_date']}\n\n"
                    "Por favor, prepare el pago antes de la fecha límite."
                )
                send_email("britoshky@gmail.com", subject, body)

            # Verifica si es el día de vencimiento
            elif days_to_payment == 0:
                subject = f"Aviso de deuda: {ad['company_name']}"
                body = (
                    f"Hola,\n\n"
                    f"La empresa {ad['company_name']} tiene un pago pendiente.\n"
                    f"Total adeudado: ${ad['total']:,.0f}\nFecha de vencimiento: {ad['payment_date']}\n\n"
                    "Por favor, realice el pago lo antes posible."
                )
                send_email("britoshky@gmail.com", subject, body)
    except Exception as e:
        print(f"Error verificando pagos vencidos: {e}")
