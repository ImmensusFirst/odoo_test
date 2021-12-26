import os
import ssl
import xmlrpc.client as cli

from django.shortcuts import redirect, render

from dotenv import load_dotenv

from fb_form.forms import FbFormForm

load_dotenv()

odoo_url = 'https://gcrm.odoo.com'
odoo_db = os.environ.get('ODOO_DB')
odoo_username = os.environ.get('ODOO_USERNAME')
odoo_password = os.environ.get('ODOO_PASSWORD')
odoo_common = cli.ServerProxy('{}/xmlrpc/2/common'.format(odoo_url),
                              context=ssl._create_unverified_context())
odoo_models = cli.ServerProxy('{}/xmlrpc/2/object'.format(odoo_url),
                              context=ssl._create_unverified_context())


def index(request):
    form = FbFormForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            if not odoo_write_rec(form.cleaned_data):
                return render(request, 'message.html', {
                    'message': 'Ошибка записи, попробуйте позже!',
                    'page_title': 'Запись'})
            return redirect('index')
    context = {
        'form': form,
    }
    return render(request, 'fb_form.html', context)


def odoo_auth():
    return odoo_common.authenticate(odoo_db, odoo_username, odoo_password, {})


def get_or_create_record(uid, table, value):
    rec = odoo_models.execute_kw(odoo_db, uid, odoo_password,
                                 table, 'search',
                                 [[['name', '=', value]]])
    if not len(rec):
        rec_id = odoo_models.execute_kw(
            odoo_db, uid, odoo_password, table,
            'create', [{'name': value, }])
    else:
        rec_id = rec[0]

    return rec_id


def odoo_write_rec(context):
    uid = odoo_auth()
    if not uid:
        return False

    medium_id = get_or_create_record(uid, 'utm.medium', 'Google Adwords')
    source_id = get_or_create_record(uid, 'utm.source', 'Сайт')
    tag_id = get_or_create_record(uid, 'crm.tag', 'Заявка с сайта')

    rec_id = odoo_models.execute_kw(
        odoo_db, uid, odoo_password, 'crm.lead', 'create', [{
            'name': context['text'],
            'partner_name': context['partner_name'],
            'email_from': context['email_from'],
            'tag_ids': [tag_id, ],
            'source_id': source_id,
            'medium_id': medium_id}])

    if not rec_id:
        return False

    return True
